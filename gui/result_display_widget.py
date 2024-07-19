import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from camera_feed import CameraFeed
from object_detection import detect_object
from visualization import visualize_result
from utils import save_template, load_template, resize_image

class ResultDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.camera = CameraFeed()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.mode = 'idle'
        self.current_frame = None
        self.roi_coords = None
        self.is_drawing = False
        self.match_threshold = 0.98
        self._has_template = False
        self._is_detecting = False
        self.template = None

    def start_template_capture(self):
        self.camera.start()
        cv2.namedWindow("Capture Template")
        cv2.setMouseCallback("Capture Template", self.draw_rectangle)
        
        self.roi_coords = None
        self.is_drawing = True
        self.template_captured = False
        
        while not self.template_captured:
            frame = self.camera.read_frame()
            if frame is None:
                break
            
            display_frame = frame.copy()
            if self.roi_coords:
                cv2.rectangle(display_frame, (self.roi_coords[0], self.roi_coords[1]),
                              (self.roi_coords[2], self.roi_coords[3]), (0, 255, 0), 2)
            
            cv2.imshow("Capture Template", display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break
        
        cv2.destroyWindow("Capture Template")
        self.camera.stop()
        self._has_template = True
        self._is_detecting = False

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.roi_coords = [x, y, x, y]
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.roi_coords:
                self.roi_coords[2], self.roi_coords[3] = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            if self.roi_coords:
                self.roi_coords[2], self.roi_coords[3] = x, y
                # Ensure we have a valid rectangle
                if self.roi_coords[2] != self.roi_coords[0] and self.roi_coords[3] != self.roi_coords[1]:
                    self.capture_template()
                else:
                    self.roi_coords = None
                    QMessageBox.warning(self, "Warning", "Invalid selection. Please try again.")

    def capture_template(self):
        if self.roi_coords:
            frame = self.camera.read_frame()
            if frame is not None:
                x1, y1, x2, y2 = self.roi_coords
                # Ensure coordinates are in the correct order
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                
                # Check if ROI is within frame boundaries
                height, width = frame.shape[:2]
                x1, x2 = max(0, x1), min(width, x2)
                y1, y2 = max(0, y1), min(height, y2)
                
                # Check if ROI has a valid size
                if x2 - x1 > 0 and y2 - y1 > 0:
                    template = frame[y1:y2, x1:x2]
                    if template.size > 0:
                        save_template(template, [x1, y1, x2, y2])
                        self.template_captured = True
                        self._has_template = True
                        QMessageBox.information(self, "Success", "Template captured successfully!")
                    else:
                        QMessageBox.warning(self, "Warning", "Failed to capture template. The selected area is empty.")
                else:
                    QMessageBox.warning(self, "Warning", "Invalid ROI size. Please select a larger area.")
            else:
                QMessageBox.warning(self, "Warning", "Failed to capture frame. Please try again.")
        else:
            QMessageBox.warning(self, "Warning", "No ROI selected. Please try again.")

    def start_detection(self):
        self.mode = 'detection'
        template_data = load_template()
        if template_data is None or len(template_data) != 2:
            QMessageBox.warning(self, "Warning", "Failed to load template. Please capture a new template.")
            return
        self.template, self.roi_coords = template_data
        if self.template is None or self.roi_coords is None:
            QMessageBox.warning(self, "Warning", "Failed to load template. Please capture a new template.")
            return
        self.camera.start()
        self.timer.start(30)
        self._is_detecting = True

    def stop(self):
        self.timer.stop()
        self.camera.stop()
        self.mode = 'idle'
        self.clear_display()
        self._is_detecting = False

    def clear_display(self):
        self.image_label.clear()

    def update_frame(self):
        frame = self.camera.read_frame()
        if frame is not None:
            self.current_frame = frame.copy()
            if self.mode == 'detection':
                detection_result = detect_object(frame, self.template)
                if detection_result:
                    frame = visualize_result(frame, detection_result)
                    
                    # Draw ROI
                    cv2.rectangle(frame, (self.roi_coords[0], self.roi_coords[1]),
                                  (self.roi_coords[2], self.roi_coords[3]), (0, 0, 255), 2)
                    
                    # Change ROI color if object detected
                    if detection_result[2] > self.match_threshold:
                        cv2.rectangle(frame, (self.roi_coords[0], self.roi_coords[1]),
                                      (self.roi_coords[2], self.roi_coords[3]), (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "No match found", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            self.display_frame(frame)

    def display_frame(self, frame):
        frame = resize_image(frame)  # Resize the frame if it's too large
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def set_match_threshold(self, value):
        self.match_threshold = value

    def has_template(self):
        return self._has_template

    def is_detecting(self):
        return self._is_detecting

    # def adjust_roi(self, dx, dy):
    #     if self.roi_coords:
    #         self.roi_coords[0] += dx
    #         self.roi_coords[1] += dy
    #         self.roi_coords[2] += dx
    #         self.roi_coords[3] += dy
    #         update_roi_coords(self.roi_coords)

    def closeEvent(self, event):
        self.stop()
        super().closeEvent(event)

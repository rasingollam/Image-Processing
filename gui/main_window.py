from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                             QHBoxLayout, QMessageBox, QLabel, QSlider, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import QIcon
from .result_display_widget import ResultDisplayWidget
from utils import load_template, save_count, load_count
from config import MATCH_THRESHOLD

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Searchch")
        self.setWindowIcon(QIcon('resources/app_icon.png'))
        self.setGeometry(100, 100, 1000, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.result_display = ResultDisplayWidget()
        self.layout.addWidget(self.result_display)

        self.control_layout = QHBoxLayout()
        self.layout.addLayout(self.control_layout)

        # Left side controls
        self.left_controls = QGroupBox("Controls")
        self.left_layout = QVBoxLayout(self.left_controls)
        self.control_layout.addWidget(self.left_controls)

        self.capture_template_button = QPushButton("Capture Template")
        self.start_detection_button = QPushButton("Start Detection")
        self.stop_button = QPushButton("Stop")
        self.count_button = QPushButton("Count Object")
        self.reset_count_button = QPushButton("Reset Count")
        self.help_button = QPushButton("Help")

        self.left_layout.addWidget(self.capture_template_button)
        self.left_layout.addWidget(self.start_detection_button)
        self.left_layout.addWidget(self.stop_button)
        self.left_layout.addWidget(self.count_button)
        self.left_layout.addWidget(self.reset_count_button)
        self.left_layout.addWidget(self.help_button)

        # # ROI adjustment controls
        # self.roi_controls = QGroupBox("ROI Adjustment")
        # self.roi_layout = QVBoxLayout(self.roi_controls)
        # self.left_layout.addWidget(self.roi_controls)

        # self.roi_up_button = QPushButton("Move Up")
        # self.roi_down_button = QPushButton("Move Down")
        # self.roi_left_button = QPushButton("Move Left")
        # self.roi_right_button = QPushButton("Move Right")

        # self.roi_layout.addWidget(self.roi_up_button)
        # self.roi_layout.addWidget(self.roi_down_button)
        # self.roi_layout.addWidget(self.roi_left_button)
        # self.roi_layout.addWidget(self.roi_right_button)

        # Right side info
        self.right_info = QGroupBox("Info")
        self.right_layout = QVBoxLayout(self.right_info)
        self.control_layout.addWidget(self.right_info)

        self.status_label = QLabel("Status: Idle")
        self.right_layout.addWidget(self.status_label)

        self.template_preview = QLabel("Template Preview")
        self.template_preview.setFixedSize(200, 200)
        self.template_preview.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.template_preview)

        self.threshold_label = QLabel(f"Match Threshold: {MATCH_THRESHOLD}")
        self.right_layout.addWidget(self.threshold_label)

        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(int(MATCH_THRESHOLD * 100))
        self.right_layout.addWidget(self.threshold_slider)

        self.count_label = QLabel("Count: 0")
        self.right_layout.addWidget(self.count_label)

        self.capture_template_button.clicked.connect(self.start_template_capture)
        self.start_detection_button.clicked.connect(self.start_detection)
        self.stop_button.clicked.connect(self.stop)
        self.count_button.clicked.connect(self.increment_count)
        self.reset_count_button.clicked.connect(self.reset_count)
        self.help_button.clicked.connect(self.show_help)
        self.threshold_slider.valueChanged.connect(self.update_threshold)

        # self.roi_up_button.clicked.connect(lambda: self.adjust_roi(0, -5))
        # self.roi_down_button.clicked.connect(lambda: self.adjust_roi(0, 5))
        # self.roi_left_button.clicked.connect(lambda: self.adjust_roi(-5, 0))
        # self.roi_right_button.clicked.connect(lambda: self.adjust_roi(5, 0))

        self.object_count = load_count()
        self.update_count(self.object_count)

        self.update_button_states()
        self.update_template_preview()

    def start_template_capture(self):
        try:
            self.result_display.start_template_capture()
            self.status_label.setText("Status: Template Captured")
            self.update_template_preview()
            self.update_button_states()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start template capture: {str(e)}")

    def start_detection(self):
        try:
            self.result_display.start_detection()
            self.status_label.setText("Status: Detection Running")
            self.update_button_states()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start detection: {str(e)}")

    def stop(self):
        try:
            self.result_display.stop()
            self.status_label.setText("Status: Idle")
            self.update_button_states()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stop: {str(e)}")

    def increment_count(self):
        self.object_count += 1
        self.update_count(self.object_count)

    def reset_count(self):
        self.object_count = 0
        self.update_count(self.object_count)
        QMessageBox.information(self, "Count Reset", "The object count has been reset to 0.")

    def show_help(self):
        help_text = (
            "1. Click 'Capture Template' to select a template.\n"
            "2. In the template capture window, click and drag to draw a rectangle around the object.\n"
            "3. Click 'Start Detection' to begin object detection.\n"
            "4. Use ROI adjustment buttons to fine-tune the template position.\n"
            "5. Adjust the match threshold if needed.\n"
            "6. Click 'Count Object' when you want to increment the count.\n"
            "7. Click 'Stop' to end the detection process.\n"
            "8. Use 'Reset Count' to set the count back to 0."
        )
        QMessageBox.information(self, "Help", help_text)

    def update_threshold(self):
        value = self.threshold_slider.value() / 100
        self.threshold_label.setText(f"Match Threshold: {value:.2f}")
        self.result_display.set_match_threshold(value)

    def update_button_states(self):
        has_template = self.result_display.has_template()
        is_detecting = self.result_display.is_detecting()

        self.capture_template_button.setEnabled(not is_detecting)
        self.start_detection_button.setEnabled(has_template and not is_detecting)
        self.stop_button.setEnabled(is_detecting)
        self.count_button.setEnabled(is_detecting)
        self.reset_count_button.setEnabled(True)
        
        # # Enable/disable ROI adjustment buttons
        # roi_adjustable = has_template and not is_detecting
        # self.roi_up_button.setEnabled(roi_adjustable)
        # self.roi_down_button.setEnabled(roi_adjustable)
        # self.roi_left_button.setEnabled(roi_adjustable)
        # self.roi_right_button.setEnabled(roi_adjustable)

    def update_template_preview(self):
        template, _ = load_template()
        if template is not None:
            height, width = template.shape[:2]
            bytes_per_line = 3 * width
            q_img = QImage(template.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.template_preview.setPixmap(pixmap)
        else:
            self.template_preview.setText("No template")

    def update_count(self, count):
        self.object_count = count
        self.count_label.setText(f"Count: {self.object_count}")
        save_count(self.object_count)

    def adjust_roi(self, dx, dy):
        self.result_display.adjust_roi(dx, dy)
        self.update_template_preview()

    def closeEvent(self, event):
        save_count(self.object_count)
        self.result_display.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    print("MainWindow class defined successfully")

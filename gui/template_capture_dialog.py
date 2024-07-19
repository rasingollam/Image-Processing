# gui/template_capture_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QIcon
import os
import cv2
from camera_feed import CameraFeed
from template_capture import get_template_roi, cleanup_cv2_windows

class TemplateCaptureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Capture Template")
        
        # Set the icon
        icon_path = os.path.abspath('resources/app_icon.png')
        self.setWindowIcon(QIcon(icon_path))
        
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout(self)

        self.capture_button = QPushButton("Capture Template")
        self.layout.addWidget(self.capture_button)

        self.capture_button.clicked.connect(self.capture_template)

        self.camera = CameraFeed()
        self.camera.start()

    def capture_template(self):
        frame = self.camera.read_frame()
        if frame is not None:
            self.camera.stop()  # Stop the camera before opening OpenCV window
            success = get_template_roi(frame)
            cleanup_cv2_windows()  # Ensure all OpenCV windows are closed
            if success:
                QMessageBox.information(self, "Success", "Template captured successfully!")
                self.accept()
            else:
                QMessageBox.warning(self, "Warning", "Failed to capture template. Please try again.")
                self.camera.start()  # Restart the camera if capture failed
        else:
            QMessageBox.critical(self, "Error", "Failed to capture frame from camera.")

    def closeEvent(self, event):
        self.camera.stop()
        cleanup_cv2_windows()  # Ensure all OpenCV windows are closed
        super().closeEvent(event)

    def reject(self):
        self.camera.stop()
        cleanup_cv2_windows()  # Ensure all OpenCV windows are closed
        super().reject()

    def accept(self):
        self.camera.stop()
        cleanup_cv2_windows()  # Ensure all OpenCV windows are closed
        super().accept()

    def showEvent(self, event):
        super().showEvent(event)
        # Set the icon again after the dialog is shown
        icon_path = os.path.abspath('resources/app_icon.png')
        self.setWindowIcon(QIcon(icon_path))

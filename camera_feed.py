import cv2
from config import CAMERA_INDEX

class CameraFeed:
    def __init__(self):
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

    def read_frame(self):
        if self.cap is None:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __del__(self):
        self.stop()

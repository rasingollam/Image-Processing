# template_capture.py

import cv2
import numpy as np
from utils import save_template

def get_template_roi(frame):
    """
    Allow the user to select a region of interest (ROI) for the template.
    """
    window_name = "Select Template ROI"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, frame)
    roi = cv2.selectROI(window_name, frame, False)
    cv2.destroyWindow(window_name)
    
    if roi != (0, 0, 0, 0):
        template = frame[int(roi[1]):int(roi[1]+roi[3]), 
                         int(roi[0]):int(roi[0]+roi[2])]
        save_template(template)
        return True
    return False

def cleanup_cv2_windows():
    """
    Forcefully close all OpenCV windows.
    """
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)
    cv2.waitKey(1)

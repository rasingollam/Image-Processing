# visualization.py

import cv2
from config import BOUNDING_BOX_COLOR, BOUNDING_BOX_THICKNESS

def draw_bounding_box(frame, top_left, bottom_right):
    """
    Draw a bounding box on the frame.
    """
    cv2.rectangle(frame, top_left, bottom_right, BOUNDING_BOX_COLOR, BOUNDING_BOX_THICKNESS)

def add_text(frame, text, position):
    """
    Add text to the frame.
    """
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, BOUNDING_BOX_COLOR, 2)

def visualize_result(frame, detection_result):
    """
    Visualize the detection result on the frame.
    """
    if detection_result:
        top_left, bottom_right, match_val = detection_result
        draw_bounding_box(frame, top_left, bottom_right)
        add_text(frame, f"Match: {match_val:.2f}", (10, 30))
    else:
        add_text(frame, "No match found", (10, 30))

    return frame

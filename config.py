# config.py

import cv2

# Camera settings
CAMERA_INDEX = 0  # Use 0 for default webcam

# Template matching settings
MATCH_METHOD = cv2.TM_CCOEFF_NORMED
MATCH_THRESHOLD = 0.98  # Adjust this value based on your needs

# Visualization settings
BOUNDING_BOX_COLOR = (0, 255, 0)  # Green
BOUNDING_BOX_THICKNESS = 2

# File paths
TEMPLATE_DIR = "templates"
TEMPLATE_FILENAME = "template.jpg"

# GUI settings
WINDOW_TITLE = "Template Matching Application"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

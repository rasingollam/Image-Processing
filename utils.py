import cv2
import os
import json
import numpy as np

# Define constants
TEMPLATE_DIR = 'templates'
TEMPLATE_FILENAME = 'template.png'
TEMPLATE_INFO_FILENAME = 'template_info.json'
COUNT_FILE = 'object_count.json'

def ensure_dir(directory):
    """Ensure that a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_template(image, roi_coords):
    """Save the captured template image and ROI coordinates."""
    ensure_dir(TEMPLATE_DIR)
    image_path = os.path.join(TEMPLATE_DIR, TEMPLATE_FILENAME)
    info_path = os.path.join(TEMPLATE_DIR, TEMPLATE_INFO_FILENAME)
    
    cv2.imwrite(image_path, image)
    
    template_info = {
        'roi_coords': roi_coords
    }
    
    with open(info_path, 'w') as f:
        json.dump(template_info, f)

def load_template():
    """Load the saved template image and ROI coordinates."""
    image_path = os.path.join(TEMPLATE_DIR, TEMPLATE_FILENAME)
    info_path = os.path.join(TEMPLATE_DIR, TEMPLATE_INFO_FILENAME)
    
    if os.path.exists(image_path) and os.path.exists(info_path):
        template = cv2.imread(image_path)
        
        with open(info_path, 'r') as f:
            template_info = json.load(f)
        
        roi_coords = template_info.get('roi_coords')
        
        return template, roi_coords
    
    return None, None

def save_count(count):
    """Save the current object count to a JSON file."""
    with open(COUNT_FILE, 'w') as f:
        json.dump({'count': count}, f)

def load_count():
    """Load the object count from the JSON file."""
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            data = json.load(f)
            return data.get('count', 0)
    return 0

def template_exists():
    """Check if a template image and info exist."""
    image_path = os.path.join(TEMPLATE_DIR, TEMPLATE_FILENAME)
    info_path = os.path.join(TEMPLATE_DIR, TEMPLATE_INFO_FILENAME)
    return os.path.exists(image_path) and os.path.exists(info_path)

# def update_roi_coords(roi_coords):
#     """Update the ROI coordinates in the template info file."""
#     info_path = os.path.join(TEMPLATE_DIR, TEMPLATE_INFO_FILENAME)
    
#     if os.path.exists(info_path):
#         with open(info_path, 'r') as f:
#             template_info = json.load(f)
        
#         template_info['roi_coords'] = roi_coords
        
#         with open(info_path, 'w') as f:
#             json.dump(template_info, f)

def calculate_match_percentage(detection_result):
    """Calculate the match percentage from the detection result."""
    if detection_result is None:
        return 0.0
    _, _, match_val = detection_result
    return match_val * 100

def get_roi_from_template():
    """Get the ROI coordinates from the saved template info."""
    info_path = os.path.join(TEMPLATE_DIR, TEMPLATE_INFO_FILENAME)
    
    if os.path.exists(info_path):
        with open(info_path, 'r') as f:
            template_info = json.load(f)
        
        return template_info.get('roi_coords')
    
    return None

def resize_image(image, max_width=800, max_height=600):
    """Resize an image while maintaining aspect ratio."""
    height, width = image.shape[:2]
    
    if width > max_width or height > max_height:
        scale = min(max_width / width, max_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
    
    return image

import cv2
import numpy as np
from utils import load_template

def detect_object(frame, template=None):
    if template is None:
        template_data = load_template()
        if template_data is None or len(template_data) != 2:
            return None
        template, _ = template_data

    if template is None:
        return None

    # Ensure the template is not larger than the frame
    frame_height, frame_width = frame.shape[:2]
    template_height, template_width = template.shape[:2]

    if template_height > frame_height or template_width > frame_width:
        # Resize template to fit within the frame
        scale = min(frame_height / template_height, frame_width / template_width)
        new_width = int(template_width * scale)
        new_height = int(template_height * scale)
        template = cv2.resize(template, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Convert both to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if len(template.shape) == 3 else template

    # Perform template matching
    result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get the best match location
    top_left = max_loc
    bottom_right = (top_left[0] + template_gray.shape[1], top_left[1] + template_gray.shape[0])
    match_val = max_val

    return (top_left, bottom_right, match_val)

def multi_scale_detection(frame, threshold, scale_range=(0.5, 1.5), scale_steps=20):
    template_data = load_template()
    if template_data is None or len(template_data) != 2:
        return None
    template, _ = template_data

    if template is None:
        return None

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if len(template.shape) == 3 else template

    best_match = None
    best_scale = 1.0

    for scale in np.linspace(scale_range[0], scale_range[1], scale_steps):
        resized_template = cv2.resize(template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        
        if resized_template.shape[0] > frame.shape[0] or resized_template.shape[1] > frame.shape[1]:
            continue

        result = cv2.matchTemplate(frame_gray, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold and (best_match is None or max_val > best_match[2]):
            w, h = resized_template.shape[::-1]
            best_match = (max_loc, (max_loc[0] + w, max_loc[1] + h), max_val)
            best_scale = scale

    if best_match:
        return (*best_match, best_scale)
    else:
        return None

def detect_multiple_objects(frame, threshold, max_detections=5, non_max_suppression=True):
    template_data = load_template()
    if template_data is None or len(template_data) != 2:
        return None
    template, _ = template_data

    if template is None:
        return None

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if len(template.shape) == 3 else template

    result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    detections = list(zip(*locations[::-1]))

    if non_max_suppression:
        detections = non_max_suppression_fast(detections, 0.3)

    detections = detections[:max_detections]
    
    results = []
    for detection in detections:
        top_left = detection
        bottom_right = (top_left[0] + template_gray.shape[1], top_left[1] + template_gray.shape[0])
        match_val = result[detection[1], detection[0]]
        results.append((top_left, bottom_right, match_val))

    return results

def non_max_suppression_fast(boxes, overlapThresh):
    if len(boxes) == 0:
        return []

    boxes = np.array(boxes)
    pick = []

    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,0] + boxes[:,2]
    y2 = boxes[:,1] + boxes[:,3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]

        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")

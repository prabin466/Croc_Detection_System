import cv2

def annotator(frame, detections):
    """
    Draws a bounding box and label
    """
    for detection in detections:
        bbox = detection['bbox']
        label = detection['label']
        confidence = detection['confidence']
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(frame,(x1, y1), (x2, y2), color = (0,0,255), thickness = 2)
        cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return frame
import numpy as np
from croc_detector.annotator import annotator


def test_annotator_preserves_frame_shape():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = [{"bbox": [10, 10, 50, 50], "label": "crocodile", "confidence": 0.9}]
    result = annotator(frame, detections)
    assert result.shape == frame.shape


def test_annotator_returns_frame():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = [{"bbox": [10, 10, 50, 50], "label": "crocodile", "confidence": 0.9}]
    result = annotator(frame, detections)
    assert result is not None

def test_annotator_draws_bounding_box():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = [{"bbox": [10, 10, 50, 50], "label": "crocodile", "confidence": 0.9}]
    result = annotator(frame, detections)
    assert result.sum() >  0
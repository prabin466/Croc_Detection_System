from croc_detector.logger_config import setup_logger
from croc_detector.frame_processor import ImageExtractor
from croc_detector.frame_processor import VideoExtractor
from croc_detector.detector import CrocDetector
from croc_detector.annotator import annotator
from croc_detector.utils import timing
from croc_detector.config import SUPPORTED_IMAGES, SUPPORTED_VIDEOS, SNAPSHOTS_DIR
from pathlib import Path

import cv2
from datetime import datetime
import sys

logger = setup_logger(__name__)

@timing
def main(path):
    ext = Path(path).suffix.lower()

    if ext in SUPPORTED_IMAGES:
        extractor = ImageExtractor()

    elif ext in SUPPORTED_VIDEOS:
        extractor = VideoExtractor()

    else:
        raise ValueError(f"Unsupported file type:{ext}")

    detector = CrocDetector()

    for frame in extractor.extract(path):
        detections = detector.detect(frame)
        if detections:
            logger.info("Found %s detection(s) - confidence: %s", len(detections), [d['confidence'] for d in detections])
            for detection in detections:
                frame  = annotator(frame, detection)
            filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            snapshot_path = SNAPSHOTS_DIR / filename
            cv2.imwrite(str(snapshot_path), frame)
            logger.info("Snapshot saved: %s", snapshot_path)


if __name__ == "__main__":
    file_path = sys.argv[1]
    main(file_path)
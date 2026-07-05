from croc_detector.logger_config import setup_logger
from croc_detector.frame_processor import ImageExtractor, VideoExtractor
from croc_detector.detector import CrocDetector
from croc_detector.config import SUPPORTED_IMAGES, SUPPORTED_VIDEOS
from pathlib import Path

logger = setup_logger(__name__)

def process_file(path):
    extn = Path(path).suffix.lower()

    if extn in SUPPORTED_IMAGES:
        extractor = ImageExtractor()

    elif extn in SUPPORTED_VIDEOS:
        extractor = VideoExtractor()

    else:
        raise ValueError("Unsupported format, please input valid format.")

    detector = CrocDetector()

    for frame in extractor.extract(path):
        detections = detector.detect(frame)

        if detections:
            logger.debug("Found %s detection(s) - confidence: %s", len(detections), [d['confidence'] for d in detections])

        yield frame, detections



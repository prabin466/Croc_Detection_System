from croc_detector.logger_config import setup_logger
from croc_detector.frame_processor import ImageExtractor, VideoExtractor, StreamExtractor
from croc_detector.detector import CrocDetector
from croc_detector.config import SUPPORTED_IMAGES, SUPPORTED_VIDEOS, ALLOWED_STREAM_SCHEMES
from pathlib import Path

logger = setup_logger(__name__)

def process_file(path, extractor=None):
    if extractor is None:
        extractor = get_extractor(path)
    detector = CrocDetector()

    for frame in extractor.extract(path):
        detections = detector.detect(frame)

        if detections:
            logger.debug("Found %s detection(s) - confidence: %s", len(detections), [d['confidence'] for d in detections])

        yield frame, detections


def get_extractor(path):

    if str(path).startswith(ALLOWED_STREAM_SCHEMES):
        return StreamExtractor()
    extn = Path(path).suffix.lower()

    if extn in SUPPORTED_IMAGES:
        return ImageExtractor()

    elif extn in SUPPORTED_VIDEOS:
        return VideoExtractor()

    else:
        raise ValueError("Unsupported format, please input valid format.")

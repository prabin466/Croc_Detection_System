from croc_detector.logger_config import setup_logger
from croc_detector.utils import timing
from croc_detector.annotator import annotator
from croc_detector.config import SNAPSHOTS_DIR
from croc_detector.pipeline import process_file

import cv2
from datetime import datetime
import sys

logger = setup_logger(__name__)

@timing
def main(path):
    frames_with_detections = 0
    total_detections = 0
    
    for frame, detections in process_file(path):
        frame = annotator(frame, detections)

        if detections:
            frames_with_detections += 1
            total_detections += len(detections)
            filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            snapshot_path = SNAPSHOTS_DIR / filename
            cv2.imwrite(str(snapshot_path), frame)
            logger.debug("Snapshot saved: %s", snapshot_path)

    logger.info("Processing complete. Frames with detections: %d, Total detections: %d", frames_with_detections, total_detections)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Please provide a file path as an argument.")
        sys.exit(1)
    main(sys.argv[1])
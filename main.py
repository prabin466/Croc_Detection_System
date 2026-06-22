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
    for frame, detection in process_file(path):
        frame = annotator(frame, detection)

        if detection:
            filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            snapshot_path = SNAPSHOTS_DIR / filename
            cv2.imwrite(str(snapshot_path), frame)
            logger.info("Snapshot saved: %s", snapshot_path)


if __name__ == "__main__":
    file_path = sys.argv[1]
    main(file_path)
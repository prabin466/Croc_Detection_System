
from croc_detector.config import SUPPORTED_IMAGES, SUPPORTED_VIDEOS
from croc_detector.logger_config import setup_logger
from pathlib import Path
import cv2

<<<<<<< Updated upstream

from abc import ABC, abstractmethod

class BaseExtractor(ABC):

    def __init__(self):
        self.logger = setup_logger(__name__)

    @abstractmethod
    def extract(self, path):
        yield


class ImageExtractor(BaseExtractor):
    def extract(self, path):
        self.logger.info("Extracting image from path: %s", path)
        try:
            extns = Path(path).suffix.lower()

            if extns in SUPPORTED_IMAGES:
                self.logger.info("Image format %s is supported.", extns)
            
            else:
                self.logger.error("Unsupported image format: %s", extns)
                raise ValueError(f"Unsupported image format: {extns}")
            
            image = cv2.imread(path)
            if image is None:
                self.logger.error("Failed to read image from path: %s", path)
                raise ValueError(f"Failed to read image from path: {path}")
            
            else:
                self.logger.info("Image successfully read from path %s", path)
                yield image
        except Exception as e:
            self.logger.error("Error occurred while processing image %s: %s", path, e)
            raise   


class VideoExtractor(BaseExtractor):
    def extract(self, path):
        self.logger.info("Extracting video from path: %s", path)
        cap = None
        try:
            extns = Path(path).suffix.lower()

            if extns in SUPPORTED_VIDEOS:
                self.logger.info("Video format %s is supported.", extns)
            
            else:
                self.logger.error("Unsupported video format: %s", extns)
                raise ValueError(f"Unsupported video format: {extns}")
            
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                self.logger.error("Failed to open video from path: %s", path)
                raise ValueError(f"Failed to open video from path: {path}")
            
            else:
                self.logger.info("Video successfully opened from path %s", path)
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    yield frame
        except Exception as e:
            self.logger.error("Error occurred while processing video %s: %s", path, e)
            raise

        finally:
            if cap is not None and cap.isOpened():
                cap.release()
                self.logger.info("Video capture released for path: %s", path)
=======
logger = setup_logger(__name__)

def image_extract(image_path):
    logger.info("Extracting image from path: %s", image_path)

    try:
        extns = Path(image_path).suffix.lower()

        if extns in SUPPORTED_IMAGES:
            logger.info("Image format %s is supported.", extns)
        
        else:
            logger.error("Unsupported image format: %s", extns)
            raise ValueError(f"Unsupported image format: {extns}")
        
        image = cv2.imread(image_path)
        if image is None:
            logger.error("Failed to read image from path: %s", image_path)
            raise ValueError(f"Failed to read image from path: {image_path}")
        
        else:
            logger.info("Image successfully read from path %s", image_path)
            yield image
    except Exception as e:
        logger.error("Error occurred while processing image %s: %s", image_path, e)
        raise


def video_extract(video_path):
    logger.info("Extracting video from path: %s", video_path)
    cap = None #

    try:
        extns = Path(video_path).suffix.lower()

        if extns in SUPPORTED_VIDEOS:
            logger.info("Video format %s is supported.", extns)
        
        else:
            logger.error("Unsupported video format: %s", extns)
            raise ValueError(f"Unsupported video format: {extns}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error("Failed to open video from path: %s", video_path)
            raise ValueError(f"Failed to open video from path: {video_path}")
        
        else:
            logger.info("Video successfully opened from path %s", video_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                yield frame
    except Exception as e:
        logger.error("Error occurred while processing video %s: %s", video_path, e)
        raise
    
    finally:
        if cap is not None and cap.isOpened():
            cap.release()
            logger.info("Video capture released for path: %s", video_path)


>>>>>>> Stashed changes

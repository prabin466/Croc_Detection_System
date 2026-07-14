import threading
import time
from croc_detector.logger_config import setup_logger
import cv2


from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """
    Abstract base class for extracting frames
    """

    def __init__(self):
        self.logger = setup_logger(__name__)

    @abstractmethod
    def extract(self, path):
        yield


class ImageExtractor(BaseExtractor):

    def extract(self, path):
        self.logger.info("Extracting image from path: %s", path)
        try:
            image = cv2.imread(path)
            if image is None:
                self.logger.error("Failed to read image from path: %s", path)
                raise ValueError(f"Failed to read image from path: {path}")
            
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
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                self.logger.error("Failed to open video from path: %s", path)
                raise ValueError(f"Failed to open video from path: {path}")
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


class StreamExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()
        self.latest_frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None
        self.cap = None
        self.frame_id = 0

    def _read_loop(self, cap):
        while self.running:
            ret, frame = cap.read()
            if not ret:
                self.logger.warning("Failed to read frame from stream")
                time.sleep(0.1)
                continue
            with self.lock:
                self.latest_frame = frame
                self.frame_id += 1

    def get_latest_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None, 0
            return self.latest_frame.copy(), self.frame_id

    def get_frame_id(self):
        with self.lock:
            return self.frame_id

    def start_stream(self, source):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            self.logger.error("Failed to open stream from source: %s", source)
            self.cap.release()
            raise ValueError(f"Failed to open stream from source: {source}")
        self.logger.info("Stream successfully opened from source %s", source)
        self.running = True
        self.thread = threading.Thread(target=self._read_loop, args=(self.cap,), daemon=True)
        self.thread.start()

    def stop_stream(self):
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=2.0)
            self.thread = None
        if self.cap is not None:
            self.cap.release()
            self.logger.info("Stream capture released")
            self.cap = None

    def extract(self, path):
        last_id = 0
        self.start_stream(path)
        try:
            while self.running:
                if self.get_frame_id() != last_id:
                    frame, last_id = self.get_latest_frame()
                    if frame is not None:
                        yield frame
                else:
                    time.sleep(0.001)
        finally:
            self.stop_stream()
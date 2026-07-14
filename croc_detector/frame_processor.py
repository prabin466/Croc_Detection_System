import threading
import time
import cv2
from enum import Enum
from abc import ABC, abstractmethod
from croc_detector.logger_config import setup_logger

STREAM_TIMEOUT_SECONDS = 5.0
RECONNECT_BACKOFF_INITIAL = 1.0
RECONNECT_BACKOFF_MAX = 10.0



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



class StreamState(Enum):
    STOPPED = "stopped"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"


class StreamExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()
        self.latest_frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None
        self.cap = None
        self.frame_id = 0
        self.state = StreamState.STOPPED
        self.path = None
        self.stop_event = threading.Event()

    def _read_loop(self, cap):
        last_success = time.time()
        while self.running:
            ret, frame = cap.read()
            if ret:
                with self.lock:
                    self.latest_frame = frame
                    self.frame_id += 1
                last_success = time.time()
                self.state = StreamState.CONNECTED
                continue

            if time.time() - last_success > STREAM_TIMEOUT_SECONDS:
                cap = self._reconnect(self.path)
                if cap is None:
                    return
                last_success = time.time()
                continue
            time.sleep(0.1)

    def get_latest_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None, 0
            return self.latest_frame.copy(), self.frame_id

    def get_frame_id(self):
        with self.lock:
            return self.frame_id

    def start_stream(self, path):
        self.path = path
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            self.logger.error("Failed to open stream from path: %s", path)
            self.cap.release()
            raise ValueError(f"Failed to open stream from path: {path}")
        self.logger.info("Stream successfully opened from path %s", path)
        self.running = True
        self.thread = threading.Thread(target=self._read_loop, args=(self.cap,), daemon=True)
        self.stop_event.clear()
        self.thread.start()

    def stop_stream(self):
        self.running = False
        self.stop_event.set()
        self.state = StreamState.STOPPED
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


    def _reconnect(self, path):
        backoff = RECONNECT_BACKOFF_INITIAL
        self.state = StreamState.RECONNECTING
        self.logger.info("Attempting to reconnect to stream: %s", path)
        if self.cap is not None:
            self.cap.release()
        while self.running:
            self.cap = cv2.VideoCapture(path)
            if self.cap.isOpened():
                self.logger.info("Reconnected to stream: %s", path)
                self.state = StreamState.CONNECTED
                return self.cap
            else:
                self.logger.warning("Failed to reconnect to stream: %s, retrying...", path)
                self.cap.release()
                if self.stop_event.wait(backoff):
                    self.logger.info("Stop event set, aborting reconnection attempts.")
                    return None 
                backoff = min(backoff * 2, RECONNECT_BACKOFF_MAX)

        return None

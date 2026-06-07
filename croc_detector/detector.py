from ultralytics import YOLO
from croc_detector.config import MODEL_NAME, CONFIDENCE_THRESHOLD
from croc_detector.logger_config import setup_logger

class CrocDetector:
    """
    Detector class for identifying crocodiles in images and video frames using a YOLO model.
    """
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.model = YOLO(MODEL_NAME)
        self.confidence_threshold = CONFIDENCE_THRESHOLD
        self.logger.info("CrocDetector initialized with model: %s", MODEL_NAME)


    def detect(self, frame):
        self.logger.info("Detecting crocodiles in the image frame.")
       
        results = self.model(frame, conf=self.confidence_threshold)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = box.conf.item()
                label = self.model.names[int(box.cls)]
                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence,
                    "label": label
                })
                self.logger.debug("Detection: bbox=%s, confidence=%.2f, label=%s", [x1, y1, x2, y2], confidence, label)
                
        self.logger.info("Found %d detection(s)", len(detections))
        return detections

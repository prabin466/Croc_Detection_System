from ultralytics import YOLO
from croc_detector.config import BASE_MODEL, BASE_DIR
from croc_detector.logger_config import setup_logger

logger = setup_logger(__name__)
dataset_path = BASE_DIR/'dataset_combined'/ 'data.yaml'

def main():
    model = YOLO(BASE_MODEL)

    logger.info("Training Started")
    model.train(data = str(dataset_path),epochs = 100, device = 0, imgsz = 640, patience = 20, batch = -1)
    logger.info('Training finished')


if __name__ == "__main__":
    main()
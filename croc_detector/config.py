from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / 'logs'
SNAPSHOTS_DIR = BASE_DIR / 'snapshots'
UPLOADS_DIR = BASE_DIR / 'uploads'

MODEL_NAME = 'yolov8n.pt'
CONFIDENCE_THRESHOLD = 0.5

SUPPORTED_IMAGES = ['.jpg', '.jpeg', '.png']
SUPPORTED_VIDEOS = ['.mp4', '.avi', '.mov']

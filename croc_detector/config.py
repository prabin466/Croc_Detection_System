from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / 'logs'
SNAPSHOTS_DIR = BASE_DIR / 'snapshots'
UPLOADS_DIR = BASE_DIR / 'uploads'

BASE_MODEL = 'yolov8n.pt'
MODEL_NAME = BASE_DIR / 'models' / 'croc_yolov8n.pt'
CONFIDENCE_THRESHOLD = 0.5

SUPPORTED_IMAGES = ['.jpg', '.jpeg', '.png']
SUPPORTED_VIDEOS = ['.mp4', '.avi', '.mov']

TARGET_CLASSES = ['crocodile']

ALLOWED_STREAM_SCHEMES = ('http://', 'https://', 'rtsp://', 'rtsps://')
ALLOW_LOCAL_SOURCES = os.environ.get('ALLOW_LOCAL_SOURCES', 'false').lower() == 'true'
for directory in [LOGS_DIR, SNAPSHOTS_DIR, UPLOADS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
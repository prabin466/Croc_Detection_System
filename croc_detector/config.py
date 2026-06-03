from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / 'logs'
SNAPSHOTS_DIR = BASE_DIR / 'snapshots'


SUPPORTED_IMAGES = ['.jpg', '.jpeg', '.png']
SUPPORTED_VIDEOS = ['.mp4', '.avi', '.mov']

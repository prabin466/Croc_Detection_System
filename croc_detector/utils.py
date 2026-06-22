import time
from croc_detector.logger_config import setup_logger

logger = setup_logger(__name__)

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = end - start
        logger.info("%s took %.2f seconds", func.__name__, duration)
        return result
    return wrapper


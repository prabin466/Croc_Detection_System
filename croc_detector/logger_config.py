import logging
import logging.config
from croc_detector.config import LOGS_DIR

LOGGING_CONFIG = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'default':{
            'format': '[%(asctime)s] %(levelname)s in %(module)s - %(funcName)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': logging.DEBUG,
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': logging.DEBUG,
            'filename': f'{LOGS_DIR}/croc_detector.log',
            'mode': 'a',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': logging.DEBUG,
    },
}

_configured  = False

def setup_logger(name: str) -> logging.Logger:
    global _configured
    if not _configured:
        logging.config.dictConfig(LOGGING_CONFIG)
        _configured = True
    return logging.getLogger(name)
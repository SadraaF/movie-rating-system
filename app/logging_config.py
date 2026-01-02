"""
Configuration module for application-wide logging.
Sets up console and rotating file handlers.
"""

import logging.config
import sys
from pathlib import Path

# Create a logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "logs/app.log",  # <--- This is your "فایل لاگ"
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"], # <--- Add "file" here
            "level": "INFO",
            "propagate": True,
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
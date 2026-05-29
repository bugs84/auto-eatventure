"""
logger.py - Centralized logging configuration

Configures Python's logging module with:
- Console handler: prints to stdout (default level: INFO)
- File handler: writes to logs/ directory with daily rotation

Configuration via environment variables:
- LOG_LEVEL: console log level (default "INFO")
- LOG_FILE_LEVEL: file log level (default "DEBUG")
- LOG_MAX_DAYS: days to keep rotated log files (default 7)
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "autoplay.log")

# Format for console: match previous print() style
CONSOLE_FORMAT = "%(message)s"
# Format for file: include timestamp, level, module
FILE_FORMAT = (
  "%(asctime)s [%(levelname)-5s] %(name)s: %(message)s")


def setup_logging():
  """Initialize logging with console and file handlers.

  Call once at application startup (before any logger usage).
  """
  console_level = os.getenv("LOG_LEVEL", "INFO").upper()
  file_level = os.getenv("LOG_FILE_LEVEL", "DEBUG").upper()
  max_days = int(os.getenv("LOG_MAX_DAYS", "7"))

  os.makedirs(LOG_DIR, exist_ok=True)

  root = logging.getLogger()
  root.setLevel(logging.DEBUG)

  # Remove existing handlers (avoid duplicates on re-init)
  root.handlers.clear()

  # Console handler
  console_handler = logging.StreamHandler()
  console_handler.setLevel(getattr(logging, console_level,
                                   logging.INFO))
  console_handler.setFormatter(
    logging.Formatter(CONSOLE_FORMAT))
  root.addHandler(console_handler)

  # File handler with daily rotation
  file_handler = TimedRotatingFileHandler(
    LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=max_days,
    encoding="utf-8")
  file_handler.setLevel(getattr(logging, file_level,
                                logging.DEBUG))
  file_handler.setFormatter(logging.Formatter(FILE_FORMAT))
  file_handler.suffix = "%Y-%m-%d"
  root.addHandler(file_handler)


def get_logger(name):
  """Get a named logger for a module.

  Usage:
    from logger import get_logger
    log = get_logger(__name__)
    log.info("Something happened")
  """
  return logging.getLogger(name)

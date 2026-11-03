"""Logging to the console and to rotated files in logs/.

- Console: INFO and up by default
- logs/autoplay.log: everything (DEBUG) by default - what the bot found
  on the screen, where it tapped - for the analysis of a problem; a new
  file every LOG_FILE_MB, the full ones gzipped, all of them together
  at most max_mb (the oldest deleted)
- logs/key_events.log: key milestones only, via key_log (no console),
  rotated daily, kept for key_log_max_days
- Uncaught exceptions (crashes) and the end of the bot (Ctrl+C,
  closed console window, kill) go to both log files
"""

import glob
import gzip
import logging
import os
import shutil
import signal
import sys
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'autoplay.log')
KEY_EVENTS_FILE = os.path.join(LOG_DIR, 'key_events.log')
# Size of logs/autoplay.log before it is gzipped and a new one started
# (gzip makes it ~15x smaller)
LOG_FILE_MB = 10
MB = 1024 * 1024

CONSOLE_FORMAT = '%(message)s'
# The module, function and line of the log call; the taps and searches
# (android/device.py, vision/screen.py) name the bot code calling them
FILE_FORMAT = ('%(asctime)s [%(levelname)-5s] '
               '%(module)s.%(funcName)s:%(lineno)d: %(message)s')
KEY_EVENTS_FORMAT = '%(asctime)s  %(message)s'

# Key milestones only (start, level changes, collected rewards,
# errors); details go to autoplay.log
key_log = logging.getLogger('key_events')
key_log.propagate = False


def setup_logging(console_level, file_level, max_mb, key_log_max_days):
  """Set up the handlers. Call once at start, before logging."""
  os.makedirs(LOG_DIR, exist_ok=True)
  # CRITICAL: the game was stuck and had to be restarted (stale.py)
  logging.addLevelName(logging.CRITICAL, 'FATAL')
  # Pillow logs each PNG chunk of every screenshot at DEBUG
  logging.getLogger('PIL').setLevel(logging.INFO)

  root = logging.getLogger()
  root.setLevel(logging.DEBUG)
  root.handlers.clear()

  console = logging.StreamHandler()
  console.setLevel(_level(console_level, logging.INFO))
  console.setFormatter(logging.Formatter(CONSOLE_FORMAT))
  root.addHandler(console)

  _compress_and_trim(LOG_FILE, max_mb * MB)
  file_handler = _CompressingFileHandler(LOG_FILE, max_mb * MB)
  file_handler.setLevel(_level(file_level, logging.DEBUG))
  file_handler.setFormatter(logging.Formatter(FILE_FORMAT))
  root.addHandler(file_handler)

  key_log.setLevel(logging.INFO)
  key_log.handlers.clear()
  key_handler = TimedRotatingFileHandler(
    KEY_EVENTS_FILE, when='midnight', interval=1,
    backupCount=key_log_max_days, encoding='utf-8')
  key_handler.suffix = '%Y-%m-%d'
  key_handler.setFormatter(logging.Formatter(KEY_EVENTS_FORMAT))
  key_log.addHandler(key_handler)

  sys.excepthook = _log_crash
  # Closed console window (SIGHUP, not on Windows) and kill (SIGTERM)
  # end the bot without an exception
  for name in ('SIGTERM', 'SIGHUP'):
    if hasattr(signal, name):
      signal.signal(getattr(signal, name), _log_stop)


def _level(name, default):
  return getattr(logging, name.upper(), default)


class _CompressingFileHandler(RotatingFileHandler):
  """A log file renamed to <file>.<date_time> when it reaches
  LOG_FILE_MB, then gzipped; the oldest of them are deleted so that
  all the files take at most max_bytes."""

  def __init__(self, path, max_bytes):
    super().__init__(path, maxBytes=LOG_FILE_MB * MB, encoding='utf-8')
    self._max_bytes = max_bytes

  def doRollover(self):
    if self.stream:
      self.stream.close()
      self.stream = None
    os.rename(self.baseFilename,
              f'{self.baseFilename}.{time.strftime("%Y-%m-%d_%H%M%S")}')
    _compress_and_trim(self.baseFilename, self._max_bytes)
    self.stream = self._open()


def _compress_and_trim(path, max_bytes):
  """Gzip the rotated files of the log (also the daily ones of older
  versions of the bot), then delete the oldest of them while they and
  a full log take more than max_bytes."""
  for rotated in glob.glob(glob.escape(path) + '.*'):
    if not rotated.endswith('.gz'):
      _gzip(rotated)
  # The names end with the date (and time): sorted from the oldest
  rotated = sorted(glob.glob(glob.escape(path) + '.*.gz'))
  total = LOG_FILE_MB * MB + sum(map(os.path.getsize, rotated))
  while rotated and total > max_bytes:
    oldest = rotated.pop(0)
    total -= os.path.getsize(oldest)
    os.remove(oldest)


def _gzip(path):
  with open(path, 'rb') as source, gzip.open(
      path + '.gz', 'wb', compresslevel=6) as target:
    shutil.copyfileobj(source, target)
  shutil.copystat(path, path + '.gz')
  os.remove(path)


def _log_stop(signum, _frame):
  """Log the end of the bot by a signal, then exit."""
  _log_end(signal.Signals(signum).name)
  sys.exit(0)


def _log_end(reason):
  logging.getLogger(__name__).info('Bot stopped (%s)', reason)
  key_log.info('STOP - Bot stopped (%s)', reason)


def _log_crash(exc_type, exc_value, exc_traceback):
  """Log an uncaught exception, e.g. when the phone gets
  disconnected.

  Without this its traceback goes only to the console window. The full
  traceback goes to autoplay.log, one short line to key_events.log.
  Ctrl+C is logged as the end of the bot, not as a crash.
  """
  if issubclass(exc_type, KeyboardInterrupt):
    _log_end('Ctrl+C')
    return
  logging.getLogger(__name__).error(
    'Bot crashed', exc_info=(exc_type, exc_value, exc_traceback))
  key_log.error('ERROR - Bot crashed: %s, see autoplay.log',
                exc_type.__name__)

"""FastInput: taps sent through a monkey server on the phone.

Android's `input` command starts a Java VM for every tap, which takes
over 1 s on older phones (Android 9). `monkey --port` is started once
and then takes the touches as lines of text over a socket (~0.05 s
each).
"""

import logging
import time

from adbutils import AdbError, Network

log = logging.getLogger(__name__)

# TCP port on the phone the monkey server listens on
MONKEY_PORT = 1080
# The server's Java VM takes ~2 s to start
SERVER_START_TRIES = 40
SERVER_START_RETRY_DELAY_S = 0.25
REPLY_TIMEOUT_S = 10


class FastInput:
  """Touches through the monkey server, (re)connected when needed."""

  def __init__(self, adb_device):
    self._adb = adb_device
    self._server = None
    self._lines = None

  def tap(self, point):
    self._send(f'touch down {point.x} {point.y}',
               f'touch up {point.x} {point.y}')

  def long_press(self, point, duration_ms):
    self._send(f'touch down {point.x} {point.y}')
    time.sleep(duration_ms / 1000)
    self._send(f'touch up {point.x} {point.y}')

  def _send(self, *commands):
    """Send the commands; after a lost connection once more."""
    try:
      self._send_once(commands)
    except (OSError, AdbError) as error:
      log.warning('Monkey server failed (%s), connecting again', error)
      self._lines = None
      self._send_once(commands)

  def _send_once(self, commands):
    if self._lines is None:
      self._lines = self._connect()
    for command in commands:
      self._lines.write(command + '\n')
      self._lines.flush()
      reply = self._lines.readline().strip()
      if reply != 'OK':
        raise OSError(f'monkey replied {reply!r} to {command!r}')

  def _connect(self):
    """Connect to the server, started first when it does not run (one
    left by a previous run of the bot is used again)."""
    try:
      return self._open_socket()
    except AdbError:
      log.info('Starting the monkey server on the phone')
    # The server runs as long as this shell connection is kept
    self._server = self._adb.shell(
      f'monkey --port {MONKEY_PORT}', stream=True)
    for _ in range(SERVER_START_TRIES):
      time.sleep(SERVER_START_RETRY_DELAY_S)
      try:
        return self._open_socket()
      except AdbError:
        pass
    raise OSError('the monkey server did not start')

  def _open_socket(self):
    connection = self._adb.create_connection(Network.TCP, MONKEY_PORT)
    connection.settimeout(REPLY_TIMEOUT_S)
    return connection.makefile('rw', newline='\n')

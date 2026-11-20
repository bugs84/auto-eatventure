"""Device: the phone over ADB (taps, swipes, screenshots, app start)."""

import io
import logging
import re
import subprocess
import sys
import time

import numpy as np
from adbutils import adb
from PIL import Image

from auto_eatventure.android.fast_input import FastInput

log = logging.getLogger(__name__)

GAME_PACKAGE = 'com.hwqgrhhjfd.idlefastfood'
# The game's own window (the restaurant, its dialogs); its ads have
# other activities in its package
GAME_ACTIVITY = 'com.singular.unitybridge.SingularUnityActivity'
# A failed screenshot (the phone was shortly disconnected, adb exit
# status 255; a broken PNG) is retried this many times before the bot
# crashes
SCREENSHOT_TRIES = 5
SCREENSHOT_RETRY_DELAY_S = 5
# An `input` command slower than this starts a Java VM each time (1.3-
# 1.6 s on Android 9; ~0.1 s where it is run by the system server):
# the taps then go through FastInput
SLOW_INPUT_S = 0.5


class Device:
  """The Android phone the game runs on."""

  def __init__(self, serial='', fast_input='0'):
    """Connect to the phone with this serial, else the first one.

    fast_input: "1" = taps and long presses go through FastInput
    instead of the `input` command, "0" = never, "auto" = when `input`
    is slow on this phone.
    """
    self._adb = self._connect(serial)
    self._fast_input = (
      FastInput(self._adb) if self._wants_fast_input(fast_input) else None)

  @staticmethod
  def _connect(serial):
    if serial:
      return adb.device(serial=serial)
    devices = adb.device_list()
    if not devices:
      raise RuntimeError(
        'No ADB devices connected. '
        'Connect your phone and enable USB Debugging.')
    log.warning('No device_serial in .env — '
                'using first connected device: %s', devices[0].serial)
    return devices[0]

  def _wants_fast_input(self, setting):
    if setting == 'auto':
      start = time.monotonic()
      # Without arguments it only prints its usage
      self._adb.shell('input')
      input_s = time.monotonic() - start
      setting = '1' if input_s > SLOW_INPUT_S else '0'
      log.info('The `input` command takes %.2f s', input_s)
    log.info('Fast input (monkey server): %s',
             'enabled' if setting == '1' else 'disabled')
    return setting == '1'

  @property
  def serial(self):
    return self._adb.serial

  def screen_size(self):
    """Return (width, height) of the screen in pixels."""
    output = self._adb.shell('wm size')
    # "Physical size: 1220x2712", maybe also "Override size: ..."
    match = re.search(r'(\d+)x(\d+)', output)
    if not match:
      raise RuntimeError(
        f"Could not parse resolution from 'wm size' output: {output!r}")
    return int(match.group(1)), int(match.group(2))

  def screenshot(self):
    """Return the screen as a BGR image (numpy array)."""
    for _ in range(SCREENSHOT_TRIES - 1):
      try:
        return self._screenshot()
      except (subprocess.CalledProcessError, OSError) as error:
        log.warning('Screenshot failed (%s), retrying in %d s',
                    error, SCREENSHOT_RETRY_DELAY_S)
        time.sleep(SCREENSHOT_RETRY_DELAY_S)
    return self._screenshot()

  def _screenshot(self):
    if sys.platform == 'win32':
      # Kept from the original code: older adb versions on Windows
      # turned \n into \r\n (untested with current adb)
      png = subprocess.check_output(
        ['adb', '-s', self.serial, 'shell', 'screencap', '-p'])
      png = png.replace(b'\r\n', b'\n')
    else:
      png = subprocess.check_output(
        ['adb', '-s', self.serial, 'exec-out', 'screencap', '-p'])
    rgb = Image.open(io.BytesIO(png)).convert('RGB')
    return np.array(rgb)[:, :, ::-1].copy()

  # The taps, swipes and app starts are logged (DEBUG) with the bot code
  # calling them (stacklevel=2), to analyze what the bot did

  def tap(self, point):
    """Tap the point."""
    log.debug('Tap (%d, %d)', *point, stacklevel=2)
    if self._fast_input:
      self._fast_input.tap(point)
    else:
      self._adb.shell(f'input tap {point.x} {point.y}')

  def long_press(self, point, duration_ms):
    """Hold a finger on the point (a swipe that doesn't move)."""
    log.debug('Long press (%d, %d) for %d ms', *point, duration_ms,
              stacklevel=2)
    if self._fast_input:
      self._fast_input.long_press(point, duration_ms)
    else:
      self._adb.shell(f'input swipe {point.x} {point.y} '
                      f'{point.x} {point.y} {duration_ms}')

  def swipe(self, swipe):
    """Swipe along a coords.geometry.Swipe."""
    log.debug('Swipe (%d, %d) -> (%d, %d)', *swipe.start, *swipe.end,
              stacklevel=2)
    self._adb.swipe(swipe.start.x, swipe.start.y,
                    swipe.end.x, swipe.end.y)

  def start_app(self):
    """Launch the game, or bring it to the foreground.

    It does not restart a running game (that needs close_app()).
    The screen is woken first and the lock screen dismissed (without a
    PIN): after the game crashes, the phone goes to sleep.
    """
    log.debug('Start the game / bring it to the foreground', stacklevel=2)
    self._adb.shell('input keyevent KEYCODE_WAKEUP')
    self._adb.shell('wm dismiss-keyguard')
    self._adb.shell(f'monkey -p {GAME_PACKAGE} '
                    '-c android.intent.category.LAUNCHER 1')

  def close_app(self):
    """Force-stop the game."""
    log.debug('Force-stop the game', stacklevel=2)
    self._adb.shell(f'am force-stop {GAME_PACKAGE}')

  def focused_window(self):
    """The window in front: "<package>/<activity>" (e.g. the game's
    GAME_ACTIVITY, or an ad's activity in the game's package), '' when
    unknown (e.g. the screen is off)."""
    output = self._adb.shell('dumpsys window | grep mCurrentFocus')
    # "mCurrentFocus=Window{19279cb u0 <package>/<activity>}"
    match = re.search(r'mCurrentFocus=Window\{\S+ \S+ ([^}\s]+)\}', output)
    window = match.group(1) if match else ''
    log.debug('Window in front: %s', window or output.strip(),
              stacklevel=2)
    return window

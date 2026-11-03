"""Stale game: nothing to upgrade for many loops."""

import glob
import logging
import os
import time

import cv2

from auto_eatventure.actions import popups, race_reward, start_dialogs
from auto_eatventure.android.device import GAME_ACTIVITY, GAME_PACKAGE
from auto_eatventure.logger import LOG_DIR, key_log

log = logging.getLogger(__name__)

# Loops without a station to upgrade before the game is brought to the
# foreground (e.g. an ad or a dialog may block it)
RECOVERY_LOOPS = 50
# Loops without a station to upgrade before the restaurant is scrolled
# to search for stations, then every SEARCH_SWIPE_EVERY loops
SEARCH_SWIPE_LOOPS = 15
SEARCH_SWIPE_EVERY = 5
# Number of consecutive swipes in the same direction before reversing.
# Kept high enough that repeats * swipe distance (650px) still covers
# the same total travel as the old single 1285px swipe used to, so a
# full stale-swipe cycle still reaches the top/bottom of a tall level.
SWIPES_PER_DIRECTION = 7
# Red X popups closed at most when recovering (stacked dialogs)
RECOVERY_POPUP_CLOSE_TRIES = 3
# Recoveries in a row without a station upgrade between them after
# which the game is restarted (~25 min). Waiting for coins took at most
# 7-8 recoveries in 3 weeks of logs (a restart doesn't hurt it), a
# stuck game 16 to 280 (the night of 2026-10-24).
RESTART_RECOVERIES = 6
# Wait after a recovery before checking the window in front: the game
# showed its ad again 3 s after it was brought to the foreground
# (2026-11-03), then it is restarted at once
FRONT_CHECK_DELAY_S = 4
# Wait between closing the game and starting it again
RESTART_PAUSE_S = 3
# Screenshots of a stuck game kept in logs/ (stuck_<date_time>.png)
STUCK_SCREENSHOTS_KEPT = 10


class StaleWatch:
  """Counts the loops without a station to upgrade and acts on them."""

  def __init__(self):
    self.idle_loops = 0
    self._swipes = 0
    # Recoveries in a row without a station upgrade
    self._recoveries = 0

  def found_work(self):
    self.idle_loops = 0
    self._recoveries = 0

  def found_nothing(self):
    self.idle_loops += 1

  def reset(self):
    """Start over, e.g. on a new level."""
    self.idle_loops = 0
    self._swipes = 0
    self._recoveries = 0

  def check(self, game):
    """Recover the game or scroll the restaurant when idle too long.
    Returns True when the game was restarted (_restart()).

    Recovery happens once per RECOVERY_LOOPS idle loops, not on every
    loop until something can be upgraded.
    """
    if self.idle_loops > RECOVERY_LOOPS:
      self.idle_loops = 0
      if self._recover(game):
        return True
    if (self.idle_loops >= SEARCH_SWIPE_LOOPS
        and self.idle_loops % SEARCH_SWIPE_EVERY == 0):
      self._search_swipe(game)
    return False

  def _recover(self, game):
    """Bring the game to the foreground and close blocking dialogs.
    Returns True when that didn't help and the game was restarted.

    start_app() only brings the running game to the foreground; it is
    restarted (_restart()) when it shows another window of its own
    (an ad it shows again, 2026-11-03) or after RESTART_RECOVERIES
    recoveries in a row.
    """
    log.warning('Nothing to update for %d loops — bringing game to '
                'foreground.', self.idle_loops)
    key_log.info('STALE - Nothing to update, bringing game to foreground')
    game.device.start_app()
    time.sleep(1)
    # A dialog may block the game, e.g. one that came late at start or
    # "Restaurant Race ended!" (no X)
    game.screen.capture()
    race_reward.claim(game)
    for _ in range(RECOVERY_POPUP_CLOSE_TRIES):
      if not popups.close_popup(game):
        break
      # The race dialog may have been under the closed popup
      race_reward.claim(game)
    game.device.tap(game.null_spot)
    time.sleep(1)
    self._recoveries += 1
    time.sleep(FRONT_CHECK_DELAY_S)
    window = game.device.focused_window()
    if _is_other_game_window(window):
      self._restart(game, f'its window {window} is in front after '
                    'bringing it to the foreground')
      return True
    if self._recoveries >= RESTART_RECOVERIES:
      self._restart(game, f'nothing to update after {self._recoveries} '
                    'recoveries in a row')
      return True
    return False

  def _restart(self, game, reason):
    """Close the game and start it again: it is stuck (e.g. an ad
    that comes back), which should not happen."""
    game.screen.capture()
    screenshot = _save_screenshot(game)
    log.critical('!!! GAME STUCK - %s. Restarting the game. This should '
                 'not happen: find out why (screenshot %s, this log '
                 'above) !!!', reason, screenshot)
    key_log.critical('FATAL - GAME STUCK (%s), restarting the game. This '
                     'should not happen, see %s and autoplay.log',
                     reason, screenshot)
    game.device.close_app()
    time.sleep(RESTART_PAUSE_S)
    game.device.start_app()
    start_dialogs.wait_until_ready(game)
    self._recoveries = 0

  def _search_swipe(self, game):
    """Scroll the restaurant down, later up, to search for stations."""
    cycle_position = self._swipes % (SWIPES_PER_DIRECTION * 2)
    if cycle_position < SWIPES_PER_DIRECTION:
      swipe = game.coords.swipe_down
    else:
      swipe = game.coords.swipe_up
    log.info('Stale swipe — scrolling to find items')
    game.device.swipe(swipe)
    time.sleep(3)
    self._swipes += 1


def _is_other_game_window(window):
  """Whether the window in front is the game's, but not the restaurant
  (GAME_ACTIVITY): e.g. its ad."""
  return (window.startswith(GAME_PACKAGE + '/')
          and window != f'{GAME_PACKAGE}/{GAME_ACTIVITY}')


def _save_screenshot(game):
  """Save the last screenshot to logs/ (the newest
  STUCK_SCREENSHOTS_KEPT are kept). Returns its path."""
  path = os.path.join(
    LOG_DIR, f'stuck_{time.strftime("%Y-%m-%d_%H%M%S")}.png')
  cv2.imwrite(path, game.screen.bgr)
  saved = sorted(glob.glob(os.path.join(LOG_DIR, 'stuck_*.png')))
  for old in saved[:-STUCK_SCREENSHOTS_KEPT]:
    os.remove(old)
  return path

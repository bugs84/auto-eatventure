"""Null spot: an empty spot on the restaurant tapped to close station
popups, placed just below the top bar."""

import logging

from auto_eatventure.actions import start_dialogs
from auto_eatventure.logger import key_log
from auto_eatventure.coords.geometry import Point
from auto_eatventure.vision.top_bar import find_top_bar_line

log = logging.getLogger(__name__)


def place_below_top_bar(game):
  """Place the null spot just below the top bar's black line and align
  the positions of coords/reference.py to the line.

  Called once at start. The status bar height differs between phones,
  so the spot can't be derived from the resolution. If the line is not
  found, the fallback from coords/reference.py stays, the positions
  stay as at the reference and an ERROR is logged.
  """
  # The dimming check looks at the settings gear, a Top position: align
  # to the line first, else the gear is looked for too low (LG G6: 100
  # px) and the screen always seems dimmed (in a dark place). A dimmed
  # screen keeps the line black: it is found or not, never misplaced.
  line_y = _find_line(game)
  if line_y is not None:
    game.coords.align_to_top_bar(line_y)
  if start_dialogs.close_dimming_dialogs(game):
    line_y = _find_line(game) or line_y
  if line_y is None:
    _log_fallback(game, 'no black line in the top band')
    return
  game.coords.align_to_top_bar(line_y)
  game.null_spot = Point(
    game.null_spot.x, line_y + game.coords.null_spot_below_top_bar_y)
  log.info('Null spot below the top bar (y=%d): (%d, %d), top '
           'positions moved by %+.0f px', line_y, *game.null_spot,
           game.coords.top_offset)


def _find_line(game):
  return find_top_bar_line(
    game.screen.bgr, game.coords.top_bar_line_min_rows_y)


def _log_fallback(game, reason):
  log.error(
    'Top bar not found (%s), the null spot stays at the fallback '
    '(%d, %d) from coords/reference.py. Risky: if the top bar covers '
    'it, station popups stay open; if it is too low, it can hit a '
    'customer bubble, open the Investor dialog and start an ad. The '
    'top positions are not aligned to the status bar either. Fix: '
    'check a screenshot of this phone and adjust actions/null_spot.py.',
    reason, *game.null_spot)
  key_log.error(
    'ERROR - Top bar not found (%s), null spot at fallback (%d, %d), '
    'popups may stay open or an ad may start; fix actions/null_spot.py',
    reason, *game.null_spot)

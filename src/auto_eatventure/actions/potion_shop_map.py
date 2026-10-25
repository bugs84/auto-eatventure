"""Potion Shop map: scrolling it to the shop or the cellar view (by
landmarks), its crates and stations."""

import logging
import time

from auto_eatventure.coords.geometry import Point, Region, Swipe

log = logging.getLogger(__name__)

# The crates (more slots of a station) have a moving shine, which
# lowers their score to ~0.7
CRATE_THRESHOLD = 0.7
# "MAX" in a station's popup
MAX_THRESHOLD = 0.8
POPUP_DELAY_S = 1
# Stations of the cellar view (coords potion_shop_<name>_station); the
# others are on the shop view
CELLAR_STATIONS = ('spider', 'mushrooms', 'frog')
# Landmarks of the map (template potion_shop_<name>, coords
# potion_shop_<name>_roi and _y); one is sometimes partly hidden by an
# alchemist or a price. The map is aligned when one is this close to
# its place.
LANDMARKS = ('barrel', 'landmark', 'skull', 'cellar')
LANDMARK_THRESHOLD = 0.7
LANDMARK_MISSES = 2
ALIGN_TRIES = 8
SWIPE_DELAY_S = 1.5
# A 1 s swipe moves the map ~1.1-1.3x its length, so a correction swipe
# covers a part of the offset and is repeated
SWIPE_SHARE = 0.8


def open_crates(game):
  """Tap the visible crates (each one adds a slot to its station)."""
  crates = game.screen.find_all('potion_shop_crate', CRATE_THRESHOLD)
  for crate in crates:
    log.info('Potion Shop: opening crate at (%d, %d)', *crate)
    game.device.tap(crate)
    time.sleep(0.3)
  return bool(crates)


def is_cellar_shown(game):
  """The map is at the cellar view (last screenshot)."""
  offset = shop_offset(game)
  return (offset is not None
          and abs(offset - game.coords.potion_shop_cellar_view_y)
          <= game.coords.potion_shop_aligned_y)


def show_shop(game):
  """Scroll the map so the whole shop with its stations is shown.
  Returns True when shown."""
  return _scroll_to(game, 0)


def show_cellar(game):
  """Scroll the map down to the cellar's stations. Returns True when
  shown."""
  return _scroll_to(game, game.coords.potion_shop_cellar_view_y)


def _scroll_to(game, view_y):
  """Scroll the map until shop_offset() is view_y. Returns True when
  there."""
  coords = game.coords
  # An open station popup would take the first swipe
  game.device.tap(game.null_spot)
  time.sleep(SWIPE_DELAY_S)
  misses = 0
  direction = 1
  last_offset = None
  for _ in range(ALIGN_TRIES):
    game.screen.capture()
    offset = shop_offset(game)
    log.debug('Potion Shop: landmark offset %s', offset)
    limit = coords.potion_shop_max_swipe_y
    if (offset is not None and last_offset is not None
        and abs(offset - last_offset) <= coords.potion_shop_aligned_y):
      # The swipe didn't move the map: it opened a station popup, which
      # takes the next swipes too
      game.device.tap(game.null_spot)
      time.sleep(SWIPE_DELAY_S)
    last_offset = offset
    if offset is None:
      # Hidden for a moment (an alchemist), or the map is far away:
      # scroll a screen up, then down, ...
      misses += 1
      if misses < LANDMARK_MISSES:
        time.sleep(SWIPE_DELAY_S)
        continue
      distance = limit * direction
      direction = -direction
    elif abs(offset - view_y) <= coords.potion_shop_aligned_y:
      return True
    else:
      distance = max(-limit, min(limit,
                                 round((view_y - offset) * SWIPE_SHARE)))
    start = Point(coords.potion_shop_swipe_x,
                  coords.potion_shop_swipe_from_y)
    game.device.swipe(Swipe(start, Point(start.x, start.y + distance)))
    time.sleep(SWIPE_DELAY_S)
  log.info('Potion Shop: could not scroll the map to %d', view_y)
  return False


def shop_offset(game):
  """How far (px, + = lower) the map is from its place on the last
  screenshot by the first landmark found, None when none is found."""
  coords = game.coords
  for name in LANDMARKS:
    mark = game.screen.find(f'potion_shop_{name}',
                            getattr(coords, f'potion_shop_{name}_roi'),
                            LANDMARK_THRESHOLD)
    if mark is not None:
      return mark.center.y - getattr(coords, f'potion_shop_{name}_y')
  return None


def station_arrow(game, name, icons):
  """The upgrade arrow (of stations.find_icons()) of the station on the
  current view, None when it has none (MAX or too expensive)."""
  coords = game.coords
  station = getattr(coords, f'potion_shop_{name}_station')
  radius = coords.potion_shop_station_arrow_x
  for icon in icons:
    if (abs(icon.x - station.x) <= radius
        and abs(icon.y - station.y) <= radius):
      return icon
  return None


def is_station_max(game, name):
  """Whether the station on the current view (the cellar for one of
  CELLAR_STATIONS) is MAX (its popup)."""
  coords = game.coords
  station = getattr(coords, f'potion_shop_{name}_station')
  game.device.tap(Point(
    station.x + coords.station_tap_shift_x,
    station.y + coords.station_tap_offset_y + coords.station_tap_shift_y))
  time.sleep(POPUP_DELAY_S)
  game.screen.capture()
  popup = Region(0, max(0, station.y - coords.potion_shop_station_popup_y),
                 game.screen.region.right, station.y)
  maxed = game.screen.has('potion_shop_max', popup, MAX_THRESHOLD)
  if name in CELLAR_STATIONS:
    close_cellar_popup(game)
  else:
    game.device.tap(game.null_spot)
  time.sleep(POPUP_DELAY_S)
  return maxed


def close_cellar_popup(game):
  """Close a station popup on the cellar view."""
  game.device.tap(game.coords.potion_shop_cellar_floor)

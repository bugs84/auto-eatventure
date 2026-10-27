"""Potion Shop map: scrolling it to the shop or the cellar view (by
landmarks), its crates and stations."""

import logging
import os
import time

import cv2

from auto_eatventure.actions import stations
from auto_eatventure.coords.geometry import Point, Region, Swipe
from auto_eatventure.logger import LOG_DIR
from auto_eatventure.vision.upgrade_icons import find_upgrade_icons

log = logging.getLogger(__name__)

# The crates (more slots of a station) have a moving shine, which
# lowers their score to ~0.7
CRATE_THRESHOLD = 0.7
# A crate in a shadow (e.g. the cellar's Spider Silk, in a dark corner)
# is found by its lower, less bright part (~0.9, other spots <= 0.77);
# looked for only without a lit crate, which it would find again
SHADOW_CRATE_THRESHOLD = 0.8
# The dashed tile of a locked station (on wood, in the cellar on stone):
# ~0.82-0.99, elsewhere <= 0.72
LOCKED_THRESHOLD = 0.8
# "MAX" in a station's popup
MAX_THRESHOLD = 0.8
POPUP_DELAY_S = 1
# Levels are bought by taps on the open popup's button, one each, or
# from HOLD_MIN_LEVELS on by holding it (faster, as in the cities: a 3 s
# hold bought 51 levels, 1.8 s ~20): HOLD_MS_PER_LEVEL each, HOLD_MIN_MS to
# HOLD_MAX_MS; the popup read after it tells how many were bought
LEVEL_TAP_DELAY_S = 0.3
HOLD_MIN_LEVELS = 5
HOLD_MS_PER_LEVEL = 90
HOLD_MIN_MS = 800
HOLD_MAX_MS = 6000
# Stations of the cellar view (coords potion_shop_<name>_station); the
# others are on the shop view
CELLAR_STATIONS = ('water', 'spider', 'mushrooms', 'frog')
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
  crates = (game.screen.find_all('potion_shop_crate', CRATE_THRESHOLD)
            or game.screen.find_all('potion_shop_crate_shadow',
                                    SHADOW_CRATE_THRESHOLD))
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


def shop_icons(game):
  """stations.find_icons() of the shop view and the arrow of Beetle
  Juice, which on a tall screen (LG G6) is below their limit (kept off
  the bottom buttons; the station is right of them)."""
  icons = stations.find_icons(game)
  coords = game.coords
  beetle = station_arrow(game, 'beetle', find_upgrade_icons(
    game.screen.hsv, coords.upgrade_arrow_min_height_y,
    coords.upgrade_arrow_max_height_y))
  if beetle is not None and beetle not in icons:
    icons.append(beetle)
  return icons


def station_place(game, name):
  """Where the station's arrow shows on the current view: its place on
  the shop or cellar view moved by how far the map is from that view
  (a scroll of ~180 px put the Unicorn's arrow on the Djinn's place)."""
  coords = game.coords
  station = getattr(coords, f'potion_shop_{name}_station')
  offset = shop_offset(game)
  if offset is None:
    return station
  if name in CELLAR_STATIONS:
    offset -= coords.potion_shop_cellar_view_y
  return Point(station.x, station.y + offset)


def current_view(game):
  """'shop' or 'cellar' when the map is at that view (last
  screenshot), else None."""
  offset = shop_offset(game)
  if offset is None:
    return None
  aligned = game.coords.potion_shop_aligned_y
  if abs(offset) <= aligned:
    return 'shop'
  if abs(offset - game.coords.potion_shop_cellar_view_y) <= aligned:
    return 'cellar'
  return None


def view_of(name):
  return 'cellar' if name in CELLAR_STATIONS else 'shop'


def read_station(game, name):
  """The station's popup numbers (tapped open and closed): see
  open_station()."""
  popup = open_station(game, name)
  close_station(game, name)
  return popup


def open_station(game, name):
  """Open the station's popup. Returns its numbers (StationPopup of
  vision/station_popup.py), 'max' when it is MAX, None when they can't
  be read (e.g. not unlocked, covered; the screenshot is saved to
  logs/)."""
  coords = game.coords
  place = station_place(game, name)
  game.device.tap(Point(
    place.x + coords.station_tap_shift_x,
    place.y + coords.station_tap_offset_y + coords.station_tap_shift_y))
  time.sleep(POPUP_DELAY_S)
  game.screen.capture()
  return _popup_numbers(game, name, place)


def buy_levels(game, name, count):
  """Buy about count levels on the open popup (tap or hold its
  button). Returns the popup's numbers after (see open_station())."""
  button = game.screen.station_popup_button(game.coords)
  if button is None:
    return None
  if count >= HOLD_MIN_LEVELS:
    game.device.long_press(button, max(HOLD_MIN_MS, min(
      HOLD_MAX_MS, count * HOLD_MS_PER_LEVEL)))
  else:
    for _ in range(count):
      game.device.tap(button)
      time.sleep(LEVEL_TAP_DELAY_S)
  time.sleep(POPUP_DELAY_S)
  game.screen.capture()
  return _popup_numbers(game, name, station_place(game, name))


def close_station(game, name):
  """Close the station's open popup."""
  if name in CELLAR_STATIONS:
    close_cellar_popup(game)
  else:
    game.device.tap(game.coords.potion_shop_floor)
  time.sleep(POPUP_DELAY_S)


def _popup_numbers(game, name, place):
  popup = game.screen.read_station_popup(game.coords)
  if popup is None and is_max_shown(game, place):
    return 'max'
  if popup is None:
    # To see why (e.g. a new suffix letter without its sample)
    cv2.imwrite(os.path.join(LOG_DIR, f'station_popup_{name}.png'),
                game.screen.bgr)
  return popup


def station_arrow(game, name, icons):
  """The upgrade arrow (of stations.find_icons()) of the station on the
  current view, None when it has none (MAX or too expensive)."""
  coords = game.coords
  station = station_place(game, name)
  radius = coords.potion_shop_station_arrow_x
  near = [icon for icon in icons
          if abs(icon.x - station.x) <= radius
          and abs(icon.y - station.y) <= radius]
  return min(near, default=None,
             key=lambda icon: abs(icon.x - station.x)
             + abs(icon.y - station.y))


def is_locked(game, arrow):
  """Whether the arrow is over a dashed tile: it unlocks a station."""
  coords = game.coords
  region = Region(max(0, arrow.x - coords.potion_shop_locked_left_x),
                  arrow.y,
                  arrow.x + coords.potion_shop_locked_right_x,
                  arrow.y + coords.potion_shop_locked_below_y)
  return any(game.screen.has(name, region, LOCKED_THRESHOLD)
             for name in ('potion_shop_locked', 'potion_shop_locked_cellar'))


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
  maxed = is_max_shown(game, station)
  if name in CELLAR_STATIONS:
    close_cellar_popup(game)
  else:
    game.device.tap(game.null_spot)
  time.sleep(POPUP_DELAY_S)
  return maxed


def is_max_shown(game, place):
  """Whether the popup of the station at place shows MAX (last
  screenshot)."""
  popup = Region(0, max(0, place.y - game.coords.potion_shop_station_popup_y),
                 game.screen.region.right, place.y)
  return game.screen.has('potion_shop_max', popup, MAX_THRESHOLD)


def close_cellar_popup(game):
  """Close a station popup on the cellar view."""
  game.device.tap(game.coords.potion_shop_cellar_floor)

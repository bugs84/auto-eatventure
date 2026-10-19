"""Potion Shop event: entering and leaving it, its crates, brewing
potions and scrolling its map to the shop."""

import logging
import time

from auto_eatventure.actions import levels, popups
from auto_eatventure.coords.geometry import Point, Region, Swipe
from auto_eatventure.logger import key_log
from auto_eatventure.vision.colors import GREEN, RED

log = logging.getLogger(__name__)

# The event's cauldron button and dialog buttons
BUTTON_THRESHOLD = 0.8
# Time for the "Potion Shop" dialog to open
DIALOG_DELAY_S = 2
# The green loading screen after Enter takes ~8 s
ENTER_TIMEOUT_S = 30
# The crates (more slots of a station) have a moving shine, which
# lowers their score to ~0.7
CRATE_THRESHOLD = 0.7
# The green coin covers ~17% of its search area, 0% on the main screen
COIN_MIN_RATIO = 0.08
# The red "!" badge fills ~20-30% of its area (like the Upgrades one)
BADGE_MIN_RATIO = 0.12
# The red X of the Cauldron dialog fills most of its area
CLOSE_MIN_RATIO = 0.4
CAULDRON_DELAY_S = 1.5
# Potions (template potion_shop_<name>) and the level each is brewed
# to, in this order; each brew raises the level by one. The levels
# follow the fastest runs found on the web (experiments/potion_shop/
# NOTES.md): Swift (walk) and Sizzle (food) first, then Instant and
# Double food. A potion stays active (5 slots) until bottled.
BREW_PLAN = (
  ('swift', 4), ('sizzle', 4), ('instant', 4), ('double', 4),
  ('perfect', 3), ('swift', 8), ('instant', 6), ('double', 6),
  ('sizzle', 6))
POTIONS = ('swift', 'sizzle', 'perfect', 'instant', 'double',
           'telepathic')
POTION_THRESHOLD = 0.8
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


def is_available(game):
  """The event's button is shown in the right column (main screen)."""
  return _find_button(game) is not None


def is_inside(game):
  """The green event coin is shown left of the coin counter (the
  main game's coin is gold; a dialog dimming the top bar hides it)."""
  return (game.screen.color_ratio(game.coords.potion_shop_coin_roi, GREEN)
          >= COIN_MIN_RATIO)


def enter(game):
  """Open the event from the main screen. Returns True when inside."""
  if not _open_dialog(game, 'potion_shop_enter'):
    return False
  log.info('Potion Shop: entering')
  game.device.tap(game.coords.potion_shop_enter_exit)
  levels.tap_open_button(game)
  deadline = time.monotonic() + ENTER_TIMEOUT_S
  while time.monotonic() < deadline:
    game.screen.capture()
    if is_inside(game):
      key_log.info('POTION SHOP - Entered the event')
      return True
    time.sleep(1)
  log.warning('Potion Shop: not inside after Enter')
  return False


def leave(game):
  """Back to the main game by Exit. Returns True when left."""
  if not _open_dialog(game, 'potion_shop_exit'):
    return False
  log.info('Potion Shop: leaving')
  game.device.tap(game.coords.potion_shop_enter_exit)
  time.sleep(ENTER_TIMEOUT_S / 3)
  game.screen.capture()
  return not is_inside(game)


def open_crates(game):
  """Tap the visible crates (each one adds a slot to its station)."""
  crates = game.screen.find_all('potion_shop_crate', CRATE_THRESHOLD)
  for crate in crates:
    log.info('Potion Shop: opening crate at (%d, %d)', *crate)
    game.device.tap(crate)
    time.sleep(0.3)
  return bool(crates)


def can_brew(game):
  """The Cauldron button shows its red "!" badge (a brewed potion is
  done)."""
  return (game.screen.color_ratio(
            game.coords.potion_shop_cauldron_badge_roi, RED)
          >= BADGE_MIN_RATIO)


def brew(game):
  """Open the Cauldron, claim a finished potion and brew the next one
  by BREW_ORDER. Returns True when a potion was brewed."""
  coords = game.coords
  if not is_cauldron_open(game):
    game.device.tap(coords.potion_shop_cauldron_button)
    time.sleep(CAULDRON_DELAY_S)
    game.screen.capture()
    if not is_cauldron_open(game):
      log.info('Potion Shop: Cauldron dialog did not open')
      return False
  _claim(game)
  game.device.tap(coords.potion_shop_brew_tab)
  time.sleep(CAULDRON_DELAY_S)
  game.screen.capture()
  brewed = _brew_next(game)
  game.device.tap(coords.potion_shop_cauldron_close)
  time.sleep(CAULDRON_DELAY_S)
  return brewed


def is_cauldron_open(game):
  """Red X of the Cauldron dialog (it also opens by itself with "Brew
  Complete!" when a potion is done)."""
  return (game.screen.color_ratio(
            game.coords.potion_shop_cauldron_close_roi, RED)
          >= CLOSE_MIN_RATIO)


def _claim(game):
  """Claim the finished potion ("Brew Complete!"), if any."""
  button = game.screen.find('potion_shop_claim',
                            game.coords.potion_shop_brew_list_roi,
                            BUTTON_THRESHOLD)
  if button is None:
    return
  log.info('Potion Shop: claiming a brewed potion')
  game.device.tap(button.center)
  time.sleep(CAULDRON_DELAY_S)
  game.screen.capture()


def _brew_next(game):
  """Brew the first potion of BREW_PLAN below its level that has a
  Brew button (while a potion is brewing the list shows only it,
  without a Brew button). Returns True when one was brewed."""
  rows = _potion_rows(game)
  log.debug('Potion Shop: potions %s', {
    name: level for name, (level, _) in rows.items()})
  for name, level_to in BREW_PLAN:
    level, button = rows.get(name, (None, None))
    if button is not None and level is not None and level <= level_to:
      return _tap_brew(game, button, f'{name} (level {level})')
  log.info('Potion Shop: nothing to brew')
  return False


def _potion_rows(game):
  """{potion: (level shown, its Brew button or None)} of the potions
  found in the Brew list."""
  coords = game.coords
  buttons = coords.potion_shop_brew_list_roi
  rows = {}
  for name in POTIONS:
    icon = game.screen.find(f'potion_shop_{name}',
                            coords.potion_shop_potion_icons_roi,
                            POTION_THRESHOLD)
    if icon is None:
      continue
    center = icon.center
    level = game.screen.read_level(
      coords.potion_shop_level_label.moved(center.x, center.y))
    row = Region(buttons.left, icon.top, buttons.right, icon.bottom)
    rows[name] = (level, game.screen.find('potion_shop_brew', row,
                                          BUTTON_THRESHOLD))
  return rows


def _tap_brew(game, button, name):
  log.info('Potion Shop: brewing %s', name)
  game.device.tap(button.center)
  time.sleep(CAULDRON_DELAY_S)
  return True


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
  for _ in range(ALIGN_TRIES):
    game.screen.capture()
    offset = shop_offset(game)
    log.debug('Potion Shop: landmark offset %s', offset)
    limit = coords.potion_shop_max_swipe_y
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


def _open_dialog(game, button_name):
  """Open the "Potion Shop" dialog and wait for its button (Enter or
  Exit). Returns True when it is shown."""
  game.screen.capture()
  button = _find_button(game)
  if button is None:
    log.info('Potion Shop: event button not found')
    return False
  game.device.tap(button.center)
  time.sleep(DIALOG_DELAY_S)
  game.screen.capture()
  if game.screen.has(button_name, game.coords.potion_shop_enter_exit_roi,
                     BUTTON_THRESHOLD):
    return True
  log.info('Potion Shop: %s not found in the dialog', button_name)
  if popups.is_screen_dimmed(game):
    game.device.tap(game.coords.potion_shop_dialog_close)
    time.sleep(DIALOG_DELAY_S)
  return False


def _find_button(game):
  return game.screen.find('potion_shop_button',
                          game.coords.potion_shop_button_roi,
                          BUTTON_THRESHOLD)

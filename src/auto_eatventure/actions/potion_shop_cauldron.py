"""Potion Shop Cauldron: claiming, brewing potions by plan and
bottling them."""

import logging
import time
from collections import namedtuple

from auto_eatventure.coords.geometry import Region, Swipe
from auto_eatventure.logger import key_log
from auto_eatventure.vision.colors import RED

log = logging.getLogger(__name__)

# Claim, Brew, "Slots Full!", "MAX" and Bottle of the Cauldron dialog
BUTTON_THRESHOLD = 0.8
# The red "!" badge fills ~20-30% of its area (like the Upgrades one)
BADGE_MIN_RATIO = 0.12
# The red X of the Cauldron dialog fills most of its area
CLOSE_MIN_RATIO = 0.4
CAULDRON_DELAY_S = 1.5
# Potions (template potion_shop_<name>) and the level each is brewed
# to: the first one of the plan below its level that can be brewed;
# each brew raises the level by one. The order of the 21 min run
# (experiments/potion_shop/video_transcript/GUIDE.md): Swift, Sizzle
# (Unicorn), Double (Mermaid, before the Djinn), Swift, Double, Instant
# (Djinn); no Perfect. The bot's stations are slower (no boosts): the
# levels are a bit higher and the last three keep the Cauldron busy
# until the cellar's potions. A potion stays active (5 slots) until
# bottled.
BREW_PLAN = (
  ('swift', 4), ('sizzle', 4), ('double', 4), ('swift', 7),
  ('double', 6), ('instant', 6), ('swift', 8), ('double', 7),
  ('instant', 7))
# Once the cellar's ingredients show Divine in the list: Divine, then
# Golden (Sizzle is bottled for its slot; bottling sets a potion's level
# back to 1, so it is not brewed again); Golden to 7 (user's advice:
# worth it near the end). After it nothing more is brewed (the video
# stops brewing and buys the customers).
LATE_PLAN = (
  ('swift', 7), ('double', 6), ('instant', 6), ('divine', 5),
  ('golden', 7))
LATE_POTION = 'divine'
POTIONS = ('swift', 'sizzle', 'perfect', 'instant', 'double',
           'telepathic', 'divine', 'golden', 'greedy', 'addictive')
# A row of the Brew list: "Lvl N" (the next brew's level; None when
# unreadable), the Brew button (None while brewing or at the max level),
# "Slots Full!" (5 potions active, the potion isn't) and "MAX" (the
# potion is at its max level, 10)
PotionRow = namedtuple('PotionRow', 'level button slots_full maxed')
# When a planned potion can't be brewed because all slots are full,
# the first active of these is bottled (1 cork)
BOTTLE_ORDER = ('sizzle', 'perfect')
POTION_THRESHOLD = 0.8


def can_brew(game):
  """The Cauldron button shows its red "!" badge (a brewed potion is
  done)."""
  return (game.screen.color_ratio(
            game.coords.potion_shop_cauldron_badge_roi, RED)
          >= BADGE_MIN_RATIO)


def is_cauldron_open(game):
  """Red X of the Cauldron dialog (it also opens by itself with "Brew
  Complete!" when a potion is done)."""
  return (game.screen.color_ratio(
            game.coords.potion_shop_cauldron_close_roi, RED)
          >= CLOSE_MIN_RATIO)


def brew(game):
  """Open the Cauldron, claim a finished potion and brew the next one
  of the plan. Returns 'brewed', 'done' (LATE_PLAN complete: nothing
  more to brew) or None."""
  if not _open_brew_tab(game):
    return None
  result = _brew_next(game)
  _close_cauldron(game)
  return result


def bottle_or_brew(game, name, keep, bottle=True):
  """Bottle the potion when it is at its max level (unless not bottle),
  else brew its next level; with all slots full an active potion not in
  keep is bottled first. Returns 'bottled', 'max' (at its max level, not
  bottled), 'brewed' or None (nothing done, e.g. while brewing)."""
  if not _open_brew_tab(game):
    return None
  both, rows = _read_brew_list(game)
  row = both.get(name)
  result = None
  if row is None:
    # While brewing the list shows only the brewing potion (its icon
    # isn't always found then)
    log.debug('Potion Shop: %s not in the Brew list', name)
  elif row.maxed and not bottle:
    result = 'max'
  elif row.maxed:
    if _bottle(game, (name,), 'at its max level'):
      result = 'bottled'
  elif row.button is not None:
    if _brew_listed(game, name, row.level, rows):
      result = 'brewed'
  elif row.slots_full:
    _bottle(game, [other for other in POTIONS if other not in keep],
            'to free a slot')
  _close_cauldron(game)
  return result


def bottle_all(game, reason):
  """Bottle every active potion (1 cork each). Returns the number
  bottled."""
  if not _open_brew_tab(game):
    return 0
  bottled = 0
  while bottled < len(POTIONS) and _bottle(game, POTIONS, reason):
    bottled += 1
  _close_cauldron(game)
  return bottled


def _open_brew_tab(game):
  """Open the Cauldron (unless open), claim a finished potion and show
  the Brew tab. Returns False when the dialog did not open."""
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
  return True


def _close_cauldron(game):
  game.device.tap(game.coords.potion_shop_cauldron_close)
  time.sleep(CAULDRON_DELAY_S)


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
  """Brew the first potion of the plan below its level that has a
  Brew button (while a potion is brewing the list shows only it,
  without a Brew button). Returns 'brewed', 'done' (LATE_PLAN
  complete) or None."""
  both, rows = _read_brew_list(game)
  plan = LATE_PLAN if LATE_POTION in both else BREW_PLAN
  log.debug('Potion Shop: potions %s', {
    name: row.level for name, row in both.items()})
  for name, level_to in plan:
    row = both.get(name)
    if (row is None or row.button is None or row.level is None
        or row.level > level_to):
      continue
    return 'brewed' if _brew_listed(game, name, row.level, rows) else None
  if _needs_slot(plan, both):
    _bottle(game, BOTTLE_ORDER, 'to free a slot')
  log.info('Potion Shop: nothing to brew')
  return 'done' if _is_plan_done(LATE_PLAN, both) else None


def _is_plan_done(plan, rows):
  """Every potion of the plan is listed and brewed to its level (the
  list shows the next brew's level) or MAX."""
  for name, level_to in plan:
    row = rows.get(name)
    if row is None or not (
        row.maxed or row.level is not None and row.level > level_to):
      return False
  return True


def _read_brew_list(game):
  """The rows of the Brew list's first page and its scrolled part
  (only one row while brewing, then not scrolled). Returns (rows of
  both pages, rows of the page shown)."""
  first = rows = _potion_rows(game)
  if len(first) > 1:
    _scroll_brew_list(game, game.coords.potion_shop_brew_list_swipe)
    rows = _potion_rows(game)
  both = dict(first)
  for name, row in rows.items():
    # A label at the screen's edge may be unreadable on one page
    if row.level is not None or name not in both:
      both[name] = row
  return both, rows


def _brew_listed(game, name, level, rows):
  """Tap the potion's Brew button: on the page shown (rows) or on the
  first page. Returns True when tapped."""
  row = rows.get(name)
  if row is not None and row.button is not None:
    button = row.button
  else:
    swipe = game.coords.potion_shop_brew_list_swipe
    _scroll_brew_list(game, Swipe(swipe.end, swipe.start))
    row = _potion_rows(game).get(name)
    if row is None or row.button is None:
      return False
    button = row.button
  return _tap_brew(game, button, f'{name} (level {level})')


def _scroll_brew_list(game, swipe):
  game.device.swipe(swipe)
  time.sleep(CAULDRON_DELAY_S)
  game.screen.capture()


def _needs_slot(plan, rows):
  """Whether a planned potion can't be brewed only because all slots
  are full."""
  for name, level_to in plan:
    row = rows.get(name)
    if (row is not None and row.slots_full and row.level is not None
        and row.level <= level_to):
      return True
  return False


def _potion_rows(game):
  """{potion: PotionRow} of the potions found in the Brew list."""
  coords = game.coords
  buttons = coords.potion_shop_brew_list_roi
  rows = {}
  for name in POTIONS:
    icon = _find_potion(game, name)
    if icon is None:
      continue
    center = icon.center
    level = game.screen.read_level(
      coords.potion_shop_level_label.moved(center.x, center.y))
    # "Slots Full!" is a bit above the icon's top
    row = Region(buttons.left, icon.top - (icon.bottom - icon.top) // 4,
                 buttons.right, icon.bottom)
    rows[name] = PotionRow(
      level, game.screen.find('potion_shop_brew', row, BUTTON_THRESHOLD),
      game.screen.has('potion_shop_slots_full', row, BUTTON_THRESHOLD),
      game.screen.has('potion_shop_brew_max', row, BUTTON_THRESHOLD))
  return rows


def _bottle(game, names, reason):
  """Bottle the first active potion of names (Active Potions tab, 1
  cork). Returns its name, None when none was bottled."""
  coords = game.coords
  game.device.tap(coords.potion_shop_active_tab)
  time.sleep(CAULDRON_DELAY_S)
  game.screen.capture()
  for name in names:
    icon = _find_potion(game, name)
    if icon is None:
      continue
    center = icon.center
    button = game.screen.find(
      'potion_shop_bottle',
      coords.potion_shop_bottle_row.moved(center.x, center.y),
      BUTTON_THRESHOLD)
    if button is not None:
      key_log.info('POTION SHOP - Bottled %s %s', name, reason)
      game.device.tap(button.center)
      time.sleep(CAULDRON_DELAY_S)
      return name
  log.info('Potion Shop: no potion to bottle')
  return None


def _find_potion(game, name):
  return game.screen.find(f'potion_shop_{name}',
                          game.coords.potion_shop_potion_icons_roi,
                          POTION_THRESHOLD)


def _tap_brew(game, button, name):
  log.info('Potion Shop: brewing %s', name)
  game.device.tap(button.center)
  time.sleep(CAULDRON_DELAY_S)
  return True

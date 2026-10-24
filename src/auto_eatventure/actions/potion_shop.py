"""Potion Shop event: entering and leaving it, its crates, brewing
potions and scrolling its map to the shop."""

import logging
import time
from collections import namedtuple

from auto_eatventure.actions import levels, popups, upgrades
from auto_eatventure.coords.geometry import Point, Region, Swipe
from auto_eatventure.logger import key_log
from auto_eatventure.vision.colors import GREEN, RED

log = logging.getLogger(__name__)

# The event's cauldron button and dialog buttons
BUTTON_THRESHOLD = 0.8
# Time for the "Potion Shop" dialog to open
DIALOG_DELAY_S = 2
# The green loading screen after Enter takes ~8 s, the "Open" of the
# first stand (first entry only) shows up later
ENTER_TIMEOUT_S = 60
# End game: once Beetle Juice (the shop's last station) is MAX, only the
# best paying station is upgraded, coins are saved for it, until it is
# MAX (level 1000), then the next one. Stations by income: Bat Wing,
# Dragon Scale, Unicorn Horn, Djinn's Breath, Mermaid Tears, Beetle
# Juice, then the cellar's Purified Water, Spider Silk, Mystic
# Mushrooms, Frog Screams.
END_GAME_STATION = 'beetle'
FOCUS_STATIONS = ('spider', 'mushrooms', 'frog')
# Focused stations whose last upgrade (Upgrades dialog: Mushrooms x100,
# Frog x175) was still to be bought; their levels are upgraded only after
# it, levels without it are not worth the coins
LAST_UPGRADES = ('mushrooms', 'frog')
POPUP_DELAY_S = 1
# The rewards list is scrolled to its bottom by this many swipes; a
# reward's green check fills ~10% of its icon's area (0% without it)
REWARDS_SWIPES = 4
REWARDS_SWIPE_DELAY_S = 0.8
CHECK_MIN_RATIO = 0.06
# The crates (more slots of a station) have a moving shine, which
# lowers their score to ~0.7
CRATE_THRESHOLD = 0.7
# The green coin covers ~17% of its search area, 0% on the main screen
COIN_MIN_RATIO = 0.08
# The event's loading screen is all teal (its coin area too)
LOADING_TEAL = [((80, 200, 100), (90, 255, 180))]
LOADING_MIN_RATIO = 0.9
# The red "!" badge fills ~20-30% of its area (like the Upgrades one)
BADGE_MIN_RATIO = 0.12
# The red X of the Cauldron dialog fills most of its area
CLOSE_MIN_RATIO = 0.4
CAULDRON_DELAY_S = 1.5
# Rows of the Upgrades dialog looked at (the 5th is cut off), upgrades
# bought in one visit at most (a bought row leaves the list, the rows
# below move up)
UPGRADE_ROWS = 4
MAX_UPGRADE_BUYS = 30
UPGRADE_BUY_DELAY_S = 0.6
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
  main game's coin is gold; a dialog dimming the top bar hides it), not
  the teal loading screen."""
  screen = game.screen
  return (screen.color_ratio(game.coords.potion_shop_coin_roi, GREEN)
          >= COIN_MIN_RATIO
          and screen.color_ratio(game.coords.potion_shop_loading_roi,
                                 LOADING_TEAL) < LOADING_MIN_RATIO)


def enter(game):
  """Open the event from the main screen. Returns True when inside."""
  if not _open_dialog(game, 'potion_shop_enter'):
    return False
  log.info('Potion Shop: entering')
  game.device.tap(game.coords.potion_shop_enter_exit)
  deadline = time.monotonic() + ENTER_TIMEOUT_S
  while time.monotonic() < deadline:
    game.screen.capture()
    if is_inside(game):
      key_log.info('POTION SHOP - Entered the event')
      return True
    close_outside_dialog(game)
    time.sleep(1)
  log.warning('Potion Shop: not inside after Enter')
  return False


def close_outside_dialog(game):
  """Tap Open of "Welcome to the Potion Shop!" (a new event) or close a
  red X dialog. Returns True when Open was tapped (the event loads)."""
  # Never tapped blindly: entered again, "Offline Earnings" shows
  # instead, with its Collect x2 (an ad) next to the Open spot
  if levels.is_open_button_shown(game):
    log.info('Potion Shop: Open of the welcome dialog')
    game.device.tap(game.coords.first_stand_open_button)
    return True
  popups.close_popup(game)
  return False


def is_completed(game):
  """Whether the event's last reward is done (the rewards list of the
  "Potion Shop" dialog, scrolled to its bottom)."""
  if not _open_dialog(game, 'potion_shop_exit'):
    return False
  coords = game.coords
  for _ in range(REWARDS_SWIPES):
    game.device.swipe(coords.potion_shop_rewards_swipe)
    time.sleep(REWARDS_SWIPE_DELAY_S)
  time.sleep(REWARDS_SWIPE_DELAY_S)
  game.screen.capture()
  done = (game.screen.color_ratio(coords.potion_shop_last_reward_roi,
                                  GREEN)
          >= CHECK_MIN_RATIO)
  if done:
    key_log.info('POTION SHOP - All rewards done')
  else:
    log.info('Potion Shop: rewards not all done yet')
  game.device.tap(coords.potion_shop_dialog_close)
  time.sleep(DIALOG_DELAY_S)
  return done


def leave(game):
  """Leave the event (Exit). Returns True when left."""
  if not _open_dialog(game, 'potion_shop_exit'):
    return False
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
  FOCUS_STATIONS) is MAX (its popup)."""
  coords = game.coords
  station = getattr(coords, f'potion_shop_{name}_station')
  game.device.tap(Point(
    station.x + coords.station_tap_shift_x,
    station.y + coords.station_tap_offset_y + coords.station_tap_shift_y))
  time.sleep(POPUP_DELAY_S)
  game.screen.capture()
  popup = Region(0, max(0, station.y - coords.potion_shop_station_popup_y),
                 game.screen.region.right, station.y)
  maxed = game.screen.has('potion_shop_max', popup, BUTTON_THRESHOLD)
  if name in FOCUS_STATIONS:
    close_cellar_popup(game)
  else:
    game.device.tap(game.null_spot)
  time.sleep(POPUP_DELAY_S)
  return maxed


def close_cellar_popup(game):
  """Close a station popup on the cellar view."""
  game.device.tap(game.coords.potion_shop_cellar_floor)


def buy_upgrades(game, customers):
  """Buy the affordable upgrades of the Upgrades dialog, the top row
  first, but at most `customers` "+N Customer(s)" rows (the guides buy
  them only after brewing: more customers keep the alchemists from
  carrying the ingredients). Returns (upgrades, customer rows) bought."""
  if not upgrades.open_dialog(game):
    return 0, 0
  bought = customer_rows = 0
  while bought < MAX_UPGRADE_BUYS:
    row = _affordable_row(game, customer_rows < customers)
    if row is None:
      break
    button, customer = row
    log.info('Potion Shop: buying an upgrade%s',
             ' (customers)' if customer else '')
    game.device.tap(button)
    bought += 1
    customer_rows += customer
    time.sleep(UPGRADE_BUY_DELAY_S)
    game.screen.capture()
  upgrades.close_dialog(game)
  game.screen.capture()
  return bought, customer_rows


def _affordable_row(game, customers):
  """(buy button, is a customer row) of the first visible row that can
  be bought (customer rows only when customers); None when none."""
  coords = game.coords
  for index in range(UPGRADE_ROWS):
    dy = index * coords.potion_shop_upgrade_row_y
    button = coords.first_upgrade_buy_roi.moved(0, dy)
    if not upgrades.is_affordable(game, button):
      continue
    customer = game.screen.has(
      'potion_shop_upgrade_customer',
      coords.potion_shop_upgrade_icon_roi.moved(0, dy))
    if customer and not customers:
      continue
    return button.center, customer
  return None


def has_last_upgrade(game, name):
  """Whether the Upgrades dialog still lists the station's upgrade (a
  name of LAST_UPGRADES); also True when the dialog did not open."""
  if not upgrades.open_dialog(game):
    return True
  listed = game.screen.has(f'potion_shop_upgrade_{name}',
                           game.coords.potion_shop_upgrades_roi)
  upgrades.close_dialog(game)
  return listed


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

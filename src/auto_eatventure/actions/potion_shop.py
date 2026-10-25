"""Potion Shop event: its button and "Potion Shop" dialog (entering,
leaving, the rewards) and its Upgrades dialog. The Cauldron is in
potion_shop_cauldron.py, the map in potion_shop_map.py; the event is
played by potion_shop_loop.py."""

import logging
import time

from auto_eatventure.actions import levels, popups, upgrades
from auto_eatventure.logger import key_log
from auto_eatventure.vision.colors import GREEN

log = logging.getLogger(__name__)

# The event's cauldron button and dialog buttons
BUTTON_THRESHOLD = 0.8
# Time for the "Potion Shop" dialog to open
DIALOG_DELAY_S = 2
# The green loading screen after Enter takes ~8 s, the "Open" of the
# first stand (first entry only) shows up later
ENTER_TIMEOUT_S = 60
# The rewards list is scrolled to its bottom by this many swipes; a
# reward's green check fills ~10% of its icon's area (0% without it)
REWARDS_SWIPES = 4
REWARDS_SWIPE_DELAY_S = 0.8
CHECK_MIN_RATIO = 0.06
# The green coin covers ~17% of its search area, 0% on the main screen
COIN_MIN_RATIO = 0.08
# The event's loading screen is all teal (its coin area too)
LOADING_TEAL = [((80, 200, 100), (90, 255, 180))]
LOADING_MIN_RATIO = 0.9
# Rows of the Upgrades dialog looked at (the 5th is cut off), upgrades
# bought in one visit at most (a bought row leaves the list, the rows
# below move up)
UPGRADE_ROWS = 4
MAX_UPGRADE_BUYS = 30
UPGRADE_BUY_DELAY_S = 0.6


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
  """Whether the Upgrades dialog still lists the station's last
  upgrade (template potion_shop_upgrade_<name>); also True when the
  dialog did not open."""
  if not upgrades.open_dialog(game):
    return True
  listed = game.screen.has(f'potion_shop_upgrade_{name}',
                           game.coords.potion_shop_upgrades_roi)
  upgrades.close_dialog(game)
  return listed


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

"""Potion Shop event: its button and "Potion Shop" dialog (entering,
leaving, the rewards) and its Upgrades dialog. The Cauldron is in
potion_shop_cauldron.py, the map in potion_shop_map.py; the event is
played by potion_shop_loop.py."""

import logging
import time

from auto_eatventure import potion_shop_upgrades
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
# Time for the main screen to load after Exit
LEAVE_DELAY_S = 20
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
# The Upgrades dialog is read page by page (a swipe moves it ~3 rows),
# up to its end (the same rows twice)
UPGRADE_PAGES = 15
UPGRADE_DELAY_S = 1
# Stations, by income
STATIONS = ('bat', 'dragon', 'unicorn', 'djinn', 'mermaid', 'beetle',
            'water', 'spider', 'mushrooms', 'frog')


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
  time.sleep(LEAVE_DELAY_S)
  game.screen.capture()
  return not is_inside(game)


def read_upgrades(game):
  """The rows of the Upgrades dialog (potion_shop_upgrades.Upgrade, not
  bought yet), None when the dialog did not open."""
  if not upgrades.open_dialog(game):
    return None
  rows = []
  _scan_upgrades(game, lambda buttons: _note_rows(rows, buttons))
  upgrades.close_dialog(game)
  game.screen.capture()
  log.info('Potion Shop: %d upgrades to buy', len(rows))
  return rows


def buy_upgrade(game, upgrade):
  """Buy the row of the Upgrades dialog (its button found by its
  price). Returns True when bought (gone from the dialog)."""
  if not upgrades.open_dialog(game):
    return False
  bought = _scan_upgrades(game, lambda buttons: _buy_row(game, upgrade,
                                                         buttons))
  upgrades.close_dialog(game)
  game.screen.capture()
  if bought:
    what = ' '.join(filter(None, (
      upgrade.station, upgrade.kind,
      upgrade.multiplier and f'x{upgrade.multiplier:g}')))
    key_log.info('POTION SHOP - Bought %s (%s, %s)', upgrade.title, what,
                 upgrade.price)
  return bool(bought)


def _scan_upgrades(game, page):
  """Call page(buttons) on each page of the open dialog until it
  returns something other than None (returned) or the end."""
  coords = game.coords
  last = None
  for _ in range(UPGRADE_PAGES):
    buttons = game.screen.read_price_buttons(
      coords.potion_shop_upgrade_buttons_roi, coords)
    result = page(buttons)
    if result is not None:
      return result
    prices = [button.price for button in buttons]
    if prices == last:
      break
    last = prices
    game.device.swipe(coords.potion_shop_upgrades_swipe)
    time.sleep(UPGRADE_DELAY_S)
    game.screen.capture()
  return None


def _note_rows(rows, buttons):
  for button in buttons:
    if button.price is None:
      continue
    upgrade = potion_shop_upgrades.find(button.price)
    if upgrade is None:
      log.info('Potion Shop: unknown upgrade of price %.3g', button.price)
    elif upgrade not in rows:
      rows.append(upgrade)


def _buy_row(game, upgrade, buttons):
  """Tap the button of the upgrade among buttons. Returns True when
  bought, False when it can't be (grey), None when not among them."""
  for button in buttons:
    if (button.price is None
        or potion_shop_upgrades.find(button.price) != upgrade):
      continue
    if not button.affordable:
      return False
    game.device.tap(button.center)
    time.sleep(UPGRADE_DELAY_S)
    game.screen.capture()
    return not any(
      other.price is not None
      and potion_shop_upgrades.find(other.price) == upgrade
      for other in game.screen.read_price_buttons(
        game.coords.potion_shop_upgrade_buttons_roi, game.coords))
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

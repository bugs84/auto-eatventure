"""PotionBottlesLoop: after the Potion Shop's rewards, brews the potions
of POTION_SHOP_BOTTLES to their max level and bottles them (to use
them outside the event)."""

import datetime
import json
import logging
import time

from auto_eatventure import config
from auto_eatventure.actions import popups, potion_shop
from auto_eatventure.logger import key_log
from auto_eatventure.timer import Timer

log = logging.getLogger(__name__)

# Bottled counts of the current event, kept across restarts of the bot
BOTTLES_FILE = 'potion_shop_bottles.json'
# The Cauldron is looked at this often (a brew takes ~3 min; "Brew
# Complete!" also opens it by itself)
CAULDRON_CHECK_S = 30
LOOP_DELAY_S = 1
# Screenshots outside the event in a row that end the loop
OUTSIDE_LOOPS = 3


def parse_orders(text):
  """[(potion, count)] of "golden:2,divine:1"; unknown potions and bad
  counts are skipped with a warning."""
  orders = []
  for item in text.split(','):
    if not item.strip():
      continue
    name, _, count = item.partition(':')
    name = name.strip().lower()
    try:
      count = int(count or '1')
    except ValueError:
      count = 0
    if name not in potion_shop.POTIONS or count < 1:
      log.warning('POTION_SHOP_BOTTLES: %r ignored', item)
      continue
    orders.append((name, count))
  return orders


class PotionBottlesLoop:
  """Brews and bottles the ordered potions one after another while
  the bot is inside the event."""

  def __init__(self, game):
    self.game = game
    self.orders = parse_orders(config.POTION_SHOP_BOTTLES)
    self.event = _event_start()
    self.bottled = _load_bottled(self.event)
    self.cauldron_timer = Timer()

  def run(self):
    """Brew and bottle until all orders are done (True) or the bot is
    no longer inside the event (False)."""
    outside = 0
    while outside < OUTSIDE_LOOPS:
      name = self._next_potion()
      if name is None:
        if self.orders:
          key_log.info('POTION SHOP - All ordered potions bottled')
        return True
      self.game.screen.capture()
      if potion_shop.is_inside(self.game):
        outside = 0
        self.play_once(name)
      else:
        outside += 1
        popups.close_popup(self.game)
    return False

  def play_once(self, name):
    """Brew or bottle the potion when the Cauldron is open or due."""
    game = self.game
    if not (potion_shop.is_cauldron_open(game)
            or self.cauldron_timer.is_due()):
      if popups.is_screen_dimmed(game):
        popups.close_popup(game)
      time.sleep(LOOP_DELAY_S)
      return
    self.cauldron_timer.postpone(CAULDRON_CHECK_S)
    keep = [order for order, _ in self.orders]
    if potion_shop.bottle_or_brew(game, name, keep) == 'bottled':
      self.bottled[name] = self.bottled.get(name, 0) + 1
      _save_bottled(self.event, self.bottled)
      count = dict(self.orders)[name]
      key_log.info('POTION SHOP - %s bottled %d/%d', name,
                   self.bottled[name], count)

  def _next_potion(self):
    """The first ordered potion not bottled often enough yet."""
    return next((name for name, count in self.orders
                 if self.bottled.get(name, 0) < count), None)


def _event_start():
  """The Saturday the current event (Saturday-Tuesday) started, as
  text."""
  today = datetime.date.today()
  saturday = today - datetime.timedelta(days=(today.weekday() - 5) % 7)
  return saturday.isoformat()


def _load_bottled(event):
  """{potion: count} bottled in this event so far."""
  try:
    with open(BOTTLES_FILE, encoding='utf-8') as file:
      state = json.load(file)
  except (OSError, ValueError):
    return {}
  return state.get('bottled', {}) if state.get('event') == event else {}


def _save_bottled(event, bottled):
  with open(BOTTLES_FILE, 'w', encoding='utf-8') as file:
    json.dump({'event': event, 'bottled': bottled}, file)

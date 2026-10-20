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
  """[(potion, count)] of "swift:max,golden:2,divine:1"; count None
  ("max") means brewed to its max level and kept, not bottled. Unknown
  potions and bad counts are skipped with a warning."""
  orders = []
  for item in text.split(','):
    if not item.strip():
      continue
    name, _, count = item.partition(':')
    name = name.strip().lower()
    count = count.strip().lower() or '1'
    if count == 'max':
      count = None
    else:
      try:
        count = int(count)
      except ValueError:
        count = 0
    if name not in potion_shop.POTIONS or count is not None and count < 1:
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
    # Indexes of the "max" orders whose potion reached its max level
    self.maxed = set()
    self.cauldron_timer = Timer()

  def run(self):
    """Brew and bottle until all orders are done (True) or the bot is
    no longer inside the event (False)."""
    outside = 0
    while outside < OUTSIDE_LOOPS:
      index = self._next_order()
      if index is None:
        if self.orders:
          key_log.info('POTION SHOP - All ordered potions done')
        return True
      self.game.screen.capture()
      if potion_shop.is_inside(self.game):
        outside = 0
        self.play_once(index)
      else:
        outside += 1
        popups.close_popup(self.game)
    return False

  def play_once(self, index):
    """Brew or bottle the potion of the order when the Cauldron is open
    or due."""
    game = self.game
    if not (potion_shop.is_cauldron_open(game)
            or self.cauldron_timer.is_due()):
      if popups.is_screen_dimmed(game):
        popups.close_popup(game)
      time.sleep(LOOP_DELAY_S)
      return
    self.cauldron_timer.postpone(CAULDRON_CHECK_S)
    name, count = self.orders[index]
    keep = [order for order, _ in self.orders]
    result = potion_shop.bottle_or_brew(game, name, keep,
                                        bottle=count is not None)
    if result == 'max':
      self.maxed.add(index)
      key_log.info('POTION SHOP - %s at its max level, kept', name)
    elif result == 'bottled':
      self.bottled[name] = self.bottled.get(name, 0) + 1
      _save_bottled(self.event, self.bottled)
      total = sum(order_count or 0 for order, order_count in self.orders
                  if order == name)
      key_log.info('POTION SHOP - %s bottled %d/%d', name,
                   self.bottled[name], total)

  def _next_order(self):
    """Index of the first order not done yet: a "max" order until its
    potion reaches its max level, else until the potion was bottled as
    often as the orders up to this one want."""
    wanted = {}
    for index, (name, count) in enumerate(self.orders):
      if count is None:
        if index not in self.maxed:
          return index
        continue
      wanted[name] = wanted.get(name, 0) + count
      if self.bottled.get(name, 0) < wanted[name]:
        return index
    return None


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

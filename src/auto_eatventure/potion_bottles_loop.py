"""PotionBottlesLoop: after the Potion Shop's rewards, brews the speed
potions to their max level and bottles the potions ordered in
potion_orders.txt (to use them outside the event); in the event's last
hour bottles all active potions."""

import datetime
import logging
import time

from auto_eatventure import potion_orders
from auto_eatventure.actions import (
  popups, potion_shop, potion_shop_cauldron)
from auto_eatventure.logger import key_log
from auto_eatventure.timer import Timer

log = logging.getLogger(__name__)

# Potions that make brewing faster: always brewed to their max level and
# kept active; their bottles are done last (a bottle sets the level back
# to 1), each followed by a brew back to the max level
SPEED_POTIONS = ('swift', 'instant', 'double')
# The Cauldron is looked at this often (a brew takes ~3 min; "Brew
# Complete!" also opens it by itself)
CAULDRON_CHECK_S = 30
LOOP_DELAY_S = 1
# Screenshots outside the event in a row that end the loop
OUTSIDE_LOOPS = 3
# The event runs from Saturday 00:00 to Wednesday 00:00 (local time; the
# countdown of its button)
EVENT_START_WEEKDAY = 5
EVENT_DAYS = 4
# The active potions are lost with the event: they are bottled this
# long before its end
FINAL_BOTTLES_S = 60 * 60


def seconds_to_final_bottles():
  """Seconds until the active potions are bottled (FINAL_BOTTLES_S
  before the end of the current event; <= 0: now)."""
  now = datetime.datetime.now()
  start = (now - datetime.timedelta(
    days=(now.weekday() - EVENT_START_WEEKDAY) % 7)).replace(
      hour=0, minute=0, second=0, microsecond=0)
  # Local times made aware: a summer time change is counted
  end = (start + datetime.timedelta(days=EVENT_DAYS)).astimezone()
  return (end - now.astimezone()).total_seconds() - FINAL_BOTTLES_S


def next_task(orders, maxed):
  """(potion, bottle) of the next step: a speed potion not at its max
  level yet (brewed and kept), else the first ordered potion that isn't
  a speed potion, else the first ordered speed potion (bottled). None
  when all is done."""
  for name in SPEED_POTIONS:
    if name not in maxed:
      return name, False
  ordered = [name for name, count in orders.items() if count > 0]
  for name in ordered:
    if name not in SPEED_POTIONS:
      return name, True
  return (ordered[0], True) if ordered else None


class PotionBottlesLoop:
  """Brews the speed potions to their max level, then brews and bottles
  the ordered potions one after another while the bot is inside the
  event."""

  def __init__(self, game):
    self.game = game
    # Speed potions found at their max level (bottling one removes it)
    self.maxed = set()
    self.cauldron_timer = Timer()
    self.orders = {}
    self.orders_text = None

  def run(self):
    """Brew and bottle until all is done (True) or the bot is no longer
    inside the event (False); in the event's last hour bottle all
    active potions instead."""
    outside = 0
    while outside < OUTSIDE_LOOPS:
      if seconds_to_final_bottles() <= 0:
        key_log.info('POTION SHOP - Event ends soon, bottling all')
        potion_shop_cauldron.bottle_all(
          self.game, 'before the event ends')
        return True
      self._read_orders()
      task = next_task(self.orders, self.maxed)
      if task is None:
        key_log.info('POTION SHOP - All ordered potions done')
        return True
      self.game.screen.capture()
      if potion_shop.is_inside(self.game):
        outside = 0
        self.play_once(*task)
      else:
        outside += 1
        popups.close_popup(self.game)
    return False

  def play_once(self, name, bottle):
    """Brew or bottle the potion when the Cauldron is open or due."""
    game = self.game
    if not (potion_shop_cauldron.is_cauldron_open(game)
            or self.cauldron_timer.is_due()):
      if popups.is_screen_dimmed(game):
        popups.close_popup(game)
      time.sleep(LOOP_DELAY_S)
      return
    self.cauldron_timer.postpone(CAULDRON_CHECK_S)
    keep = SPEED_POTIONS + tuple(
      order for order, count in self.orders.items() if count > 0)
    result = potion_shop_cauldron.bottle_or_brew(
      game, name, keep, bottle=bottle)
    if result == 'max':
      self.maxed.add(name)
      key_log.info('POTION SHOP - %s at its max level, kept', name)
    elif result == 'bottled':
      self.maxed.discard(name)
      left = potion_orders.lower_order(name)
      key_log.info('POTION SHOP - %s bottled, %s left', name,
                   0 if left is None else left)

  def _read_orders(self):
    """Read the orders file (parsed and logged when its text
    changed)."""
    text = potion_orders.read_text()
    if text == self.orders_text:
      return
    self.orders_text = text
    self.orders = potion_orders.parse_orders(text)
    log.info('Potion Shop orders: %s', {
      name: count for name, count in self.orders.items() if count > 0}
      or 'none')

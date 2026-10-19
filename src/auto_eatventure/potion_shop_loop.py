"""PotionShopLoop: plays the Potion Shop event while the bot is inside
it."""

import logging
import time

from auto_eatventure.actions import popups, potion_shop, stations, upgrades
from auto_eatventure.logger import key_log
from auto_eatventure.timer import Timer

log = logging.getLogger(__name__)

# Crates are looked for every this many loops
CRATE_CHECK_LOOPS = 2
# The map is scrolled back to the shop when its landmark was out of
# place (or hidden) in this many loops in a row
MISPLACED_LOOPS = 2
# The Cauldron's badge may stay while nothing can be brewed (e.g. a
# potion is brewing); then it is looked at again only after this time
BREW_RETRY_S = 60
# A red station icon next to the Upgrades button looks like its badge;
# when nothing could be bought the badge is ignored for this time
UPGRADES_RETRY_S = 60
# Screenshots outside the event in a row that end the loop (the event
# ended or the game left it)
OUTSIDE_LOOPS = 3


class PotionShopLoop:
  """Plays the event: one screenshot per loop, then the first thing to
  do on it. The map stays scrolled to the shop with its stations."""

  def __init__(self, game):
    self.game = game
    self.loops = 0
    self.misplaced_loops = 0
    self.brew_timer = Timer()
    self.upgrades_timer = Timer()

  def run(self):
    """Play until the bot is no longer inside the event."""
    key_log.info('POTION SHOP - Playing the event')
    potion_shop.show_shop(self.game)
    outside = 0
    while outside < OUTSIDE_LOOPS:
      self.game.screen.capture()
      if potion_shop.is_inside(self.game):
        outside = 0
        self.play_once()
      else:
        outside += 1
        popups.close_popup(self.game)
    key_log.info('POTION SHOP - Left the event')

  def play_once(self):
    """One loop on the current screenshot."""
    game = self.game
    self.loops += 1
    if potion_shop.is_cauldron_open(game):
      potion_shop.brew(game)
      return
    if popups.is_screen_dimmed(game):
      if not popups.close_popup(game):
        self._close_unknown_dialog()
      return
    if potion_shop.can_brew(game) and self.brew_timer.is_due():
      if not potion_shop.brew(game):
        self.brew_timer.postpone(BREW_RETRY_S)
      return
    if (upgrades.has_badge(game) and self.upgrades_timer.is_due()
        and not upgrades.buy_if_available(game)):
      self.upgrades_timer.postpone(UPGRADES_RETRY_S)
    if (self.loops % CRATE_CHECK_LOOPS == 0
        and potion_shop.open_crates(game)):
      return
    if self._shop_misplaced():
      potion_shop.show_shop(game)
      return
    icons = stations.find_icons(game)
    if icons:
      stations.upgrade(game, icons)

  def _shop_misplaced(self):
    """Whether the map was moved away from the shop (e.g. by a tap
    that scrolled it) for MISPLACED_LOOPS loops."""
    offset = potion_shop.shop_offset(self.game)
    aligned = self.game.coords.potion_shop_aligned_y
    if offset is not None and abs(offset) <= aligned:
      self.misplaced_loops = 0
      return False
    self.misplaced_loops += 1
    return self.misplaced_loops >= MISPLACED_LOOPS

  def _close_unknown_dialog(self):
    """A dialog without the usual red X: tap its usual X places."""
    log.info('Potion Shop: closing an unknown dialog')
    self.game.device.tap(self.game.coords.potion_shop_dialog_close)
    time.sleep(1)

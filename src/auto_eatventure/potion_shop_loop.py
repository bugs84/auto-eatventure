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
# The Cauldron's red badge shows when a brewed potion is done (while
# brewing the kettle shows the ingredients it still needs). It fades
# out for a while after a new brew, and the finished potion's Claim
# shows a moment after the badge: so the badge is ignored for
# BREW_PAUSE_S after a brew and looked at again after BREW_RETRY_S
# when the Cauldron had nothing to do.
BREW_PAUSE_S = 20
BREW_RETRY_S = 15
# The badge also shows when the plan has nothing more to brew: after
# IDLE_BREWS checks in a row without a brew it is looked at only every
# IDLE_BREW_S
IDLE_BREWS = 3
IDLE_BREW_S = 5 * 60
# A red station icon next to the Upgrades button looks like its badge;
# when nothing could be bought the badge is ignored for this time
UPGRADES_RETRY_S = 60
# Every CELLAR_CHECK_S the map is scrolled to the cellar for
# CELLAR_LOOPS loops of crates and station upgrades there
CELLAR_CHECK_S = 60
CELLAR_LOOPS = 3
# The rewards are looked at (Exit when all are done) right away and
# then every COMPLETION_CHECK_S
COMPLETION_CHECK_S = 15 * 60
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
    self.idle_brews = 0
    self.brew_timer = Timer()
    self.upgrades_timer = Timer()
    self.cellar_timer = Timer()
    self.completion_timer = Timer()
    self.completed = False

  def run(self):
    """Play until the bot is no longer inside the event. Returns True
    when it left because all rewards were done."""
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
    return self.completed

  def play_once(self):
    """One loop on the current screenshot."""
    game = self.game
    self.loops += 1
    if self._handle_dialog():
      return
    if self.completion_timer.is_due():
      self.completion_timer.postpone(COMPLETION_CHECK_S)
      self.completed = potion_shop.leave_if_completed(game)
      return
    if potion_shop.can_brew(game) and self.brew_timer.is_due():
      self._brew()
      return
    if (upgrades.has_badge(game) and self.upgrades_timer.is_due()
        and not upgrades.buy_if_available(game)):
      self.upgrades_timer.postpone(UPGRADES_RETRY_S)
    if (self.loops % CRATE_CHECK_LOOPS == 0
        and potion_shop.open_crates(game)):
      return
    if self.cellar_timer.is_due():
      self.cellar_timer.postpone(CELLAR_CHECK_S)
      self._play_cellar()
      return
    if self._shop_misplaced():
      potion_shop.show_shop(game)
      return
    icons = stations.find_icons(game)
    if icons:
      stations.upgrade(game, icons)
    else:
      # The shop's stations are MAX (level 1000) or too expensive
      self.cellar_timer.reset()

  def _handle_dialog(self):
    """Brew in the Cauldron dialog (it also opens by itself) or close
    another dialog. Returns True when one was open."""
    game = self.game
    if potion_shop.is_cauldron_open(game):
      if potion_shop.brew(game):
        self.brew_timer.postpone(BREW_PAUSE_S)
      return True
    if popups.is_screen_dimmed(game):
      if not popups.close_popup(game):
        self._close_unknown_dialog()
      return True
    return False

  def _brew(self):
    """Claim and brew; looked at again sooner after a brew."""
    if potion_shop.brew(self.game):
      self.idle_brews = 0
      self.brew_timer.postpone(BREW_PAUSE_S)
      return
    self.idle_brews += 1
    self.brew_timer.postpone(
      IDLE_BREW_S if self.idle_brews >= IDLE_BREWS else BREW_RETRY_S)

  def _play_cellar(self):
    """Open the crates and upgrade the stations of the cellar, then
    back to the shop."""
    game = self.game
    if potion_shop.show_cellar(game):
      for _ in range(CELLAR_LOOPS):
        game.screen.capture()
        potion_shop.open_crates(game)
        icons = stations.find_icons(game)
        if not icons:
          break
        stations.upgrade(game, icons)
    potion_shop.show_shop(game)

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

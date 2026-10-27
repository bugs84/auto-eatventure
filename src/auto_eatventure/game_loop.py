"""GameLoop: the endless loop deciding what the bot does next."""

import logging

from auto_eatventure import config
from auto_eatventure.actions import (
  adventures, boxes, food_delivery, helper_invite, levels, popular_dish,
  popups, start_dialogs, stations, upgrades)
from auto_eatventure.actions.stale import StaleWatch
from auto_eatventure.actions.start_dialogs import LateDialogWatch
from auto_eatventure.logger import key_log
from auto_eatventure.potion_shop_loop import PotionShopWatch
from auto_eatventure.timer import Timer

log = logging.getLogger(__name__)

# Every this many loops: popups closed, the next level checked (when
# there is no station to upgrade), boxes opened
POPUP_CHECK_LOOPS = 150
NEXT_LEVEL_CHECK_LOOPS = 10
BOX_CHECK_LOOPS = 2
# Unexpected errors in a row (no loop played without one between them)
# that are recovered from by bringing the game back; the next one ends
# the bot. E.g. the game crashed and the bot tapped the home screen.
RECOVERY_TRIES = 2


class GameLoop:
  """Plays the game: one screenshot per loop, then the first thing to
  do on it."""

  def __init__(self, game):
    self.game = game
    self.loops = 0
    self.stale = StaleWatch()
    self.late_dialogs = LateDialogWatch()
    # The first station icons of a level move the restaurant into place
    self.needs_reposition = True
    self.popular_dish_timer = Timer()
    # After a level change no dish can be selected until the first
    # stand is open, i.e. until the first station upgrade
    self.popular_dish_waits_for_upgrade = False
    self.food_delivery_timer = Timer()
    self.helper_invite_timer = Timer()
    self.adventures_timer = Timer()
    self.potion_shop = PotionShopWatch()

  def run(self):
    """Play until stopped; after an unexpected error the game is
    brought back (_recover()) up to RECOVERY_TRIES times in a row."""
    errors = 0
    while True:
      try:
        self.play_once()
        errors = 0
      except Exception:  # pylint: disable=broad-exception-caught
        errors += 1
        if errors > RECOVERY_TRIES:
          raise
        self._recover(errors)

  def _recover(self, errors):
    """After an unexpected error: log it, bring the game back to the
    foreground (started again when it crashed) and wait until it is
    playable."""
    log.exception('Unexpected error (%d of %d tries), bringing the game '
                  'back to the foreground', errors, RECOVERY_TRIES)
    key_log.error('ERROR - Unexpected error, recovering (%d/%d), see '
                  'autoplay.log', errors, RECOVERY_TRIES)
    self.game.device.start_app()
    start_dialogs.wait_until_ready(self.game)
    self.needs_reposition = True

  def play_once(self):
    """One loop: a new screenshot and the actions it calls for. An
    action that changes the screen a lot ends the loop early."""
    game = self.game
    self.loops += 1
    self.stale.check(game)

    if (config.POPULAR_DISH_ENABLED
        and not self.popular_dish_waits_for_upgrade
        and self.popular_dish_timer.is_due()):
      self._select_popular_dish()
    if config.COLLECT_ADVENTURES_ENABLED and self.adventures_timer.is_due():
      self._collect_adventures()

    game.screen.capture()
    if self.late_dialogs.close_dialogs(game):
      return
    if config.POTION_SHOP_ENABLED and self._play_potion_shop():
      return
    if (config.FOOD_DELIVERY_ENABLED and self.food_delivery_timer.is_due()
        and self._accept_food_delivery()):
      return
    if (config.HELPER_INVITE_ENABLED and self.helper_invite_timer.is_due()
        and self._invite_helper()):
      return

    if self.loops % POPUP_CHECK_LOOPS == 0:
      popups.close_popup(game)
    upgrades.buy_if_available(game)
    if self.loops == 1 or self.loops % BOX_CHECK_LOOPS == 0:
      boxes.open_all(game)

    icons = stations.find_icons(game)
    if icons:
      self._upgrade_stations(icons)
    else:
      self._no_station_to_upgrade()

  def _upgrade_stations(self, icons):
    if self.needs_reposition:
      stations.reposition_after_new_level(self.game, icons)
      self.needs_reposition = False
      return
    self.stale.found_work()
    if stations.scroll_if_icons_too_high(self.game, icons):
      return
    stations.upgrade(self.game, icons)
    if self.popular_dish_waits_for_upgrade:
      self.popular_dish_waits_for_upgrade = False
      self.popular_dish_timer.reset()

  def _no_station_to_upgrade(self):
    self.stale.found_nothing()
    if (self.loops % NEXT_LEVEL_CHECK_LOOPS == 0
        and levels.go_to_next_level(self.game)):
      self.stale.reset()
      self.needs_reposition = True
      self.popular_dish_waits_for_upgrade = True

  def _select_popular_dish(self):
    selected = popular_dish.select(self.game)
    self.popular_dish_timer.postpone(
      popular_dish.COOLDOWN_S if selected else popular_dish.RETRY_S)

  def _collect_adventures(self):
    finished = adventures.collect(self.game)
    self.adventures_timer.postpone(
      adventures.INTERVAL_S if finished else adventures.RETRY_S)

  def _accept_food_delivery(self):
    """Returns True when a delivery was available (and tried)."""
    truck = food_delivery.find_truck(self.game)
    if truck is None:
      return False
    food_delivery.accept(self.game, truck)
    self.food_delivery_timer.postpone(food_delivery.PAUSE_S)
    return True

  def _play_potion_shop(self):
    """Returns True when the bot was in the Potion Shop event (played
    until it left it): the restaurant is then found again."""
    if not self.potion_shop.play_if_due(self.game):
      return False
    self.stale.reset()
    self.needs_reposition = True
    return True

  def _invite_helper(self):
    """Returns True when a helper was available (and tried)."""
    if not helper_invite.is_available(self.game):
      return False
    invited = helper_invite.invite(self.game)
    self.helper_invite_timer.postpone(
      helper_invite.PAUSE_S if invited else helper_invite.RETRY_S)
    return True

"""The Potion Shop event, apart from the city's GameLoop:
PotionShopWatch (GameLoop's hook) looks for it and enters it,
PotionShopLoop plays it while the bot is inside it."""

import logging
import time

from auto_eatventure import potion_bottles_loop
from auto_eatventure.actions import (
  popups, potion_shop, potion_shop_cauldron, potion_shop_map, stations)
from auto_eatventure.logger import key_log
from auto_eatventure.potion_bottles_loop import PotionBottlesLoop
from auto_eatventure.potion_shop_planner import Planner
from auto_eatventure.timer import Timer

log = logging.getLogger(__name__)

# The event (weekly) is looked for this often; once all its rewards are
# done it is entered again only in its last hour (all active potions
# bottled), or after EVENT_DONE_S when that hour has begun
EVENT_CHECK_S = 30 * 60
EVENT_DONE_S = 24 * 60 * 60
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
# The badge may be gone while the Cauldron is idle and could brew (e.g.
# after the dialog was seen once): it is opened after this time without
# a look anyway
CAULDRON_CHECK_S = 5 * 60
# "+N Customer(s)" upgrades bought before brewing is done: the first two
# (cheap, needed at the start); the rest after the last brew (video)
EARLY_CUSTOMER_ROWS = 2
# The other view (shop, cellar) is looked at for crates this often
OTHER_VIEW_S = 15 * 60
# The rewards are looked at (when all are done: bottling, then Exit)
# right away and then every COMPLETION_CHECK_S
COMPLETION_CHECK_S = 15 * 60
# Station levels and the Upgrades dialog's rows are bought by
# potion_shop_planner.py from the numbers read: each station's popup
# (once, then after each purchase; unreadable ones again after
# UNREAD_RETRY_S, all of them every SURVEY_S) and the dialog's rows
# (once, then every UPGRADES_READ_S: the user may buy some).
UNREAD_RETRY_S = 10 * 60
SURVEY_S = 60 * 60
UPGRADES_READ_S = 30 * 60
# Screenshots outside the event in a row that end the loop (the event
# ended or the game left it)
OUTSIDE_LOOPS = 3


class PotionShopWatch:
  """GameLoop's hook: looks for the event every EVENT_CHECK_S, enters
  it and plays it (PotionShopLoop)."""

  def __init__(self):
    self._timer = Timer()

  def play_if_due(self, game):
    """When due, enter the event (unless inside) and play it until the
    bot is no longer inside. Returns True when the bot was inside."""
    if not self._timer.is_due():
      return False
    self._timer.postpone(EVENT_CHECK_S)
    if not (potion_shop.is_inside(game)
            or (potion_shop.is_available(game) and potion_shop.enter(game))):
      return False
    if PotionShopLoop(game).run():
      final = potion_bottles_loop.seconds_to_final_bottles()
      self._timer.postpone(final if final > 0 else EVENT_DONE_S)
    return True


class PotionShopLoop:
  """Plays the event: one screenshot per loop, then the first thing to
  do on it. The map stays at the shop or the cellar view (its
  stations), whichever the coins are spent on."""

  def __init__(self, game):
    self.game = game
    self.loops = 0
    self.misplaced_loops = 0
    self.cauldron = CauldronWatch()
    self.other_view_timer = Timer()
    self.other_view_timer.postpone(OTHER_VIEW_S)
    self.completion_timer = Timer()
    self.completed = False
    # Customer rows that may still be bought; None (no limit) once all
    # of potion_shop_cauldron.LATE_PLAN is brewed
    self.customer_rows_left = EARLY_CUSTOMER_ROWS
    self.plan = StationPlan(game)

  def run(self):
    """Play until the bot is no longer inside the event or all rewards
    are done; then the ordered potions are bottled
    (PotionBottlesLoop) and the bot leaves. Returns True when all
    rewards were done."""
    key_log.info('POTION SHOP - Playing the event')
    potion_shop_map.show_shop(self.game)
    outside = 0
    while outside < OUTSIDE_LOOPS and not self.completed:
      self.game.screen.capture()
      if potion_shop.is_inside(self.game):
        outside = 0
        self.play_once()
      elif not potion_shop.close_outside_dialog(self.game):
        outside += 1
    if (self.completed and PotionBottlesLoop(self.game).run()
        and not potion_shop.leave(self.game)):
      log.warning('Potion Shop: Exit did not leave the event')
    key_log.info('POTION SHOP - Left the event')
    return self.completed

  def play_once(self):
    """One loop on the current screenshot."""
    game = self.game
    self.loops += 1
    if self._handle_dialog():
      return
    reason = self.cauldron.reason(game)
    if reason is not None:
      self.cauldron.note(self._brewed(potion_shop_cauldron.brew(game)),
                         reason == 'badge')
      return
    if (self.loops % CRATE_CHECK_LOOPS == 0
        and potion_shop_map.open_crates(game)):
      return
    view = self._view()
    if view is None or self._play_occasional(view):
      return
    left = self.customer_rows_left
    bought = self.plan.play(view, left is None or left > 0)
    if bought == 'customer' and left is not None:
      self.customer_rows_left = left - 1

  def _play_occasional(self, view):
    """The rewards check, a look at the other view (its crates) or an
    unlock of a new station. Returns True when one was played."""
    if self.completion_timer.is_due():
      self.completion_timer.postpone(COMPLETION_CHECK_S)
      self.completed = potion_shop.is_completed(self.game)
      return True
    if self.other_view_timer.is_due():
      self.other_view_timer.postpone(OTHER_VIEW_S)
      self._show('shop' if view == 'cellar' else 'cellar')
      return True
    return self._unlock_stations(view)

  def _view(self):
    """The view shown ('shop' or 'cellar'); None when the map was moved
    away (scrolled back to the shop after MISPLACED_LOOPS loops)."""
    view = potion_shop_map.current_view(self.game)
    if view is not None:
      self.misplaced_loops = 0
      return view
    self.misplaced_loops += 1
    if self.misplaced_loops >= MISPLACED_LOOPS:
      potion_shop_map.show_shop(self.game)
    return None

  def _show(self, view):
    if view == 'cellar':
      potion_shop_map.show_cellar(self.game)
    else:
      potion_shop_map.show_shop(self.game)

  def _unlock_stations(self, view):
    """Tap the arrows over dashed tiles (new stations) of the view.
    Returns True when one was tapped."""
    game = self.game
    icons = (potion_shop_map.shop_icons(game) if view == 'shop'
             else stations.find_icons(game))
    locked = [icon for icon in icons
              if potion_shop_map.is_locked(game, icon)]
    if not locked:
      return False
    stations.upgrade(game, locked)
    if view == 'cellar':
      potion_shop_map.close_cellar_popup(game)
    return True

  def _handle_dialog(self):
    """Brew in the Cauldron dialog (it also opens by itself) or close
    another dialog. Returns True when one was open."""
    game = self.game
    if potion_shop_cauldron.is_cauldron_open(game):
      self.cauldron.note(self._brewed(potion_shop_cauldron.brew(game)),
                         False)
      return True
    if popups.is_screen_dimmed(game):
      if not popups.close_popup(game):
        self._close_unknown_dialog()
      return True
    return False

  def _brewed(self, result):
    """Note a 'done' of potion_shop_cauldron.brew(). Returns True when
    a potion was brewed."""
    if result == 'done' and self.customer_rows_left is not None:
      self.customer_rows_left = None
      key_log.info('POTION SHOP - Brewing done, buying customers')
    return result == 'brewed'

  def _close_unknown_dialog(self):
    """A dialog without the usual red X: tap its usual X places."""
    log.info('Potion Shop: closing an unknown dialog')
    self.game.device.tap(self.game.coords.potion_shop_dialog_close)
    time.sleep(1)


class CauldronWatch:
  """When to open the Cauldron: on its badge (see BREW_PAUSE_S and
  IDLE_BREWS) and after CAULDRON_CHECK_S without a look."""

  def __init__(self):
    self.idle_brews = 0
    self.badge_timer = Timer()
    self.check_timer = Timer()

  def reason(self, game):
    """'badge', 'check' or None (not now)."""
    if (potion_shop_cauldron.can_brew(game)
        and self.badge_timer.is_due()):
      return 'badge'
    return 'check' if self.check_timer.is_due() else None

  def note(self, brewed, badge):
    """Note a look into the Cauldron (badge: for its badge); looked at
    again sooner after a brew."""
    self.check_timer.postpone(CAULDRON_CHECK_S)
    if brewed:
      self.idle_brews = 0
      self.badge_timer.postpone(BREW_PAUSE_S)
    elif badge:
      self.idle_brews += 1
      self.badge_timer.postpone(
        IDLE_BREW_S if self.idle_brews >= IDLE_BREWS else BREW_RETRY_S)


class StationPlan:
  """Buys what potion_shop_planner.Planner chooses: a station's levels
  (taps on its popup's button, its view scrolled to) or a row of the
  Upgrades dialog; waits (saves the coins) while it can't be paid."""

  def __init__(self, game):
    self.game = game
    self.planner = Planner()
    self.upgrades_timer = Timer()
    self.survey_timer = Timer()
    # Station -> Timer: when to read its popup again (unread ones)
    self.unread_timers = {}
    self.waiting_for = None

  def play(self, view, customers):
    """Read what is to be read on the view or buy the choice. Returns
    the kind of the row bought ('customer', ...), 'level', 'read'
    (the screen changed) or None (nothing done)."""
    game = self.game
    planner = self.planner
    if planner.upgrades is None or self.upgrades_timer.is_due():
      self.upgrades_timer.postpone(UPGRADES_READ_S)
      planner.upgrades = potion_shop.read_upgrades(game)
      return 'read'
    if self.survey_timer.is_due():
      self.survey_timer.postpone(SURVEY_S)
      self.unread_timers = {}
    if self._read_unread(view):
      return 'read'
    coins = game.screen.read_coins(game.coords)
    if coins is None:
      return None
    here = [name for name in potion_shop.STATIONS
            if potion_shop_map.view_of(name) == view]
    choice = planner.choice(coins, customers, here)
    if choice is None:
      return None
    if choice.kind == 'upgrade':
      return self._buy_upgrade(choice, coins)
    return self._buy_levels(choice.station, coins, customers, view)

  def _read_unread(self, view):
    """Read the popups of the view's stations not read yet (again after
    UNREAD_RETRY_S when unreadable). Returns True when one was read."""
    names = [name for name in potion_shop.STATIONS
             if potion_shop_map.view_of(name) == view
             and name not in self.planner.stations
             and name not in self.planner.maxed
             and self.unread_timers.setdefault(name, Timer()).is_due()]
    for name in names:
      popup = potion_shop_map.read_station(self.game, name)
      log.debug('Potion Shop: %s %s', name, popup)
      if popup is None:
        self.unread_timers[name].postpone(UNREAD_RETRY_S)
      else:
        self.planner.station_read(name, popup)
    return bool(names)

  def _buy_upgrade(self, choice, coins):
    upgrade = choice.upgrade
    if choice.cost > coins:
      self._wait(f'{upgrade.title} ({upgrade.price})')
      return None
    if potion_shop.buy_upgrade(self.game, upgrade):
      self.planner.upgrade_bought(upgrade)
      return upgrade.kind
    # Not found or grey: the dialog is read again
    self.planner.upgrades = None
    return 'read'

  def _buy_levels(self, name, coins, customers, view):
    """Buy the levels of the station that pay off now (scrolled to its
    view first)."""
    game = self.game
    station = self.planner.stations[name]
    if station.price > coins:
      self._wait(f'{name} level ({station.price:.3g})')
      return None
    if potion_shop_map.view_of(name) != view:
      if potion_shop_map.view_of(name) == 'cellar':
        potion_shop_map.show_cellar(game)
      else:
        potion_shop_map.show_shop(game)
      return 'read'
    popup = potion_shop_map.open_station(game, name)
    if popup is not None:
      self.planner.station_read(name, popup)
    count = (self.planner.levels_to_buy(name, coins, customers, (name,))
             if name in self.planner.stations else 0)
    if count:
      popup = potion_shop_map.buy_levels(game, name, count)
      log.info('Potion Shop: %s +%d levels (%s)', name, count, popup)
      if popup is not None:
        self.planner.station_read(name, popup)
      elif count < potion_shop_map.HOLD_MIN_LEVELS:
        self.planner.levels_bought(name, count)
      else:
        # Held: how many is unknown, read again
        del self.planner.stations[name]
        self.unread_timers.pop(name, None)
    potion_shop_map.close_station(game, name)
    self.waiting_for = None
    return 'level'

  def _wait(self, what):
    if what != self.waiting_for:
      log.info('Potion Shop: saving coins for %s', what)
      self.waiting_for = what

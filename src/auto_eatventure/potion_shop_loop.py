"""The Potion Shop event, apart from the city's GameLoop:
PotionShopWatch (GameLoop's hook) looks for it and enters it,
PotionShopLoop plays it while the bot is inside it."""

import logging
import os
import time

from auto_eatventure import potion_bottles_loop
from auto_eatventure.actions import (
  popups, potion_shop, potion_shop_cauldron, potion_shop_map, stations,
  upgrades)
from auto_eatventure.logger import key_log
from auto_eatventure.potion_bottles_loop import PotionBottlesLoop
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
# A red station icon next to the Upgrades button looks like its badge
# (and skipped customer rows keep it shown); when nothing could be
# bought the badge is ignored for this time
UPGRADES_RETRY_S = 60
# "+N Customer(s)" upgrades bought before brewing is done: the first two
# (cheap, needed at the start); the rest after the last brew (video)
EARLY_CUSTOMER_ROWS = 2
# Every CELLAR_CHECK_S the map is scrolled to the cellar for
# CELLAR_LOOPS loops of crates and station upgrades there
CELLAR_CHECK_S = 60
CELLAR_LOOPS = 3
# The rewards are looked at (when all are done: bottling, then Exit)
# right away and then every COMPLETION_CHECK_S
COMPLETION_CHECK_S = 15 * 60
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
# The station whose profit was multiplied last (Upgrades row "<station>
# profit xN") earns the most per level: only its arrow is tapped, the
# coins are saved for it, until it had no arrow for FOCUS_WAIT_S (MAX,
# or its levels cost more than a few minutes of income)
FOCUS_WAIT_S = 3 * 60
# The focus survives restarts (watchdog, low battery pause) in this
# file; one older than FOCUS_MAX_AGE_S is from an earlier event. The
# station's name may also be written there by hand (e.g. "bat").
FOCUS_FILE = 'logs/potion_shop_focus.txt'
FOCUS_MAX_AGE_S = 24 * 60 * 60
# In the end game (END_GAME_STATION MAX, looked at every
# END_GAME_CHECK_S) the focused station's last upgrade (bought yet?)
# and, without an arrow, its MAX are looked at again STATION_CHECK_S
# after a "not yet"; after a yes the next check follows right away
# (after a restart the bot passes the MAX stations in seconds)
END_GAME_CHECK_S = 5 * 60
STATION_CHECK_S = 60
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
  do on it. The map stays scrolled to the shop with its stations."""

  def __init__(self, game):
    self.game = game
    self.loops = 0
    self.misplaced_loops = 0
    self.cauldron = CauldronWatch()
    self.upgrades_timer = Timer()
    self.cellar_timer = Timer()
    self.completion_timer = Timer()
    self.completed = False
    # Customer rows that may still be bought; None (no limit) once all
    # of potion_shop_cauldron.LATE_PLAN is brewed
    self.customer_rows_left = EARLY_CUSTOMER_ROWS
    self.end_game = EndGame(game)
    self.focus = StationFocus(game)

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
    if upgrades.has_badge(game) and self.upgrades_timer.is_due():
      self._buy_upgrades()
    if (self.loops % CRATE_CHECK_LOOPS == 0
        and potion_shop_map.open_crates(game)):
      return
    if self._play_occasional():
      return
    if self._shop_misplaced():
      potion_shop_map.show_shop(game)
      return
    if not self.focus.upgrade(potion_shop_map.shop_icons(game),
                              cellar=False):
      # Nothing to wait for here (the shop's stations are MAX or too
      # expensive, or the focused station is in the cellar)
      self.cellar_timer.reset()

  def _play_occasional(self):
    """The rewards check, the end game or a cellar visit. Returns True
    when one was played."""
    if self.completion_timer.is_due():
      self.completion_timer.postpone(COMPLETION_CHECK_S)
      self.completed = potion_shop.is_completed(self.game)
      return True
    if self.end_game.play():
      return True
    if self.cellar_timer.is_due():
      self.cellar_timer.postpone(CELLAR_CHECK_S)
      self._play_cellar()
      return True
    return False

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

  def _buy_upgrades(self):
    """Buy the affordable upgrades; customer rows only the first
    EARLY_CUSTOMER_ROWS until brewing is done."""
    left = self.customer_rows_left
    kinds = potion_shop.buy_upgrades(
      self.game, potion_shop.MAX_UPGRADE_BUYS if left is None else left)
    if left is not None:
      self.customer_rows_left = left - kinds.count('customer')
    if not kinds:
      self.upgrades_timer.postpone(UPGRADES_RETRY_S)
    for kind in kinds:
      if kind in potion_shop.STATIONS:
        self.focus.set(kind)

  def _play_cellar(self):
    """Open the crates and upgrade the stations of the cellar, then
    back to the shop."""
    game = self.game
    if potion_shop_map.show_cellar(game):
      for _ in range(CELLAR_LOOPS):
        game.screen.capture()
        potion_shop_map.open_crates(game)
        if not self.focus.upgrade(stations.find_icons(game), cellar=True):
          break
    potion_shop_map.show_shop(game)

  def _shop_misplaced(self):
    """Whether the map was moved away from the shop (e.g. by a tap
    that scrolled it) for MISPLACED_LOOPS loops."""
    offset = potion_shop_map.shop_offset(self.game)
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


class EndGame:
  """The end game of PotionShopLoop: once END_GAME_STATION is MAX, only
  FOCUS_STATIONS are upgraded, one after another."""

  def __init__(self, game):
    self.game = game
    self.end_game_timer = Timer()
    self.station_check_timer = Timer()
    # Station name -> 'bought' (its last upgrade) or 'max'
    self.station_states = {}

  def play(self):
    """End game: upgrade only the first focused station that isn't MAX
    (in the cellar) once its last upgrade is bought, else wait for
    coins. Returns False while it isn't the end game or when all
    focused stations are MAX."""
    game = self.game
    if not self._is_end_game():
      return False
    name = next((name for name in FOCUS_STATIONS
                 if self.station_states.get(name) != 'max'), None)
    if name is None:
      return False
    if (name not in self.station_states
        and not self._is_last_upgrade_bought(name)):
      return True
    if not potion_shop_map.is_cellar_shown(game):
      potion_shop_map.show_cellar(game)
      return True
    arrow = potion_shop_map.station_arrow(game, name,
                                          stations.find_icons(game))
    if arrow is not None:
      stations.upgrade(game, [arrow])
      # Near the top of the screen stations.upgrade() closes the popup
      # by a tap beside the icon, which in the cellar opens it again;
      # the open popup hid the arrow
      potion_shop_map.close_cellar_popup(game)
    elif self.station_check_timer.is_due():
      if potion_shop_map.is_station_max(game, name):
        key_log.info('POTION SHOP - %s is MAX', name)
        self.station_states[name] = 'max'
      else:
        self.station_check_timer.postpone(STATION_CHECK_S)
    return True

  def _is_last_upgrade_bought(self, name):
    """Whether the station's last upgrade is bought (none for a station
    not in LAST_UPGRADES)."""
    if name in LAST_UPGRADES:
      if not self.station_check_timer.is_due():
        return False
      if potion_shop.has_last_upgrade(self.game, name):
        self.station_check_timer.postpone(STATION_CHECK_S)
        return False
      key_log.info('POTION SHOP - %s: last upgrade bought', name)
    self.station_states[name] = 'bought'
    return True

  def _is_end_game(self):
    """Whether END_GAME_STATION is MAX (looked at in the shop view
    every END_GAME_CHECK_S until it is)."""
    station = END_GAME_STATION
    if self.station_states.get(station) == 'max':
      return True
    if not self.end_game_timer.is_due():
      return False
    self.end_game_timer.postpone(END_GAME_CHECK_S)
    game = self.game
    if not (potion_shop_map.show_shop(game)
            and potion_shop_map.is_station_max(game, station)):
      return False
    key_log.info('POTION SHOP - End game: upgrading only %s',
                 ', '.join(FOCUS_STATIONS))
    self.station_states[station] = 'max'
    return True


class StationFocus:
  """Station upgrades: only the focused station's arrow (and unlocks of
  new stations) while it had one within FOCUS_WAIT_S, else (and without
  a focus) all arrows."""

  def __init__(self, game):
    self.game = game
    self.station = _read_focus()
    self.timer = Timer()
    if self.station is not None:
      log.info('Potion Shop: focus on %s (%s)', self.station, FOCUS_FILE)
      self.timer.postpone(FOCUS_WAIT_S)

  def set(self, station):
    """Focus on the station (its profit was just multiplied)."""
    if station != self.station:
      log.info('Potion Shop: focus on %s', station)
      _write_focus(station)
    self.station = station
    self.timer.postpone(FOCUS_WAIT_S)

  def upgrade(self, icons, cellar):
    """Tap the arrows (icons) of the cellar or the shop view. Returns
    False when there is nothing to wait for on this view (no arrow, the
    focused station is on the other one)."""
    game = self.game
    name = self.station
    locked = [icon for icon in icons
              if potion_shop_map.is_locked(game, icon)]
    if name is not None and locked:
      # New stations are unlocked whatever the focus
      stations.upgrade(game, locked)
      return True
    here = name is not None and (
      name in potion_shop_map.CELLAR_STATIONS) == cellar
    if here:
      arrow = potion_shop_map.station_arrow(game, name, icons)
      if arrow is not None:
        stations.upgrade(game, [arrow])
        if cellar:
          potion_shop_map.close_cellar_popup(game)
        self.timer.postpone(FOCUS_WAIT_S)
        return True
    if name is not None and not self.timer.is_due():
      # Coins saved for the focused station
      return here
    if icons:
      stations.upgrade(game, icons)
    return bool(icons)


def _read_focus():
  """The station in FOCUS_FILE; None when missing, old or unknown."""
  try:
    if time.time() - os.path.getmtime(FOCUS_FILE) > FOCUS_MAX_AGE_S:
      return None
    with open(FOCUS_FILE, encoding='utf-8') as file:
      station = file.read().strip()
  except OSError:
    return None
  return station if station in potion_shop.STATIONS else None


def _write_focus(station):
  try:
    with open(FOCUS_FILE, 'w', encoding='utf-8') as file:
      file.write(f'{station}\n')
  except OSError as error:
    log.warning('Potion Shop: focus not saved: %s', error)

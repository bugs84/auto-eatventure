"""What the Potion Shop's coins buy next: a station's levels or a row of
the Upgrades dialog, the one that pays for itself first (the time to
save its price plus the time its extra income takes to return it).

Measured on the LG (2026-10-26): a level multiplies a station's profit
by LEVEL_PROFIT and the next level's price by LEVEL_PRICE (all
stations); each star (every 100 levels from level 300 to MAX, level
1000) doubles the profit. The income is taken as proportional to the
sum of the stations' profits (customers order from all stations), so
a purchase raising a station's profit by G raises the income by G /
that sum."""

from collections import namedtuple
import math

from auto_eatventure.potion_shop_upgrades import PRICES, UPGRADES

LEVEL_PROFIT = 1.08
LEVEL_PRICE = 1.12
STAR_EVERY = 100
FIRST_STAR = 300
MAX_LEVEL = 1000
# A "faster" row counts like a profit x2 (its real effect is unknown)
FASTER_GAIN = 1.0
# Anything costing at most this share of the coins is bought anyway
# (finishes stations towards MAX)
CHEAP_SHARE = 0.001
# ... a cheap station's levels then while they cost at most this many
# times more (a few levels per popup opened)
CHEAP_BATCH = 4
# Levels bought in one go at most (taps on the open popup)
MAX_LEVELS = 30
# Scrolling to the other view (shop, cellar) takes a while: a choice
# here is taken while it pays for itself at most this many times later
# than the best one there
OTHER_VIEW_FACTOR = 1.5
# Its popup open, a station's next level is bought while it pays for
# itself at most this many times later than the best choice (else one
# level per popup: the best choice flips to saving for another one and
# back as soon as the coins grow)
OPEN_POPUP_FACTOR = 1.5

# kind: 'level' (station: levels of it, count: how many it pays to buy
# at once, cost: their price) or 'upgrade' (upgrade: the Upgrade)
Choice = namedtuple('Choice', 'kind station count upgrade cost')


class Station:
  """A station's numbers of its popup, updated by the levels bought
  (level None when unknown, profit None when unread)."""

  def __init__(self, profit, price, level):
    self.profit = profit
    self.price = price
    self.level = level

  def add_levels(self, count):
    """Count levels bought: their profit, stars and the next price."""
    for _ in range(count):
      if self.profit is not None:
        self.profit *= LEVEL_PROFIT
      self.price *= LEVEL_PRICE
      if self.level is not None:
        self.level += 1
        if self.level >= FIRST_STAR and self.level % STAR_EVERY == 0:
          if self.profit is not None:
            self.profit *= 2

  def maxed(self):
    return self.level is not None and self.level >= MAX_LEVEL

  def levels_cost(self, count):
    """The price of the next count levels."""
    return self.price * (LEVEL_PRICE ** count - 1) / (LEVEL_PRICE - 1)

  def levels_gain(self, count):
    """How much count more levels raise the profit."""
    after = Station(self.profit, self.price, self.level)
    after.add_levels(count)
    return after.profit - self.profit

  def to_star(self):
    """Levels to its next star, None when unknown (or no more)."""
    if self.level is None or self.level < FIRST_STAR - STAR_EVERY:
      return None
    left = STAR_EVERY - self.level % STAR_EVERY
    return min(left, MAX_LEVEL - self.level) or None


class Planner:
  """Stations (name -> Station; MAX ones are dropped) and the Upgrades
  dialog's rows not bought yet (None until read)."""

  def __init__(self):
    self.stations = {}
    self.maxed = set()
    self.upgrades = None

  def station_read(self, name, popup):
    """A station's popup was read (station_popup.StationPopup, 'max')."""
    if popup == 'max':
      self.maxed.add(name)
      self.stations.pop(name, None)
      return
    old = self.stations.get(name)
    level = popup.level
    if level is None and old is not None and old.level is not None:
      # Its level is under the top bar: known from the levels bought,
      # unless its price moved differently
      bought = round(_log(popup.price / old.price, LEVEL_PRICE))
      level = old.level + bought if bought >= 0 else None
    profit = popup.profit
    if profit is None and old is not None and old.profit is not None:
      bought = round(_log(popup.price / old.price, LEVEL_PRICE))
      if bought >= 0:
        moved = Station(old.profit, old.price, old.level)
        moved.add_levels(bought)
        profit = moved.profit
    self.stations[name] = Station(profit, popup.price, level)

  def levels_bought(self, name, count):
    """Count levels of the station were bought (its popup unread)."""
    station = self.stations[name]
    station.add_levels(count)
    if station.maxed():
      self.maxed.add(name)
      del self.stations[name]

  def upgrade_bought(self, upgrade):
    """A row of the Upgrades dialog was bought: gone from it, its
    station's profit multiplied."""
    if self.upgrades is not None and upgrade in self.upgrades:
      self.upgrades.remove(upgrade)
    station = self.stations.get(upgrade.station)
    if (upgrade.kind == 'profit' and station is not None
        and station.profit is not None):
      station.profit *= upgrade.multiplier

  def choice(self, coins, customers=True, here=()):
    """The Choice that pays for itself first with these coins (rows of
    customers only when customers; cheap levels of the stations here,
    on the view shown, first), None when nothing is known."""
    cheap = self._cheap(coins, customers, here)
    if cheap is not None:
      return cheap
    times = self._times(coins, customers)
    if not times:
      return None
    best_time, best = min(times, key=lambda item: item[0])
    local = [(time, choice) for time, choice in times
             if choice.kind == 'upgrade' or choice.station in here]
    if here and local and best not in [choice for _, choice in local]:
      time, choice = min(local, key=lambda item: item[0])
      if time <= best_time * OTHER_VIEW_FACTOR:
        return choice
    return best

  def levels_to_buy(self, name, coins, customers=True, here=()):
    """How many levels of the station to buy now with these coins:
    while they stay the choice (up to MAX_LEVELS)."""
    cheap = self._cheap(coins, customers, here)
    if cheap is not None and cheap.station == name:
      return cheap.count if cheap.kind == 'level' else 0
    planner = Planner()
    planner.upgrades = self.upgrades
    planner.stations = {
      key: Station(station.profit, station.price, station.level)
      for key, station in self.stations.items()}
    count = 0
    while count < MAX_LEVELS and name in planner.stations:
      station = planner.stations[name]
      times = planner._times(coins, customers)
      level = [time for time, choice in times
               if choice.kind == 'level' and choice.station == name
               and choice.count == 1]
      if (not level or station.price > coins
          or level[0] > OPEN_POPUP_FACTOR * min(t for t, _ in times)):
        break
      coins -= station.price
      planner.levels_bought(name, 1)
      count += 1
    return count

  def _times(self, coins, customers):
    """(Time to pay for itself, Choice) of the candidates."""
    total = sum(station.profit for station in self.stations.values()
                if station.profit is not None)
    times = []
    for choice, gain in self._candidates(customers):
      if gain is None:
        # Alchemists, the Kettle, the cellar: first, as soon as they
        # can be paid
        times.append((max(0.0, choice.cost - coins), choice))
      elif gain > 0:
        times.append((max(0.0, choice.cost - coins)
                      + choice.cost * total / gain, choice))
    return times

  def _cheap(self, coins, customers, here):
    """A Choice costing at most CHEAP_SHARE of the coins (the cheapest
    row, else the levels of a station here, else of another), None
    when none does."""
    limit = coins * CHEAP_SHARE
    rows = [Choice('upgrade', upgrade.station, 1, upgrade, price)
            for upgrade, price in self._rows(customers) if price <= limit]
    if rows:
      return min(rows, key=lambda row: row.cost)
    levels = []
    for name, station in self.stations.items():
      if station.price <= limit:
        count = min(MAX_LEVELS, 1 + int(_log(
          limit * CHEAP_BATCH / station.price, LEVEL_PRICE)))
        if station.level is not None:
          count = min(count, MAX_LEVEL - station.level)
        levels.append(Choice('level', name, count, None,
                             station.levels_cost(count)))
    return min(levels, default=None,
               key=lambda level: (level.station not in here, level.cost))

  def _candidates(self, customers):
    """(Choice, profit gain or None for a row bought first) of the
    levels and the rows."""
    for name, station in self.stations.items():
      if station.profit is None:
        continue
      counts = {1, station.to_star() or 1}
      for count in counts:
        yield (Choice('level', name, count, None,
                      station.levels_cost(count)),
               station.levels_gain(count))
    for upgrade, price in self._rows(customers):
      choice = Choice('upgrade', upgrade.station, 1, upgrade, price)
      if upgrade.kind in ('profit', 'faster'):
        station = self.stations.get(upgrade.station)
        if station is None or station.profit is None:
          continue
        yield choice, station.profit * (
          upgrade.multiplier - 1 if upgrade.kind == 'profit'
          else FASTER_GAIN)
      else:
        yield choice, None

  def _rows(self, customers):
    """(Upgrade, price) of the rows not bought yet (customer rows only
    when customers)."""
    for upgrade in self.upgrades or ():
      if upgrade.kind != 'customer' or customers:
        yield upgrade, upgrade_price(upgrade)


def upgrade_price(upgrade):
  return PRICES[UPGRADES.index(upgrade)]


def _log(value, base):
  return math.log(value) / math.log(base)

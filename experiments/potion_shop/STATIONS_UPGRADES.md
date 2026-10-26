# Potion Shop: stations, upgrades, strategy (2026-10-26 night)

## Stations (where to tap them)

Positions at the reference 1220x2712 (`coords/reference.py`,
`potion_shop_<name>_station`, the station's upgrade arrow), on the view
the map is aligned to by landmarks (`actions/potion_shop_map.py`:
`show_shop()`, `show_cellar()`, `current_view()`). A popup opens by a
tap at the station (`open_station()`), a level is bought by a tap on
its button (`buy_levels()`; one tap = one level).

| # | Station | Name in code | View | Point (ref) |
|---|---------|--------------|------|-------------|
| 1 | Bat Wing Extract | bat | shop | (72, 757) |
| 2 | Dragon Scale Dust | dragon | shop | (1070, 1142) |
| 3 | Unicorn Horn Shavings | unicorn | shop | (72, 1334) |
| 4 | Djinn's Breath | djinn | shop | (1070, 1334) |
| 5 | Mermaid Tears | mermaid | shop | (627, 1718) |
| 6 | Beetle Juice | beetle | shop | (959, 2122) |
| 7 | Purified Water | water | cellar | (183, 1040) |
| 8 | Spider Silk | spider | cellar | (848, 852) |
| 9 | Mystic Mushrooms | mushrooms | cellar | (1071, 1236) |
| 10 | Frog Screams | frog | cellar | (738, 1716) |

Popups partly covered on the LG: Bat's profit (chest "1603" left;
only its price is read), Spider's level (under the top bar), sometimes
Mushrooms / Dragon (chests at the right edge).

## Levels (measured on the LG, all stations)

- One level: profit x1.08, price of the next level x1.12.
- A star every 100 levels from 300 (purple 300-700, red 800, 900;
  MAX = 1000) doubles the profit (Beetle 794 -> 802: x1.08^8 x 2).
- Below 300 not measured yet (a new event: watch the popups).

## Upgrades dialog (all 131 rows)

`experiments/potion_shop/upgrades_video.tsv` (from the video of a run,
checked on the LG: same prices) = `src/auto_eatventure/potion_shop_upgrades.py`.
The dialog lists only the rows not bought yet, by price; a row is told
by the price read on its button. Every station has 8 profit rows
(x2, x3, x4, x5, x10, x25, x50, x75 = x112.5M in all; Mushrooms x100
last, Frog x175 last) and 3 "faster" rows; 11 alchemists, 8 customer
rows, Kettle 2.5M, Dig a Cellar 133aa.

Profit rows by station (price order):
- bat: x2 850B, x3 3.4aa, x4 33.1ab, x5 150ac, x10 750ad, x25 150af, x50 1ai, x75 75.1ak
- dragon: x2 680T, x3 2.72ab, x4 26.5ac, x5 120ad, x10 600ae, x25 121ag, x50 800ai, x75 60al
- unicorn: x2 544aa, x3 2.18ac, x4 21.2ad, x5 96ae, x10 480af, x25 96ah, x50 640aj, x75 48am
- djinn: x2 436ab, x3 1.75ad, x4 17ae, x5 76.8af, x10 384ag, x25 76.9ai, x50 512ak, x75 38.4an
- mermaid: x2 349ac, x3 1.4ae, x4 13.6af, x5 61.5ag, x10 308ah, x25 61.5aj, x50 410al, x75 30.8ao
- beetle: x2 279ad, x3 1.12af, x4 10.9ag, x5 49.2ah, x10 246ai, x25 49.2ak, x50 328am, x75 24.6ap
- water: x2 1.79af, x3 7.14ag, x4 69.3ah, x5 315ai, x10 1.58ak, x25 315al, x50 2.1ao, x75 158aq
- spider: x2 6.24ag, x3 25ah, x4 243ai, x5 1.11ak, x10 5.51al, x25 1.11an, x50 7.35ap, x75 551ar
- mushrooms: x2 11.5ah, x3 45.7ai, x4 444aj, x5 2.02al, x10 10.1am, x25 2.02ao, x50 13.5aq, x100 1.01at
- frog: x2 17.2ai, x3 68.5aj, x4 665ak, x5 3.02am, x10 15.1an, x25 3.02ap, x50 20.2ar, x175 1.51au

LG 2026-10-26 23:13, not bought yet (16): Frog x10 15.1an, Mushrooms
faster 20.2an, Djinn x75 38.4an, Mushrooms x25 2.02ao, Water x50 2.1ao,
Frog faster 30.3ao, Mermaid x75 30.8ao, Frog x25 3.02ap, Spider x50
7.35ap, Beetle x75 24.6ap, Mushrooms x50 13.5aq, Water x75 158aq, Frog
x50 20.2ar, Spider x75 551ar, Mushrooms x100 1.01at, Frog x175 1.51au.

## Strategy (`potion_shop_planner.py`, `StationPlan` in `potion_shop_loop.py`)

- The bot knows each station's profit, price and level (its popup, read
  once and after each purchase; between reads counted by the rules
  above) and the dialog's rows left (read once, then every 30 min).
- Income = proportional to the sum of the stations' profits. Each
  possible purchase (a level, the levels up to the next star, a row)
  gets a time: coins still missing + price x (sum of profits / profit
  gained). The shortest one is bought; while it can't be paid, the
  coins are saved for it ("saving coins for ..." in the log).
- A row of the dialog (e.g. Djinn x75) then makes that station's levels
  worth more, so they are bought next - until another purchase pays
  back sooner (the user's "after Dragon x75 upgrade the Dragon").
- Anything costing <= 0.1 % of the coins is bought at once, levels of a
  station in batches (finishes old stations to 1000: Dragon MAX 23:46).
- Alchemists, the Kettle and the cellar first; customer rows only the
  first two until brewing is done (as before).
- The other view is scrolled to only when the purchase there is clearly
  better (1.5x) or every 15 min for its crates.

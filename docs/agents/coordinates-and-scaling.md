# Coordinates and Resolution Scaling

> <- Back to [AGENTS.md](../../AGENTS.md)

## Overview

The coordinate system supports **any device resolution** from a single set of reference values calibrated at **1220x2712 pixels**. The `coords/` package (`src/auto_eatventure/coords/`; module paths below are relative to `src/auto_eatventure/`) provides resolution-independent positions.

## Module Chain

```
coords/geometry.py (Point, Region, Swipe)
    |
    v
coords/reference.py (positions at 1220x2712)
    |
    v
coords/scaled.py (ScaledCoords - scales by device ratio)
    |
    v
actions/*.py (game.coords.<name> for all interactions)
```

## How the game scales

The game scales its UI by the **screen width**, in both directions. A
phone with another aspect ratio (LG G6 2:1 vs. the reference ~2.22:1)
only has less or more room between the top bar and the bottom bar:

- the top bar and the side button columns stay at the top, below the
  status bar (its height differs between phones: Xiaomi top bar line
  at y=226, LG G6 201, OnePlus Nord 3 284)
- the bottom button bar stays at the bottom
- dialogs stay centered between the status bar and the bottom

Measured on the LG G6 (1440x2880) against the Xiaomi (1080x2400): x
and all sizes match `x * 1440 / 1220`; the top elements are 100 px
higher than that scale says, the Upgrades dialog 50 px (half), the
bottom bar matches counted from the bottom.

## coords/geometry.py

`NamedTuple`s:

- `Point(x, y)` -- a pixel on the screen (tap target)
- `Region(left, top, right, bottom)` -- a rectangle (search area; right and bottom excluded). `Region.around(point, half_width, half_height)` builds one around a point; `center`, `crop(image)`, `moved(dx, dy)`.
- `Swipe(start, end)` -- a swipe gesture between two `Point`s
- `Top(value)` / `Bottom(value)` -- anchors used only in `reference.py`: the wrapped position stays at the top / bottom of the screen
- `Center(value)` -- a y position given as a number that stays centered like a plain `Point` (the Potion Shop map's landmarks)
- `Offset(value)` -- a `Point` / `Region` relative to another position (e.g. a level label below a found icon): scaled like a size

## coords/reference.py

Pure data module. Contains:

- `REFERENCE_WIDTH = 1220`, `REFERENCE_HEIGHT = 2712` and `TOP_BAR_LINE_Y = 255` (the top bar's black line at the reference)
- All tap targets as `Point` (buttons, menus, UI elements)
- All search areas as `Region` (names ending in `_roi`)
- All swipes as `Swipe`
- Y boundaries of safe zones and tap offsets as plain numbers

### Naming Convention

Positions are lowercase names. Plain numbers end in `_x` or `_y`:

```python
settings = Top(Point(1134, 161))
settings_roi = Top(Region.around(settings.value, 30, 30))
upgrade_button = Bottom(Point(1093, 2524))
close_upgrades = Point(1035, 908)          # dialog: centered
swipe_down = Swipe(Point(646, 1889), Point(646, 1239))
station_icon_max_y = Bottom(2200)          # y position: anchored
station_tap_offset_y = 22                  # size: only scaled
side_button_zone_width_x = 180
```

**Rule**: everything is scaled by `screen_width / 1220`. A `Top`
position also moves with the status bar, a `Bottom` one is counted
from the bottom, a plain `Point` / `Region` / `Swipe` stays centered.
A plain number ending in `_x` or `_y` is a size; a y position given as
a number must be wrapped in `Top`, `Bottom` or `Center`; a `Point` /
`Region` relative to another position in `Offset`. Other values pass
through unscaled; non-pixel values (counts, ratios, thresholds) live in
the module that uses them, not here.

## coords/scaled.py

`ScaledCoords` uses Python's `__getattr__` to intercept attribute access
(`s = width / 1220`, `H` = screen height):

```python
sc = ScaledCoords(width, height)
sc.settings              # Top:    (1134 * s, 161 * s + top_offset)
sc.upgrade_button        # Bottom: (1093 * s, H - (2712 - 2524) * s)
sc.close_upgrades        # center: (1035 * s, (H + top_offset) / 2
                         #                    - (1356 - 908) * s)
sc.station_tap_offset_y  # 22 * s
sc.first_dish_candidates # tuple of scaled Points
```

`top_offset` is 0 until `align_to_top_bar(line_y)`, called at start by
`actions/null_spot.py` with the measured y of the top bar's black line
(`vision/top_bar.py`): `top_offset = line_y - 255 * s`. If the line
is not found, the positions stay as at the reference and an ERROR is
logged.

It also has `scale`, `screen_width`, `screen_height` and `top_offset`.
An unknown name raises `AttributeError` naming `coords/reference.py`.

### Resolution Detection

`Device.screen_size()` (`android/device.py`) runs `wm size` and parses output like `"Physical size: 1080x2400"`. `main.py` creates `ScaledCoords` from it; actions read it as `game.coords`.

## Adding New Coordinates

1. Add the position to `coords/reference.py`: `Point` for a tap target, `Region` for a search area, `Swipe` for a swipe, a number with `_x` / `_y` suffix for an offset or boundary. Wrap it in `Top(...)` when it belongs to the top bar or the side button columns, in `Bottom(...)` for the bottom button bar; leave dialogs and the restaurant plain (centered). Check it on a phone with another aspect ratio if you can.
2. Use it as `game.coords.<name>` in an `actions/` module, e.g. `game.device.tap(game.coords.<name>)` or `game.screen.find('<template>', game.coords.<name>_roi)`

## Key Boundaries and Thresholds

| Variable | Value | Purpose |
|----------|-------|---------|
| `station_icon_max_y` | Bottom(2200) | Icons below this are ignored (club button, red badge of the Upgrades button) |
| `station_icon_tooltip_y` | Top(1240) | Icons above this need a special tap to avoid the tooltip |
| `station_icon_min_y` | Top(1100) | Icons above this trigger a swipe up |
| `side_button_zone_width_x` | 180 | Station taps keep this far from the screen edges |

The DBSCAN pixel distance (`CLUSTER_MAX_DISTANCE = 10`, not scaled) is in `vision/matching.py`.

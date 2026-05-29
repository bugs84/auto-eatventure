# Coordinates and Resolution Scaling

> <- Back to [AGENTS.md](../../AGENTS.md)

## Overview

The coordinate system supports **any device resolution** from a single set of reference values calibrated at **1220x2712 pixels**. Three modules work together to provide resolution-independent coordinates.

## Module Chain

```
coords.py (raw values at 1220x2712)
    |
    v
scaled_coords.py (ScaledCoords proxy - scales by device ratio)
    |
    v
constants.py (Constants - bundles into {x, y} dicts)
    |
    v
adb_autoplay.py (uses self.loc.xxx for all interactions)
```

## coords.py

Pure data module at project root. Contains:

- `REFERENCE_WIDTH = 1220` and `REFERENCE_HEIGHT = 2712`
- All tap coordinates (buttons, menus, UI elements)
- All swipe start/end coordinates
- Y-boundary thresholds for safe zones
- Click offsets for fine-tuned positioning
- DBSCAN clustering parameter (`dbscan_eps = 10`)

### Naming Convention

All coordinate variables follow the pattern: `<element_name>_<x|y>`

Examples:
```python
settings_x = 1134
settings_y = 161
swipe_layout_down_start_x = 646
swipe_layout_down_start_y = 1889
```

## scaled_coords.py

`ScaledCoords` class uses Python's `__getattr__` to intercept attribute access:

- Attributes ending in `_x` -> scaled by `actual_width / REFERENCE_WIDTH`
- Attributes ending in `_y` -> scaled by `actual_height / REFERENCE_HEIGHT`
- All other attributes -> passed through unscaled (e.g., `dbscan_eps`)

```python
sc = ScaledCoords(actual_w, actual_h)
sc.settings_x    # returns round(1134 * (actual_w / 1220))
sc.settings_y    # returns round(161 * (actual_h / 2712))
sc.dbscan_eps    # returns 10 (no suffix, no scaling)
```

### Resolution Detection

`detect_resolution(device)` at `scaled_coords.py:21`:
- Calls `device.shell("wm size")`
- Parses output like `"Physical size: 1080x2400"`
- Returns `(width, height)` tuple

## constants.py

`Constants` class bundles pairs of scaled coordinates into dictionaries:

```python
self.settings_coords = {
    'x': sc.settings_x,
    'y': sc.settings_y
}

self.swipe_layout_down_coords = {
    'start': {'x': sc.swipe_layout_down_start_x, 'y': sc.swipe_layout_down_start_y},
    'end': {'x': sc.swipe_layout_down_end_x, 'y': sc.swipe_layout_down_end_y}
}
```

Used as: `self.click(self.loc.settings_coords)` or `self.swipe(**self.loc.swipe_layout_down_coords)`

## Adding New Coordinates

1. Add raw pixel values to `coords.py` with `_x` / `_y` suffix
2. If it's a tap target, add a `{x, y}` dict in `constants.py`
3. If it's a swipe, add a `{start: {x, y}, end: {x, y}}` dict in `constants.py`
4. Use via `self.loc.<name>_coords` in `adb_autoplay.py`

## Key Boundaries and Thresholds

| Variable | Value | Purpose |
|----------|-------|---------|
| `danger_max_y` | 2200 | Items below this Y excluded from food detection (club icon area) |
| `food_icon_tooltip_boundary_y` | 1240 | Food icons above this need offset click to avoid tooltip overlap |
| `food_icon_top_boundary_y` | 1100 | Icons above this trigger swipe-up to reposition layout |
| `dbscan_eps` | 10 | Max pixel distance for DBSCAN clustering (not scaled) |

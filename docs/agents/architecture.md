# Architecture

> <- Back to [AGENTS.md](../../AGENTS.md)

## Overview

The project is a **single-class monolithic Python script** that automates the Android mobile game "Eatventure" via ADB and OpenCV template matching. There are no service layers, no MVC pattern, and no external APIs beyond ADB.

## Core Architecture Diagram

```
adb_autoplay.py (AutoEatventure class)
    |
    +-- constants.py (Constants) --- coordinate dicts for click/swipe targets
    |       |
    |       +-- scaled_coords.py (ScaledCoords) --- resolution-adaptive proxy
    |               |
    |               +-- coords.py --- raw pixel values (reference: 1220x2712)
    |
    +-- matching_screenshots/ --- PNG template images for OpenCV detection
    |
    +-- ADB (adbutils) --- sends tap/swipe/text commands to device
    |
    +-- OpenCV (cv2) --- template matching, color masking, image conversion
    |
    +-- scikit-learn (DBSCAN) --- clusters duplicate match points
```

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `adb_autoplay.py` | Entry point + `AutoEatventure` class (850 lines). Screenshot capture, template matching, game loop, all interaction logic. |
| `coords.py` | All reference-resolution pixel coordinates calibrated for 1220x2712. Pure data, no logic. |
| `scaled_coords.py` | `ScaledCoords` proxy that scales `coords.py` values to actual device resolution. `_x` suffix scales horizontally, `_y` suffix scales vertically. |
| `constants.py` | `Constants` class that bundles scaled coordinates into `{x, y}` dicts for cleaner call sites. |
| `matching_screenshots/` | Pre-captured PNG images used as OpenCV templates. |

## Data Flow (One Iteration)

1. Capture screenshot from device via ADB (`screencap -p`)
2. Convert to OpenCV format (BGR, grayscale, HSV)
3. Run `cv2.matchTemplate()` against relevant templates
4. Use DBSCAN to deduplicate multiple nearby match points into centroids
5. Execute game actions (tap/swipe) via ADB shell commands
6. Repeat

## State Management

State is purely **in-memory instance variables** on `AutoEatventure`:

- `count` -- iteration counter driving periodic actions
- `nothing_to_update_count` -- consecutive frames with no food icons found
- `new_level_started` / `new_level_first_food_icon_swipe` -- post-level-transition flags
- `swipe_count` -- cycles through swipe pattern array
- `current_cv2_sc` / `_grayscale` / `_bgr2hsv` -- current frame in multiple color spaces

There is **no persistent state**, no database, no save files. The bot is purely reactive.

## Key Design Decisions

- **Flat file structure**: No `src/` directory. All core modules at project root.
- **Single class**: All bot logic in one class to keep things simple (KISS principle).
- **Resolution scaling**: One set of reference coordinates scales to any device resolution via `ScaledCoords`.
- **Template matching over OCR**: More reliable for Unity game UI where text rendering varies.
- **In-memory screenshots**: Avoids disk I/O on every iteration (except debug mode).

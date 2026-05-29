# Game Loop

> <- Back to [AGENTS.md](../../AGENTS.md)

## Overview

The main game loop lives in `AutoEatventure.start_playing_game()` at `adb_autoplay.py:684`. It runs **indefinitely**, performing actions based on what templates match in the current screenshot.

## Loop Structure

```
start_playing_game()
  |
  +-- Increment count
  +-- Check stale state (nothing_to_update_count > 50 -> restart app)
  +-- Swipe pattern (when nothing_to_update_count >= 15, every 5th frame)
  +-- Capture screenshot
  +-- [Every 5th iteration] Upgrade items (if upgrade button visible)
  +-- [Every 2nd iteration] Find and open boxes
  +-- Find food icons
  +-- If food icons found:
  |     +-- First time after level: swipe layout to reposition
  |     +-- Check for "danger" food items too close to top -> swipe up
  |     +-- Shuffle and upgrade food items (max 3 per iteration)
  +-- If no food icons:
  |     +-- Increment nothing_to_update_count
  |     +-- [Every 10th iteration] Check for next level / next city
  +-- Loop
```

## Periodic Actions by Count

| Condition | Action |
|-----------|--------|
| `count % 2 == 0` | Find and open boxes |
| `count % 5 == 0` | Open upgrade menu, click upgrade button (10x or 50x for new level) |
| `count % 10 == 0` (no food icons) | Check if next level or next city is available |

## Stale State Recovery

When `nothing_to_update_count` reaches thresholds:

- **>= 15** (every 5th after): Execute swipe pattern to reveal hidden elements
- **> 50**: Force-restart the app via `start_app()` to escape stuck state

Swipe pattern cycles through:
```python
[down, down, down, up, up, up]
```

## Level Transition Flow

`check_to_go_next_level()` at `adb_autoplay.py:558`:

### Same-city level (renovate):
1. Detect `go_next_level_icon` template
2. Click next level button
3. Click renovate button
4. Wait 10s for loading
5. Click first lemonade stand
6. Open all chests (recursive)

### New city (fly):
1. Detect `fly_next_city_icon` template
2. Click next level button
3. Click fly to next city button
4. Wait 15s for flight animation
5. Click welcome OK button
6. Click first lemonade stand
7. Open all chests (recursive)

## Food Upgrade Logic

`upgrade_food_items()` at `adb_autoplay.py:585`:

For each food icon (max 3 per iteration):
1. Click the food icon (with Y offset to hit upgrade area)
2. Click-and-hold above the icon (3000ms) to trigger "buy better food" menu
3. Click dismiss (null zone or offset position depending on Y boundary)

## Chest Opening

`open_chests()` at `adb_autoplay.py:533` is **recursive**:
1. Capture new screenshot
2. If chest icon detected:
   - Click chest icon (open it)
   - Click 3 more times (collect items)
   - Click close button
   - Call `open_chests()` again (for multiple chests)

## Disabled Features

Currently commented out in the game loop:

- **Investor redemption** (`redeem_investor()`) -- was checked every 3rd iteration
- **Ad watching for boost** (`run_full_boost_ads()`) -- was checked every 100th iteration

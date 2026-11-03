# Logging

> <- Back to [AGENTS.md](../../AGENTS.md)

## Overview

The project uses Python's built-in `logging` module configured in `src/auto_eatventure/logger.py`. All output goes through structured loggers instead of raw `print()` calls.

## Architecture

```
logger.py              # setup_logging() + key_log
  |
  +-- Console handler  # StreamHandler -> stdout (default: INFO)
  |
  +-- File handler     # _CompressingFileHandler -> logs/autoplay.log
  |                    # New file every 10 MB, old ones gzipped,
  |                    # all together at most LOG_MAX_MB
  |
  +-- Key events       # TimedRotatingFileHandler -> logs/key_events.log
                       # Key milestones only (file-only, no console)
                       # Rotates daily, keeps KEY_LOG_MAX_DAYS
```

## Configuration (via `.env`)

Read in `config.py`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `LOG_LEVEL` | `INFO` | Console output verbosity |
| `LOG_FILE_LEVEL` | `DEBUG` | File output verbosity |
| `LOG_MAX_MB` | `100` | MB that `autoplay.log` and its gzipped old files take together |
| `KEY_LOG_MAX_DAYS` | `365` | Days to keep the daily files of `key_events.log` |

## Log Levels

| Level | Usage |
|-------|-------|
| `DEBUG` | What the bot saw and did, for the analysis of a problem: every screenshot, search (template, region, score, position), reading, tap, swipe and app start, the station icons found, the window in front |
| `INFO` | All game actions: upgrading stations, opening boxes, buying upgrades, chests, level transitions, layout adjustments, stale swipes |
| `WARNING` | Recovery actions: stale state (bring game to foreground), missing config, invalid env values, an expected screen not found (Okay / Open buttons, Adventures) |
| `ERROR` | Failures: top bar not found at start (null spot fallback); a crash (uncaught exception) with its traceback |
| `CRITICAL` (shown as `FATAL`) | The game was stuck and had to be restarted (`actions/stale.py`); should not happen |

## Crashes and End of the Bot

`setup_logging()` sets `sys.excepthook`, so an uncaught exception
(e.g. an ADB command failing after the phone got disconnected) is
logged as `Bot crashed` with its traceback to `autoplay.log` (and the
console) and as one short line to `key_events.log`. Before, the
traceback went only to the console window and the logs just stopped.

The end of the bot is logged too (`Bot stopped (<reason>)` /
`STOP - Bot stopped (<reason>)`): Ctrl+C (`KeyboardInterrupt`, not a
crash), a closed console window (SIGHUP, not on Windows) and `kill`
(SIGTERM). Only `kill -9` (SIGKILL) can't be logged.

## Usage in Code

```python
import logging

log = logging.getLogger(__name__)

log.info('Chest found — opening')
log.warning('Nothing to update for %d loops — bringing game to '
            'foreground.', idle_loops)
```

## Initialization

`setup_logging(console_level, file_level, max_mb, key_log_max_days)`
must be called
once at startup, before logging. `run()` in `main.py` does it with
the levels from `config.py` (which loads `.env`):

```python
setup_logging(config.LOG_LEVEL, config.LOG_FILE_LEVEL,
              config.LOG_MAX_MB, config.KEY_LOG_MAX_DAYS)
```

Its first log line is `START - Bot started`, so every bot start is
easy to find in `autoplay.log` (the key events log gets its own
`START` entry once the game is ready, after
`start_dialogs.wait_until_ready()`).

## File Output

- Log directory: `logs/` (auto-created, gitignored)
- Active log file: `logs/autoplay.log`
- Rotation: by size, when it reaches `LOG_FILE_MB` (10 MB, ~1 day of
  DEBUG lines), it is renamed to `logs/autoplay.log.YYYY-MM-DD_HHMMSS`
  (the time of the rotation) and gzipped (~15x smaller; read with
  `zless`, `zgrep`)
- Retention: the oldest gzipped files are deleted while they and a
  full `autoplay.log` take more than `LOG_MAX_MB` (100 MB, a few weeks)
- The daily files of older versions (`autoplay.log.YYYY-MM-DD`) are
  gzipped at the start and count to the same limit
- Pillow's DEBUG lines (each PNG chunk of every screenshot) are left
  out (`PIL` logger at INFO)

### Debug lines for the analysis of a problem

The taps, swipes and app starts (`android/device.py`) and the
screenshots, searches and readings (`vision/screen.py`) are logged at
DEBUG with `stacklevel`, so the file format's module, function and
line name the bot code calling them, e.g.:

```
2026-11-03 18:02:11,532 [DEBUG] game_loop.play_once:92: Screenshot
2026-11-03 18:02:11,951 [DEBUG] boxes.open_all:17: Find all box (min 0.70): [(479, 1982)]
2026-11-03 18:02:11,952 [INFO ] boxes.open_all:20: Opening box
2026-11-03 18:02:11,953 [DEBUG] boxes.open_all:21: Tap (479, 1982)
```

## Key Events Log

A separate file recording only key milestones. Useful for tracking progress (e.g. counting cleared restaurants).

- File: `logs/key_events.log`
- Rotated daily, kept `KEY_LOG_MAX_DAYS` (365) days
- **No console output** — file only
- Format: `2024-01-15 14:23:01,234  EVENT_TYPE - description`

### Events recorded:

| Event | When | Message |
|-------|------|---------|
| `START` | Bot process begins | `START - Bot started` |
| `NEXT LEVEL` | Renovated to next level (same city) | `NEXT LEVEL - Renovated to next level` |
| `FLY` | Flying to a new city/restaurant | `FLY - Flying to next city` |
| `STALE` | Nothing to update for more than 50 loops, game brought to the foreground (not restarted; at most once per ~4 min) | `STALE - Nothing to update, bringing game to foreground` |
| `FATAL` | The game was stuck and restarted: its other window (an ad) in front after a stale recovery, or 6 stale recoveries in a row (~25 min); a screenshot is saved. Should not happen | `FATAL - GAME STUCK (<reason>), restarting the game. This should not happen, see logs/stuck_<date_time>.png and autoplay.log` |
| `POPULAR DISH` | Popular Dish selected and stopped (optional) | `POPULAR DISH - Selected first dish` |
| `RACE` | "Restaurant Race ended!" reward claimed | `RACE - Restaurant Race reward claimed` |
| `ADVENTURES` | Free Adventures rewards collected (only when something was collected) | `ADVENTURES - Collected rewards: Zeus' Feast 2x, Hangry Pirates 1x` |
| `WARNING` | First stand's "Open" button not found after renovate / fly (should not normally happen) | `WARNING - Open button not found` |
| `WARNING` | "Welcome to <city>" dialog's "Okay" button not found after fly (should not normally happen) | `WARNING - Okay button not found` |
| `ERROR` | Top bar line not found at start, the null spot stays at the fallback from `coords/reference.py`; the search must be fixed for this phone | `ERROR - Top bar not found (<reason>), null spot at fallback (x, y), popups may stay open or an ad may start; fix actions/null_spot.py` |
| `ERROR` | The bot crashed (uncaught exception, e.g. the phone got disconnected); the traceback is in `autoplay.log` | `ERROR - Bot crashed: <exception type>, see autoplay.log` |
| `STOP` | The bot was stopped: Ctrl+C, closed console window (SIGHUP) or `kill` (SIGTERM) | `STOP - Bot stopped (Ctrl+C)` |

### Usage:

```python
from auto_eatventure.logger import key_log

key_log.info('FLY - Flying to next city')
```

### Example output (`logs/key_events.log`):

```
2024-01-15 08:00:12,001  START - Bot started
2024-01-15 08:05:44,321  NEXT LEVEL - Renovated to next level
2024-01-15 08:12:01,456  NEXT LEVEL - Renovated to next level
2024-01-15 08:19:33,789  FLY - Flying to next city
2024-01-15 08:25:11,012  NEXT LEVEL - Renovated to next level
2024-01-15 09:01:55,234  STALE - Nothing to update, bringing game to foreground
```

## Console Output Format

```
<message>
```

Console format matches previous `print()` output (message only, no timestamps). This keeps the terminal clean during normal operation.

## File Output Format

```
2024-01-15 14:23:01,234 [INFO ] chests.open_all:23: Chest found — opening
```

File format includes timestamp, level, and the module, function and
line of the log call (of the bot code calling a tap or a search).

## Adding Log Statements

1. Import logging at module top: `import logging`
2. Create module logger: `log = logging.getLogger(__name__)`
3. Use appropriate level: `log.debug()`, `log.info()`, `log.warning()`, `log.error()`
4. Use `%s`-style formatting (not f-strings) in log calls for lazy evaluation:
   ```python
   log.info('Found %d matches at (%d, %d)', count, x, y)
   ```

## Rules

- Never use `print()` in the bot (`src/auto_eatventure/`, except `sandbox.py`).
- Experimental scripts and `sandbox.py` may still use `print()` for interactive CLI output.
- Default console level (`INFO`) produces the same output users saw before the migration.
- Increase to `DEBUG` only when troubleshooting specific issues.
- Key game milestones must also be logged via `key_log` (`logger.py`) for progress tracking.
- Key event messages follow the pattern: `EVENT_TYPE - description`.

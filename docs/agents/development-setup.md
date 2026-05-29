# Development Setup

> <- Back to [AGENTS.md](../../AGENTS.md)

## Prerequisites

1. **Python 3.10+** (uses `tuple[int, int]` type hints)
2. **Android Studio** with emulator (or physical Android device)
3. **ADB** installed and on system PATH
4. **Eatventure** game installed on the device/emulator

## Quick Start

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# Start emulator with Eatventure open, then:
python adb_autoplay.py
```

Or use the batch script:
```bash
start.bat
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Start emulator with Eatventure open, then:
python3 adb_autoplay.py
```

Or use the shell script:
```bash
./start.sh
```

## Environment Configuration

Copy `.env-sample` to `.env` and configure:

```bash
# Optional: target specific device (from `adb devices`)
device_serial=""

# Debug: print raw template matching values (very noisy)
DEBUG_TEMPLATE_MATCHING="0"

# Optional: override auto-computed template scale factor
TEMPLATE_SCALE_OVERRIDE=""
```

## Dependencies

From `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| `adbutils` | >= 1.2.9 | ADB device control |
| `opencv-python` | >= 4.8.0 | Template matching and image processing |
| `numpy` | >= 1.26.0 | Array operations |
| `scikit-learn` | >= 1.3.0 | DBSCAN clustering |
| `Pillow` | >= 10.0.0 | Image capture/conversion |
| `python-dotenv` | >= 0.21.1 | `.env` file loading |
| `requests` | >= 2.30.0 | HTTP requests |
| `retry` | >= 0.9.2 | Retry logic |

## Emulator Setup

Tested configuration:
- **Device**: Pixel 6 Pro API 33
- **Android**: 13.0 (Tiramisu) Google APIs x86_64
- **Game**: Eatventure v1.6.0+

## Linting

Pylint is configured via `.pylintrc`:
- 2-space indentation
- Max line length: 79 characters
- LF line endings
- Disabled: `C0330` (bad-continuation)

```bash
pylint adb_autoplay.py coords.py scaled_coords.py constants.py
```

## Project File Layout

```
adb_autoplay.py              # Main entry point (run this)
coords.py                    # Reference coordinates (1220x2712)
scaled_coords.py             # Resolution scaling proxy
constants.py                 # Coordinate dict wrapper
matching_screenshots/        # Template images for detection
captured_screenshots_on_the_fly/  # Runtime screenshots (gitignored content)
experiments/                 # Experimental scripts
.env-sample                  # Environment template
start.bat / start.sh         # Launch scripts
```

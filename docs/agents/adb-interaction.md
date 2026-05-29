# ADB Interaction

> <- Back to [AGENTS.md](../../AGENTS.md)

## Overview

All device interaction happens through **Android Debug Bridge (ADB)** via the `adbutils` Python library. The bot sends input events and captures screenshots without modifying the game.

## Device Connection

Initialization at `adb_autoplay.py:20`:

```python
serial = os.getenv("device_serial", "").strip()
if serial:
    self.device = adb.device(serial=serial)
else:
    devices = adb.device_list()
    self.device = devices[0]  # first connected device
```

- Set `device_serial` in `.env` to target a specific device/emulator
- Leave empty to auto-select the first connected device

## Input Commands

### Tap

```python
def click(self, coords):
    # Accepts dict {x, y} or list [x, y]
    self.device.shell(f"input tap {x} {y}")
```

### Long Press (Click and Hold)

```python
def click_and_hold(self, x, y, hold_duration=1000):
    # Simulates long press using a zero-distance swipe
    self.device.shell(f'input swipe {x} {y} {x} {y} {hold_duration}')
```

### Swipe

```python
def swipe(self, start, end):
    self.device.swipe(start['x'], start['y'], end['x'], end['y'])
```

### Text Input

```python
def input_text(self, text):
    escaped_text = text.replace(" ", "%s").replace("&", "\\&").replace("|", "\\|")
    self.device.shell(f"input text '{escaped_text}'")
```

## Screenshot Capture

Two methods exist:

### In-Memory (Primary) -- `capture_screenshot()` at `adb_autoplay.py:140`

```python
# Windows: shell screencap with \r\n -> \n fix
adb_command = f'adb -s {self.device.serial} shell screencap -p'
output = subprocess.check_output(adb_command.split())
output = output.replace(b'\r\n', b'\n')

# Linux/macOS: exec-out for raw binary
adb_command = f'adb -s {self.device.serial} exec-out screencap -p'
output = subprocess.check_output(adb_command.split())
```

Then converted:
1. `output` -> PIL Image (`Image.open(BytesIO(output))`)
2. PIL -> numpy array (RGB)
3. RGB -> BGR (OpenCV format)
4. BGR -> grayscale and HSV variants stored on instance

### On-Disk (Legacy/Debug) -- `capture_screenshot_on_disk()` at `adb_autoplay.py:128`

Saves to `./captured_screenshots_on_the_fly/screenshot.png` then reads back with `cv2.imread`.

## App Lifecycle

### Launch

```python
def start_app(self):
    self.device.shell(f"monkey -p {self.package_name} -c android.intent.category.LAUNCHER 1")
```

### Kill

```python
def close_app(self):
    self.device.shell(f"am force-stop {self.package_name}")
```

### Package Name

```python
self.package_name = "com.hwqgrhhjfd.idlefastfood"
```

## Platform Differences

| Platform | Screenshot Method | Notes |
|----------|-------------------|-------|
| Windows | `adb shell screencap -p` + `\r\n` -> `\n` fix | ADB corrupts binary on Windows |
| Linux/macOS | `adb exec-out screencap -p` | Raw binary output |

## Prerequisites

- ADB must be installed and on `PATH`
- Device must have USB debugging enabled
- Emulator or physical device must be connected via `adb devices`
- Game must be installed: `com.hwqgrhhjfd.idlefastfood` (Eatventure)

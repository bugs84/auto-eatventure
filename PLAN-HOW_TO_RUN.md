# How to Run auto-eatventure on Windows

## What Has Been Done

1. **Python 3.13.12** installed via `winget install Python.Python.3.13`
2. **ADB** added to user PATH (`%LOCALAPPDATA%\Android\Sdk\platform-tools`)
3. **JAVA_HOME** and **ANDROID_HOME** environment variables set permanently
4. **Python virtual environment** created at `.venv` in the project root
5. **Python dependencies** installed (`requirements.txt` updated from exact old pins to `>=` minimum versions for Python 3.13 compatibility)
6. **Android command-line tools** downloaded and installed into the SDK
7. **Pixel_6_Pro_Manual** emulator (AVD) created — resolution 1440×3120, which matches the coordinates in `constants.py`
8. **`.env` file** created from `.env-sample`

## What You Still Need to Do

### 1. Fill in your Eatventure credentials

Open `.env` in the project root and enter your account email and password:

```
notepad .env
```

```
email="your-email@example.com"
password="your-password"
```

### 2. Install the Eatventure APK on the emulator

Download the Eatventure APK (v1.6.0 recommended) from [apkpure](https://apkpure.com/eatventure/com.hwqgrhhjfd.idlefastfood) or another source, then either:

- **Drag and drop** the `.apk` file onto the emulator window, or
- Run:
  ```
  adb install path\to\eatventure.apk
  ```


### 3. Run the automation script

1. Start the emulator (if not already running):
   ```
   %LOCALAPPDATA%\Android\Sdk\emulator\emulator.exe -avd Pixel_6_Pro_Manual
   ```
2. Open the Eatventure game in the emulator and get to the playable screen.
3. Activate the virtual environment and run the script:
   ```
   cd C:\repos\auto-eatventure
   .\.venv\Scripts\activate
   python adb_autoplay.py
   ```

## Notes

- The emulator **must** be Pixel_6_Pro_Manual (1440×3120) — all tap coordinates in `constants.py` are calibrated for this resolution.
- The project was originally built for Ubuntu/Python 3.7. We updated `requirements.txt` to use `>=` minimum versions so it works with Python 3.13.
- ADB is provided by the Android SDK at `%LOCALAPPDATA%\Android\Sdk\platform-tools` and is now on your PATH.

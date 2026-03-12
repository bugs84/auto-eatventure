"""
sandbox.py - Interactive testing tool for auto-eatventure

Commands:
  sc [name]          - Take a screenshot. Optionally save as template with given name.
  save <name>        - Save the last screenshot as a new PNG template to matching_screenshots/
  crop <x> <y> <w> <h> <name>  - Crop region from last screenshot and save as template
  match <template>   - Test template matching (hsv) against last screenshot
  match_gray <template> - Test grayscale matching against last screenshot
  match_all <template>  - Find all matches of template in last screenshot
  show               - Open the last screenshot in the default viewer
  show_annot         - Show last screenshot with match annotations
  list               - List available templates
  tap <x> <y>        - Tap a coordinate on the device
  help               - Show this help
  q / quit           - Exit
"""

import os
import sys
import io
import subprocess
import numpy as np
import cv2
from PIL import Image
from adbutils import adb
from dotenv import load_dotenv
from scaled_coords import ScaledCoords, detect_resolution

load_dotenv()

DEVICE_SERIAL = os.getenv("DEVICE_SERIAL", "HIDI5LI7OFFIY5FM")
CAPTURED_PATH = "./captured_screenshots_on_the_fly/screenshot.png"
TEMPLATES_DIR = "./matching_screenshots"
ANNOTATED_PATH = "./captured_screenshots_on_the_fly/annotated_screenshot.png"


def get_device():
    device = adb.device(serial=DEVICE_SERIAL)
    print(f"Connected to device: {device.serial}")
    return device


def capture_screenshot(device) -> np.ndarray:
    """Capture screenshot from device, return as BGR numpy array."""
    adb_command = f"adb -s {device.serial} shell screencap -p"
    output = subprocess.check_output(adb_command.split())
    output = output.replace(b"\r\n", b"\n")
    pilimg = Image.open(io.BytesIO(output))
    pilimg.load()
    pilimg = pilimg.convert("RGB")
    bgr = np.array(pilimg)[:, :, ::-1].copy()
    return bgr


def save_image(bgr: np.ndarray, path: str):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    cv2.imwrite(path, bgr)
    print(f"  Saved: {path}")


def load_templates(directory: str) -> dict:
    templates = {}
    for fname in os.listdir(directory):
        if fname.lower().endswith(".png"):
            name = os.path.splitext(fname)[0]
            path = os.path.join(directory, fname)
            simple = cv2.imread(path)
            if simple is None:
                continue
            templates[name] = {
                "simple": simple,
                "grayscale": cv2.cvtColor(simple, cv2.COLOR_BGR2GRAY),
                "bgr2hsv": cv2.cvtColor(simple, cv2.COLOR_BGR2HSV),
                "path": path,
            }
    return templates


def find_template(image: np.ndarray, template: np.ndarray, threshold=0.8):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(f"  max_val={max_val:.4f}  max_loc={max_loc}  threshold={threshold}")
    if max_val >= threshold:
        return max_loc, max_val
    return None, max_val


def find_all_templates(image: np.ndarray, template: np.ndarray, threshold=0.8):
    h, w = template.shape[:2]
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    coords = [(int(x + w // 2), int(y + h // 2)) for x, y in zip(*locations[::-1])]
    return coords


def annotate_and_save(bgr: np.ndarray, point_list: list, path: str, sc: ScaledCoords, template_shape=None):
    annotated = bgr.copy()
    for x, y in point_list:
        cv2.circle(annotated, (x, y), radius=sc.annotation_radius, color=(0, 0, 255), thickness=3)
        if template_shape:
            h, w = template_shape[:2]
            cv2.rectangle(annotated, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
    save_image(annotated, path)


def open_image(path: str):
    """Open image with OS default viewer."""
    if sys.platform == "win32":
        os.startfile(os.path.abspath(path))
    else:
        subprocess.Popen(["xdg-open", path])


def print_help():
    print(__doc__)


def main():
    print("=== auto-eatventure sandbox ===")
    print("Type 'help' for available commands.\n")

    device = get_device()
    actual_w, actual_h = detect_resolution(device)
    sc = ScaledCoords(actual_w, actual_h)
    templates = load_templates(TEMPLATES_DIR)
    last_bgr: np.ndarray | None = None
    last_match_coords: list = []
    last_match_template_name: str | None = None

    while True:
        try:
            raw = input("sandbox> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()

        # ── screenshot ────────────────────────────────────────────────────────
        if cmd == "sc":
            print("  Capturing screenshot...")
            last_bgr = capture_screenshot(device)
            save_image(last_bgr, CAPTURED_PATH)
            if len(parts) >= 2:
                template_name = parts[1]
                dest = os.path.join(TEMPLATES_DIR, f"{template_name}.png")
                save_image(last_bgr, dest)
                templates = load_templates(TEMPLATES_DIR)
                print(f"  Template '{template_name}' added.")
            print(f"  Size: {last_bgr.shape[1]}x{last_bgr.shape[0]}")

        # ── save last screenshot as template ──────────────────────────────────
        elif cmd == "save":
            if len(parts) < 2:
                print("  Usage: save <name>")
            elif last_bgr is None:
                print("  No screenshot captured yet. Run 'sc' first.")
            else:
                name = parts[1]
                dest = os.path.join(TEMPLATES_DIR, f"{name}.png")
                save_image(last_bgr, dest)
                templates = load_templates(TEMPLATES_DIR)
                print(f"  Template '{name}' added.")

        # ── crop region and save as template ─────────────────────────────────
        elif cmd == "crop":
            if len(parts) < 6:
                print("  Usage: crop <x> <y> <w> <h> <name>")
            elif last_bgr is None:
                print("  No screenshot captured yet. Run 'sc' first.")
            else:
                try:
                    x, y, w, h, name = int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), parts[5]
                    region = last_bgr[y:y+h, x:x+w]
                    if region.size == 0:
                        print("  Empty region — check coordinates.")
                    else:
                        dest = os.path.join(TEMPLATES_DIR, f"{name}.png")
                        save_image(region, dest)
                        templates = load_templates(TEMPLATES_DIR)
                        print(f"  Cropped template '{name}' saved ({w}x{h} px at {x},{y}).")
                except ValueError:
                    print("  All of x, y, w, h must be integers.")

        # ── template matching (hsv) ───────────────────────────────────────────
        elif cmd == "match":
            if len(parts) < 2:
                print("  Usage: match <template_name>")
            elif last_bgr is None:
                print("  No screenshot yet. Run 'sc' first.")
            else:
                name = parts[1]
                threshold = float(parts[2]) if len(parts) >= 3 else 0.8
                if name not in templates:
                    print(f"  Template '{name}' not found. Use 'list' to see available templates.")
                else:
                    hsv_sc = cv2.cvtColor(last_bgr, cv2.COLOR_BGR2HSV)
                    hsv_tmpl = templates[name]["bgr2hsv"]
                    loc, val = find_template(hsv_sc, hsv_tmpl, threshold)
                    if loc:
                        h, w = hsv_tmpl.shape[:2]
                        cx, cy = loc[0] + w // 2, loc[1] + h // 2
                        print(f"  MATCH at top-left={loc}  center=({cx},{cy})  score={val:.4f}")
                        last_match_coords = [(cx, cy)]
                        last_match_template_name = name
                        annotate_and_save(last_bgr, last_match_coords, ANNOTATED_PATH, sc, hsv_tmpl.shape)
                    else:
                        print(f"  No match (best score={val:.4f})")

        # ── grayscale matching ────────────────────────────────────────────────
        elif cmd == "match_gray":
            if len(parts) < 2:
                print("  Usage: match_gray <template_name>")
            elif last_bgr is None:
                print("  No screenshot yet. Run 'sc' first.")
            else:
                name = parts[1]
                threshold = float(parts[2]) if len(parts) >= 3 else 0.8
                if name not in templates:
                    print(f"  Template '{name}' not found.")
                else:
                    gray_sc = cv2.cvtColor(last_bgr, cv2.COLOR_BGR2GRAY)
                    gray_tmpl = templates[name]["grayscale"]
                    loc, val = find_template(gray_sc, gray_tmpl, threshold)
                    if loc:
                        h, w = gray_tmpl.shape[:2]
                        cx, cy = loc[0] + w // 2, loc[1] + h // 2
                        print(f"  MATCH at top-left={loc}  center=({cx},{cy})  score={val:.4f}")
                        last_match_coords = [(cx, cy)]
                        last_match_template_name = name
                        annotate_and_save(last_bgr, last_match_coords, ANNOTATED_PATH, sc, gray_tmpl.shape)
                    else:
                        print(f"  No match (best score={val:.4f})")

        # ── find all matches ──────────────────────────────────────────────────
        elif cmd == "match_all":
            if len(parts) < 2:
                print("  Usage: match_all <template_name>")
            elif last_bgr is None:
                print("  No screenshot yet. Run 'sc' first.")
            else:
                name = parts[1]
                threshold = float(parts[2]) if len(parts) >= 3 else 0.8
                if name not in templates:
                    print(f"  Template '{name}' not found.")
                else:
                    hsv_sc = cv2.cvtColor(last_bgr, cv2.COLOR_BGR2HSV)
                    hsv_tmpl = templates[name]["bgr2hsv"]
                    coords = find_all_templates(hsv_sc, hsv_tmpl, threshold)
                    print(f"  Found {len(coords)} match(es): {coords}")
                    last_match_coords = coords
                    last_match_template_name = name
                    if coords:
                        annotate_and_save(last_bgr, coords, ANNOTATED_PATH, sc, hsv_tmpl.shape)

        # ── show last screenshot ──────────────────────────────────────────────
        elif cmd == "show":
            if last_bgr is None:
                print("  No screenshot yet.")
            else:
                open_image(CAPTURED_PATH)

        # ── show annotated screenshot ─────────────────────────────────────────
        elif cmd == "show_annot":
            if not os.path.exists(ANNOTATED_PATH):
                print("  No annotated screenshot yet. Run a match command first.")
            else:
                open_image(ANNOTATED_PATH)

        # ── list templates ────────────────────────────────────────────────────
        elif cmd == "list":
            if not templates:
                print("  No templates found.")
            else:
                print(f"  Templates in {TEMPLATES_DIR}/:")
                for name, data in sorted(templates.items()):
                    h, w = data["simple"].shape[:2]
                    print(f"    {name:<35} {w}x{h}px")

        # ── tap ───────────────────────────────────────────────────────────────
        elif cmd == "tap":
            if len(parts) < 3:
                print("  Usage: tap <x> <y>")
            else:
                try:
                    x, y = int(parts[1]), int(parts[2])
                    device.shell(f"input tap {x} {y}")
                    print(f"  Tapped ({x}, {y})")
                except ValueError:
                    print("  x and y must be integers.")

        # ── help / quit ───────────────────────────────────────────────────────
        elif cmd == "help":
            print_help()

        elif cmd in ("q", "quit", "exit"):
            print("Bye!")
            break

        else:
            print(f"  Unknown command '{cmd}'. Type 'help' for available commands.")


if __name__ == "__main__":
    main()

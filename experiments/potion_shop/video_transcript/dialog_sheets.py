"""Find the seconds with an open Cauldron or Upgrades dialog in the 1 fps
frames of make_sheets.sh and cut those moments at ~4 fps into contact
sheets (dialogs are open only 1-3 s, several purchases a second).

Usage (project .venv for OpenCV):
  .venv/bin/python dialog_sheets.py OUT_DIR
Writes OUT_DIR/dialogs.csv (second,kind) and OUT_DIR/dialog_sheets/*.jpg
(w<first second>_<n>.jpg, 4x2 frames = 2 s, the video time with
decimals burnt in)."""

import csv
import glob
import os
import subprocess
import sys

import cv2

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
# Frames per second of the dialog sheets
FPS = 4
# Seconds added before and after a dialog window
MARGIN_S = 1


def kind(path):
  """'cauldron', 'upgrades' or None for one frame (thresholds measured
  on the Rosix video: teal 0.42-0.85 vs 0.00-0.02; dimmed border ~75 vs
  110-176 with a white card > 0.5)."""
  image = cv2.imread(path)
  height, width = image.shape[:2]
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  low = hsv[int(height * 0.35):int(height * 0.95)]
  teal = cv2.inRange(low, (85, 80, 40), (105, 255, 110)).mean() / 255
  if teal > 0.3:
    return 'cauldron'
  value = hsv[int(height * 0.3):int(height * 0.7), :, 2]
  edge = int(width * 0.05)
  border = (value[:, :edge].mean() + value[:, -edge:].mean()) / 2
  card = hsv[int(height * 0.25):int(height * 0.75),
             int(width * 0.1):int(width * 0.9)]
  white = cv2.inRange(card, (0, 0, 225), (180, 30, 255)).mean() / 255
  if border < 95 and white > 0.5:
    return 'upgrades'
  return None


def main(out):
  """Detect the dialogs and cut the dialog sheets of OUT_DIR."""
  rows = []
  for path in sorted(glob.glob(os.path.join(out, 'frames', '*.jpg'))):
    second = int(os.path.basename(path)[:-4]) - 1
    found = kind(path)
    if found:
      rows.append((second, found))
  with open(os.path.join(out, 'dialogs.csv'), 'w', newline='',
            encoding='utf-8') as file:
    csv.writer(file).writerows([('second', 'kind')] + rows)
  windows = []
  for second, _ in rows:
    start, end = second - MARGIN_S, second + 1 + MARGIN_S
    if windows and start <= windows[-1][1]:
      windows[-1][1] = max(windows[-1][1], end)
    else:
      windows.append([max(start, 0), end])
  print(f'{len(rows)} dialog seconds, {len(windows)} windows')
  if not windows:
    return
  video = sorted(glob.glob(os.path.join(out, 'video.*')))[0]
  sheets = os.path.join(out, 'dialog_sheets')
  os.makedirs(sheets, exist_ok=True)
  for start, end in windows:
    # Named by the window's first second: w<SSSS>_<n>.jpg
    filters = (
      f'fps={FPS},scale=296:-2,drawtext=fontfile={FONT}:'
      f"text='%{{pts\\:flt\\:{start}}}':x=4:y=4:fontsize=20:"
      'fontcolor=yellow:box=1:boxcolor=black,tile=4x2')
    subprocess.run(
      ['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-t',
       str(end - start), '-i', video, '-vf', filters, '-q:v', '3',
       os.path.join(sheets, f'w{start:04d}_%d.jpg')], check=True)
  print(len(os.listdir(sheets)), 'dialog sheets')

if __name__ == '__main__':
  main(sys.argv[1])

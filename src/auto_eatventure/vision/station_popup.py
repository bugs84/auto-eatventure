"""Station popups ("Level N", the profit of an item and its time, the
price of the next level on the blue button): the numbers read by
comparing their characters with samples. "67.5ak" is read as a number
of coins (67.5e18)."""

from collections import namedtuple
import os

import cv2
import numpy as np

CHARS_DIR = os.path.join('matching_screenshots', 'station_popup_chars')
# Characters are compared at this size (width, height); one whose best
# sample differs more than MAX_DIFFERENCE (share of pixels) or whose
# width/height ratio differs more than MAX_RATIO_DIFFERENCE is unknown
CHAR_SIZE = (16, 24)
MAX_DIFFERENCE = 0.15
MAX_RATIO_DIFFERENCE = 0.25
# The button (HSV light blue, also the bottom bar's buttons: the
# popup's is below white)
BUTTON_LOW = (95, 120, 200)
BUTTON_HIGH = (110, 255, 255)
WHITE_MIN_GRAY = 225
WHITE_MAX_SATURATION = 50
MIN_WHITE_ABOVE = 0.5
# The profit and time are black, the price white; the coin icons are
# green (neither)
TEXT_MAX_GRAY = 80
# The price is in the upper part of the button (below it its shadow)
BUTTON_TEXT_SHARE = 0.75
# A dot is lower than this share of the text's height, the clock icon
# higher than CLOCK_MIN_HEIGHT of it
DOT_MAX_HEIGHT = 0.4
CLOCK_MIN_HEIGHT = 1.15
# Specks of the popup's rounded corners are not characters
MIN_CHAR_AREA = 15
# "aa" is 1e15, "ab" 1e18, ...; below it K, M, B, T
LETTER_SUFFIX_EXPONENT = 15
SUFFIXES = {'': 0, 'K': 3, 'M': 6, 'B': 9, 'T': 12}

StationPopup = namedtuple('StationPopup', 'profit seconds price')


def load_char_samples():
  """[(char, binary sample, width/height)] of the samples in CHARS_DIR
  (cut out white on black): <char>.png and more per char as
  <char>_<n>.png (the dot is told by its size)."""
  samples = []
  for name in sorted(os.listdir(CHARS_DIR)):
    if name.endswith('.png'):
      image = cv2.imread(os.path.join(CHARS_DIR, name),
                         cv2.IMREAD_GRAYSCALE)
      height, width = image.shape
      samples.append((name[0], cv2.resize(
        image, CHAR_SIZE, interpolation=cv2.INTER_AREA) > 127,
                      width / height))
  return samples


def read_popup(image, coords, samples):
  """The StationPopup open on the screenshot (BGR; its seconds None
  when unreadable), None when there is none or the profit or price
  can't be read."""
  button = _find_button(image, coords)
  if button is None:
    return None
  x, y, width, height = button
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  row = gray[max(0, y - coords.station_popup_row_above_y):
             y - coords.station_popup_row_gap_y, x:x + width]
  groups = _groups(row < TEXT_MAX_GRAY, coords)
  price_groups = _groups(_white(
    image[y:y + int(height * BUTTON_TEXT_SHARE), x:x + width]), coords)
  if not groups or not price_groups:
    return None
  profit = _coins(_text(groups[0], samples))
  price = _coins(_text(max(price_groups, key=len), samples))
  if profit is None or price is None:
    return None
  # The time is often under the event's buttons at the screen's edge
  seconds = (_seconds(_text(_after_clock(groups[1]), samples))
             if len(groups) > 1 else None)
  return StationPopup(profit, seconds, price)


def _find_button(image, coords):
  """(x, y, width, height) of the popup's blue button (the largest
  below white), None when none."""
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, BUTTON_LOW, BUTTON_HIGH)
  count, _, stats, _ = cv2.connectedComponentsWithStats(mask)
  best, best_area = None, 0
  for x, y, width, height, area in stats[1:count]:
    if (width >= coords.station_popup_button_min_x
        and coords.station_popup_button_min_y <= height
        <= coords.station_popup_button_max_y and area > best_area):
      above = image[max(0, y - coords.station_popup_row_above_y):y,
                    x:x + width]
      if above.size and _white(above).mean() >= MIN_WHITE_ABOVE:
        best, best_area = (x, y, width, height), area
  return best


def _white(image):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  return ((hsv[..., 2] >= WHITE_MIN_GRAY)
          & (hsv[..., 1] <= WHITE_MAX_SATURATION))


def _groups(mask, coords):
  """Words of the mask: lists of character boxes (x, y, w, h, image)
  left to right, split at gaps wider than station_popup_gap_x."""
  binary = mask.astype(np.uint8)
  count, _, stats, _ = cv2.connectedComponentsWithStats(binary)
  boxes = sorted(
    (x, y, w, h, binary[y:y + h, x:x + w])
    for x, y, w, h, area in stats[1:count] if area >= MIN_CHAR_AREA)
  groups = []
  for box in boxes:
    if groups and box[0] - _right(groups[-1][-1]) <= (
        coords.station_popup_gap_x):
      groups[-1].append(box)
    else:
      groups.append([box])
  return groups


def _after_clock(group):
  """The boxes right of the time's clock icon (its tallest box, a
  ring around a hand)."""
  clock = max(group, key=lambda box: box[3])
  if clock[3] < _text_height(group) * CLOCK_MIN_HEIGHT:
    return []
  return [box for box in group if box[0] >= _right(clock)]


def _right(box):
  return box[0] + box[2]


def _text_height(group):
  return sorted(box[3] for box in group)[len(group) // 2]


def _text(group, samples):
  """The characters of the group, None when one is unknown."""
  if not group:
    return None
  height = _text_height(group)
  text = ''
  for _, _, width, box_height, char in group:
    if box_height < height * DOT_MAX_HEIGHT:
      text += '.'
      continue
    known = _closest_char(char, width / box_height, samples)
    if known is None:
      return None
    text += known
  # A speck at an end (the popup's edge) is no dot
  return text.strip('.')


def _closest_char(char, ratio, samples):
  image = cv2.resize(char * 255, CHAR_SIZE,
                     interpolation=cv2.INTER_AREA) > 127
  best, best_difference = None, MAX_DIFFERENCE
  for known, sample, sample_ratio in samples:
    if abs(ratio - sample_ratio) > MAX_RATIO_DIFFERENCE:
      continue
    difference = np.count_nonzero(image != sample) / image.size
    if difference < best_difference:
      best, best_difference = known, difference
  return best


def _coins(text):
  """67.5ak -> 6.75e19; None when not a number with a known suffix."""
  if not text:
    return None
  digits = text.rstrip('abcdefghijklmnopqrstuvwxyzKMBT')
  suffix = text[len(digits):]
  try:
    number = float(digits)
  except ValueError:
    return None
  if suffix in SUFFIXES:
    return number * 10.0 ** SUFFIXES[suffix]
  if len(suffix) == 2 and suffix.islower():
    index = (ord(suffix[0]) - ord('a')) * 26 + ord(suffix[1]) - ord('a')
    return number * 10.0 ** (LETTER_SUFFIX_EXPONENT + 3 * index)
  return None


def _seconds(text):
  """18s -> 18.0; None when not seconds."""
  if not text or not text.endswith('s'):
    return None
  try:
    return float(text[:-1])
  except ValueError:
    return None

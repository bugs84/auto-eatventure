"""Numbers of the Potion Shop read by comparing their characters with
samples: station popups ("Level N", the profit of an item and its time,
the price of the next level on the blue button), the prices of the
Upgrades dialog's rows and the coin counter. "67.5ak" is read as a
number of coins (67.5e18)."""

from collections import namedtuple
import os

import cv2
import numpy as np

from auto_eatventure.coords.geometry import Point

CHARS_DIR = os.path.join('matching_screenshots', 'station_popup_chars')
# Characters are compared at this size (width, height); one whose best
# sample differs more than MAX_DIFFERENCE (share of pixels) or whose
# width/height ratio differs more than MAX_RATIO_DIFFERENCE is unknown
CHAR_SIZE = (16, 24)
MAX_DIFFERENCE = 0.15
MAX_RATIO_DIFFERENCE = 0.25
# The button (HSV light blue, also the bottom bar's buttons: the
# popup's is below white; light grey while its price is more than the
# coins, the price then red)
BUTTON_LOW = (95, 120, 200)
BUTTON_HIGH = (110, 255, 255)
GREY_BUTTON_LOW = (0, 0, 190)
GREY_BUTTON_HIGH = (180, 25, 218)
RED_PRICE_LOW = (0, 150, 150)
RED_PRICE_HIGH = (10, 255, 255)
WHITE_MIN_GRAY = 225
WHITE_MAX_SATURATION = 50
MIN_WHITE_ABOVE = 0.5
# The profit and time are black, the price white; the coin icons are
# green (neither)
TEXT_MAX_GRAY = 80
# The price is in the upper part of the button (below it its shadow);
# above it (this share of the button's height) the button is plain blue
# where not covered by an event button at the screen's edge
BUTTON_TEXT_SHARE = 0.75
BUTTON_TOP_SHARE = 0.12
# A dot is lower than this share of the text's height, the clock icon
# higher than CLOCK_MIN_HEIGHT of it
DOT_MAX_HEIGHT = 0.4
CLOCK_MIN_HEIGHT = 1.15
# Specks of the popup's rounded corners are not characters
MIN_CHAR_AREA = 15
# "aa" is 1e15, "ab" 1e18, ...; below it K, M, B, T
LETTER_SUFFIX_EXPONENT = 15
SUFFIXES = {'': 0, 'K': 3, 'M': 6, 'B': 9, 'T': 12}

# profit, seconds and level are None when unreadable (often covered by
# the event's buttons at the screen's edges or by the top bar)
StationPopup = namedtuple('StationPopup', 'profit seconds price level')
# A button of the Upgrades dialog: its center, price (None when
# unreadable) and whether it is blue (affordable; grey when not)
PriceButton = namedtuple('PriceButton', 'center price affordable')
# A button is blue when this share of it is
MIN_BLUE = 0.3


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
  """The StationPopup open on the screenshot (BGR), None when there is
  none or its price can't be read (also when partly covered)."""
  button = _find_button(image, coords)
  if button is None:
    return None
  x, y, width, _ = button
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  groups = _groups(gray[max(0, y - coords.station_popup_row_above_y):
                        y - coords.station_popup_row_gap_y, x:x + width]
                   < TEXT_MAX_GRAY, coords)
  row_covered, button_covered = _covered(image, button, coords)
  price = _popup_price(image, button, button_covered, coords, samples)
  if price is None:
    return None
  profit = (_uncovered_coins(groups[0], row_covered, samples)
            if groups else None)
  # The time is often under the event's buttons at the screen's edge
  seconds = (_seconds(_text(_after_clock(groups[1]), samples))
             if len(groups) > 1 else None)
  return StationPopup(profit, seconds, price,
                      _level(gray, button, coords, samples))


def _popup_price(image, button, covered, coords, samples):
  """The price on the popup's button, None when unreadable."""
  x, y, width, height = button
  groups = _groups(_price_text(
    image[y:y + int(height * BUTTON_TEXT_SHARE), x:x + width])
                   & ~covered, coords)
  if not groups:
    return None
  return _uncovered_coins(max(groups, key=len), covered, samples)


def popup_button(image, coords):
  """Center (Point) of the open popup's button, None when none."""
  button = _find_button(image, coords)
  if button is None:
    return None
  x, y, width, height = button
  return Point(x + width // 2, y + height // 3)


def _level(gray, button, coords, samples):
  """N of the popup's "Level N" (its digits after the l), None when
  unreadable (e.g. under the top bar)."""
  x, y, width, _ = button
  top = y - coords.station_popup_level_top_y
  if top < 0:
    return None
  groups = _groups(gray[top:y - coords.station_popup_level_bottom_y,
                        x:x + width] < TEXT_MAX_GRAY, coords)
  if not groups:
    return None
  chars = [_closest_char(box[4], box[2] / box[3], samples)
           for box in max(groups, key=len)]
  digits = ''
  while chars and chars[-1] is not None and chars[-1].isdigit():
    digits = chars.pop() + digits
  if not digits or chars[-1:] != ['l']:
    return None
  return int(digits)


def read_coins(image, region, coords, samples):
  """The coins of the counter in the region (the largest light area,
  dark digits), None when unreadable (e.g. dimmed by a dialog)."""
  part = image[max(0, region.top):region.bottom,
               max(0, region.left):region.right]
  if not part.size:
    return None
  mask = _white(part).astype(np.uint8)
  count, _, stats, _ = cv2.connectedComponentsWithStats(mask)
  if count < 2:
    return None
  x, y, width, height, _ = max(stats[1:count], key=lambda stat: stat[4])
  margin = coords.coin_counter_margin_y
  inside = part[y + margin:y + height - margin,
                x + margin:x + width - margin]
  if not inside.size:
    return None
  groups = _groups(cv2.cvtColor(inside, cv2.COLOR_BGR2GRAY)
                   < TEXT_MAX_GRAY, coords)
  if not groups:
    return None
  return parse_coins(_text(max(groups, key=len), samples))


def read_price_buttons(image, region, coords, samples):
  """The PriceButtons (blue or grey) in the region, top to bottom."""
  left, top = max(0, region.left), max(0, region.top)
  part = image[top:region.bottom, left:region.right]
  count, _, stats, _ = cv2.connectedComponentsWithStats(
    _button_color(part).astype(np.uint8))
  buttons = []
  for x, y, width, height, _ in sorted(stats[1:count],
                                       key=lambda stat: stat[1]):
    if (width >= coords.upgrade_row_button_min_x
        and coords.station_popup_button_min_y <= height
        <= coords.station_popup_button_max_y):
      button = part[y:y + int(height * BUTTON_TEXT_SHARE), x:x + width]
      buttons.append(PriceButton(
        Point(left + x + width // 2, top + y + height // 2),
        _button_price(button, coords, samples), _is_blue(button)))
  return buttons


def _is_blue(button):
  hsv = cv2.cvtColor(button, cv2.COLOR_BGR2HSV)
  return (cv2.inRange(hsv, BUTTON_LOW, BUTTON_HIGH) > 0).mean() >= MIN_BLUE


def _button_price(button, coords, samples):
  """The price on a button (cut out), None when unreadable; specks at
  its edges (the row's light background beside its rounded corners)
  are not characters."""
  width = button.shape[1]
  groups = [[box for box in group if box[0] > 0 and _right(box) < width]
            for group in _groups(_price_text(button), coords)]
  groups = [group for group in groups if group]
  if not groups:
    return None
  return parse_coins(_text(max(groups, key=len), samples))


def _covered(image, button, coords):
  """The button's columns covered by the event's buttons at the
  screen's edge: of the profit row (not white between it and the
  button) and of the button (not blue at its top)."""
  x, y, width, height = button
  gap = coords.station_popup_row_gap_y
  # (a grey button has a grey border)
  row = ~_white(image[y - 2 * gap:y - gap, x:x + width]).all(axis=0)
  top = image[y:y + int(height * BUTTON_TOP_SHARE), x:x + width]
  return row, _widened(~_button_color(top).any(axis=0), coords)


def _widened(covered, coords):
  """The covered columns and their neighbours (a white label of an
  event button reaches further than its glow over the blue)."""
  size = 2 * coords.station_popup_cover_margin_x + 1
  return cv2.dilate(covered.astype(np.uint8)[np.newaxis],
                    np.ones((1, size), np.uint8))[0] > 0


def _uncovered_coins(group, covered, samples):
  """parse_coins() of the group, None when covered left of its end (a
  leading digit may be hidden: 20.9ak read as 0.9ak)."""
  if covered[:_right(group[-1])].any():
    return None
  return parse_coins(_text(group, samples))


def _find_button(image, coords):
  """(x, y, width, height) of the popup's blue button (the largest
  below white), None when none."""
  mask = _button_color(image).astype(np.uint8)
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


def _button_color(image):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  return ((cv2.inRange(hsv, BUTTON_LOW, BUTTON_HIGH) > 0)
          | (cv2.inRange(hsv, GREY_BUTTON_LOW, GREY_BUTTON_HIGH) > 0))


def _price_text(image):
  """White or red (a grey button's) text."""
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  return _white(image) | (cv2.inRange(hsv, RED_PRICE_LOW, RED_PRICE_HIGH)
                          > 0)


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


def parse_coins(text):
  """67.5ak -> 6.75e19; None when not a number with a known suffix (a
  0 and an o look alike: an o of the number is a 0, a 0 of a two
  letter suffix an o)."""
  if not text:
    return None
  if text[-1] in SUFFIXES:
    digits, suffix = text[:-1], text[-1]
  elif len(text) > 2 and text[-2].isalpha() and text[-2] != 'o':
    digits, suffix = text[:-2], text[-2:].replace('0', 'o')
  else:
    digits, suffix = text, ''
  try:
    number = float(digits.replace('o', '0'))
  except ValueError:
    return None
  if suffix in SUFFIXES:
    return number * 10.0 ** SUFFIXES[suffix]
  if suffix.isalpha() and suffix.islower():
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

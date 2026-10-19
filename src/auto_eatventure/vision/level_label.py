"""Level labels ("Lvl 7", white on a black pill): reading the number
by comparing its digits with samples."""

import os

import cv2
import numpy as np

DIGITS_DIR = os.path.join('matching_screenshots', 'level_digits')
# The pill is black, its text white
PILL_MAX_GRAY = 60
TEXT_MIN_GRAY = 170
# Digits are compared at this size (width, height); a digit whose best
# sample differs more than MAX_DIFFERENCE (share of pixels) is unknown
# (the samples match with 0-0.01; an 8 without its sample was 0.17
# from the 6)
DIGIT_SIZE = (12, 18)
MAX_DIFFERENCE = 0.1
# "Lvl" is three letters before the number
PREFIX_CHARS = 3


def load_digit_samples():
  """{digit: binary sample} of the samples in DIGITS_DIR (<digit>.png;
  digits without a sample can't be read)."""
  samples = {}
  for digit in range(10):
    path = os.path.join(DIGITS_DIR, f'{digit}.png')
    if os.path.exists(path):
      samples[digit] = cv2.imread(path, cv2.IMREAD_GRAYSCALE) > 127
  return samples


def read_level(gray, region, samples):
  """The number of the level label in the region, None when it can't
  be read."""
  chars = characters(region.crop(gray))
  digits = chars[PREFIX_CHARS:]
  if not digits:
    return None
  number = 0
  for char in digits:
    digit = _closest_digit(char, samples)
    if digit is None:
      return None
    number = number * 10 + digit
  return number


def characters(label):
  """Binary images (DIGIT_SIZE) of the label's characters, left to
  right."""
  dark = label < PILL_MAX_GRAY
  if not dark.any():
    return []
  ys, xs = np.nonzero(dark)
  pill = label[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
  text = (pill >= TEXT_MIN_GRAY).astype(np.uint8)
  count, _, stats, _ = cv2.connectedComponentsWithStats(text)
  height = pill.shape[0]
  boxes = sorted(
    (x, y, w, h) for x, y, w, h, _ in stats[1:count]
    if h >= height * 0.35)
  return [cv2.resize(text[y:y + h, x:x + w] * 255, DIGIT_SIZE,
                     interpolation=cv2.INTER_AREA) > 127
          for x, y, w, h in boxes]


def _closest_digit(char, samples):
  best, best_difference = None, MAX_DIFFERENCE
  for digit, sample in samples.items():
    difference = np.count_nonzero(char != sample) / char.size
    if difference < best_difference:
      best, best_difference = digit, difference
  return best

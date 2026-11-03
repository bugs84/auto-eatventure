"""Screen: the last screenshot of the phone and searches on it."""

import logging

import cv2

from auto_eatventure.coords.geometry import Region
from auto_eatventure.vision import (
  colors, level_label, matching, station_popup)

log = logging.getLogger(__name__)

# A part of the screen found again after a swipe (the map's customers
# and bubbles move meanwhile)
MOVED_MIN_SCORE = 0.6


class Screen:
  """The last screenshot in the color spaces the detections need.

  Searches take the template name and an optional Region to search in
  (the whole screen by default) and return Regions in screen pixels.
  The screenshots and the results of the searches are logged (DEBUG)
  with the bot code calling them (stacklevel), to analyze what the bot
  saw.
  """

  def __init__(self, device, templates):
    """templates: {name: Template}."""
    self._device = device
    self._templates = templates
    self._digit_samples = level_label.load_digit_samples()
    self._char_samples = station_popup.load_char_samples()
    self.bgr = None
    self.gray = None
    self.hsv = None

  def capture(self):
    """Take a new screenshot of the phone."""
    log.debug('Screenshot', stacklevel=2)
    self.bgr = self._device.screenshot()
    self.gray = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2GRAY)
    self.hsv = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2HSV)

  @property
  def region(self):
    """The whole screen."""
    height, width = self.bgr.shape[:2]
    return Region(0, 0, width, height)

  def find(self, name, region=None, threshold=0.8):
    """Where the template matches (HSV) above the threshold, else
    None."""
    return self._find(name, region, threshold)

  def has(self, name, region=None, threshold=0.8):
    """Whether the template matches (HSV) above the threshold."""
    return self._find(name, region, threshold) is not None

  def _find(self, name, region, threshold):
    if region is None:
      region = self.region
    image = region.crop(self.hsv)
    template = self._templates[name].hsv
    if not _fits(template, image):
      log.debug('Find %s in %s: region smaller than the template',
                name, tuple(region), stacklevel=3)
      return None
    score, match = matching.best_match(image, template)
    found = match.moved(region.left, region.top)
    log.debug('Find %s in %s: score %.3f (min %.2f) at %s%s', name,
              tuple(region), score, threshold, tuple(found.center),
              '' if score > threshold else ' - not found', stacklevel=3)
    if score <= threshold:
      return None
    return found

  def find_exact(self, name, region=None, max_difference=0.02):
    """Where the template matches (BGR) with a difference below
    max_difference, else None.

    Brightness counts, see matching.closest_match().
    """
    if region is None:
      region = self.region
    image = region.crop(self.bgr)
    template = self._templates[name].bgr
    if not _fits(template, image):
      log.debug('Find exact %s in %s: region smaller than the template',
                name, tuple(region), stacklevel=2)
      return None
    difference, match = matching.closest_match(image, template)
    found = match.moved(region.left, region.top)
    log.debug('Find exact %s in %s: difference %.4f (max %.4f) at %s%s',
              name, tuple(region), difference, max_difference,
              tuple(found.center),
              '' if difference < max_difference else ' - not found',
              stacklevel=2)
    if difference >= max_difference:
      return None
    return found

  def find_all(self, name, threshold=0.8):
    """Centers (Points) of all matches (BGR) above the threshold."""
    points = matching.all_matches(
      self.bgr, self._templates[name].bgr, threshold)
    log.debug('Find all %s (min %.2f): %s', name, threshold,
              [tuple(point) for point in points], stacklevel=2)
    return points

  def read_station_popup(self, coords):
    """The open station popup's numbers (station_popup.StationPopup),
    None when there is none or they can't be read."""
    return _logged('Station popup', station_popup.read_popup(
      self.bgr, coords, self._char_samples))

  def station_popup_button(self, coords):
    """Center (Point) of the open station popup's button, None when
    there is none."""
    return _logged('Station popup button',
                   station_popup.popup_button(self.bgr, coords))

  def station_popup_top(self, coords):
    """Top (y) of the open station popup's level line, None when there
    is no popup."""
    return _logged('Station popup top',
                   station_popup.popup_top(self.bgr, coords))

  def moved(self, before, region):
    """How far (px, + = lower) the part of the before screenshot in the
    region is on the last one (e.g. the map after a swipe), None when
    it is not found."""
    score, found = matching.best_match(
      self.bgr[:, region.left:region.right],
      before[region.top:region.bottom, region.left:region.right])
    if score < MOVED_MIN_SCORE:
      return _logged(f'Moved {tuple(region)} (score {score:.3f})', None)
    return _logged(f'Moved {tuple(region)} (score {score:.3f})',
                   found.top - region.top)

  def read_coins(self, coords):
    """The event's coins (its counter), None when unreadable."""
    return _logged('Coins', station_popup.read_coins(
      self.bgr, coords.potion_shop_coins_roi, coords, self._char_samples))

  def read_price_buttons(self, region, coords):
    """The Upgrades dialog's buttons in the region
    (station_popup.PriceButton), top to bottom."""
    return _logged(f'Price buttons in {tuple(region)}',
                   station_popup.read_price_buttons(
                     self.bgr, region, coords, self._char_samples))

  def read_level(self, region):
    """The number of a level label ("Lvl 7") in the region, None when
    it can't be read."""
    return _logged(f'Level in {tuple(region)}', level_label.read_level(
      self.gray, region, self._digit_samples))

  def color_ratio(self, region, ranges):
    """Share (0-1) of the region's pixels in the HSV ranges, 0 when
    the region is off the screen (e.g. an ad in landscape; the bot
    crashed on its screenshot)."""
    image = region.crop(self.hsv)
    ratio = colors.color_ratio(image, ranges) if image.size else 0.0
    return _logged(f'Color ratio in {tuple(region)}', ratio)


def _logged(text, result):
  """Log the result of a reading with the bot code calling it."""
  log.debug('%s: %s', text, result, stacklevel=3)
  return result


def _fits(template, image):
  """Whether the template is not larger than the image."""
  return (template.shape[0] <= image.shape[0]
          and template.shape[1] <= image.shape[1])

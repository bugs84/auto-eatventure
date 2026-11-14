"""ScaledCoords: coords/reference.py scaled to the phone's resolution."""

from auto_eatventure.coords import reference
from auto_eatventure.coords.geometry import (
  Bottom, Center, Offset, Point, Region, Swipe, Top)


class ScaledCoords:
  """Screen positions of coords/reference.py on this phone.

    sc = ScaledCoords(1080, 2400)
    sc.upgrade_button          # Point, scaled
    sc.station_tap_offset_y    # number ending in _y, scaled

  The game scales its UI by the screen width, so all sizes and x are
  scaled by one factor (a phone with another aspect ratio only has
  more or less room vertically). Vertically, Top positions stay below
  the status bar (its height differs between phones, see
  align_to_top_bar()), Bottom positions at the bottom and the others
  (dialogs, the restaurant) in the middle of the room between them.
  """

  def __init__(self, width, height):
    self.scale = width / reference.REFERENCE_WIDTH
    self.screen_width = width
    self.screen_height = height
    # How much lower the top bar is than at the reference (a taller
    # status bar); 0 until align_to_top_bar()
    self.top_offset = 0

  def align_to_top_bar(self, line_y):
    """Move the Top positions (and the centered ones by half) to the
    measured y of the top bar's black line."""
    self.top_offset = line_y - reference.TOP_BAR_LINE_Y * self.scale

  def __getattr__(self, name):
    # Called only for names that are not set in __init__
    try:
      value = getattr(reference, name)
    except AttributeError:
      raise AttributeError(
        f'{name!r} is not defined in coords/reference.py') from None
    return self._scale(name, value)

  def _scale(self, name, value, y=None):
    """y: how a y position is scaled (Top / Bottom / Center / Offset),
    None when not wrapped in them: centered for Points, a size for
    numbers."""
    anchors = {Top: self._top_y, Bottom: self._bottom_y,
               Center: self._center_y, Offset: self._size}
    if type(value) in anchors:
      return self._scale(name, value.value, anchors[type(value)])
    if isinstance(value, Point):
      y = y or self._center_y
      return Point(self._size(value.x), y(value.y))
    if isinstance(value, Region):
      y = y or self._center_y
      return Region(self._size(value.left), y(value.top),
                    self._size(value.right), y(value.bottom))
    if isinstance(value, Swipe):
      return Swipe(self._scale(name, value.start, y),
                   self._scale(name, value.end, y))
    if isinstance(value, tuple):
      return tuple(self._scale(name, item, y) for item in value)
    return self._scale_number(name, value, y)

  def _scale_number(self, name, value, y):
    if name.endswith('_x'):
      return self._size(value)
    if name.endswith('_y'):
      return (y or self._size)(value)
    return value

  def _size(self, value):
    return round(value * self.scale)

  def _top_y(self, value):
    return round(value * self.scale + self.top_offset)

  def _center_y(self, value):
    middle = (reference.REFERENCE_HEIGHT / 2 - value) * self.scale
    return round((self.screen_height + self.top_offset) / 2 - middle)

  def _bottom_y(self, value):
    return round(self.screen_height
                 - (reference.REFERENCE_HEIGHT - value) * self.scale)

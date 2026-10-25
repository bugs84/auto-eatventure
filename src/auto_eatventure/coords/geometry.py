"""Point, Region and Swipe: the shapes screen positions are made of."""

from typing import NamedTuple


class Point(NamedTuple):
  """A pixel on the screen."""
  x: int
  y: int


class Region(NamedTuple):
  """A rectangle on the screen (right and bottom excluded)."""
  left: int
  top: int
  right: int
  bottom: int

  @classmethod
  def around(cls, center, half_width, half_height):
    """Region of the given half sizes centered on a Point."""
    return cls(center.x - half_width, center.y - half_height,
               center.x + half_width, center.y + half_height)

  @property
  def center(self):
    return Point((self.left + self.right) // 2,
                 (self.top + self.bottom) // 2)

  def crop(self, image):
    """The part of an image (numpy array) inside this region.

    A region reaching over the top or left edge (a Top position on a
    phone with a lower status bar than the reference, e.g. the LG G6)
    is cut at the edge; a negative index would count from the other
    side and the part would be empty.
    """
    return image[max(self.top, 0):self.bottom,
                 max(self.left, 0):self.right]

  def moved(self, dx, dy):
    """The same region moved by (dx, dy)."""
    return Region(self.left + dx, self.top + dy,
                  self.right + dx, self.bottom + dy)


class Swipe(NamedTuple):
  """A swipe gesture from start to end."""
  start: Point
  end: Point


class Top(NamedTuple):
  """A position in coords/reference.py that stays at the top of the
  screen, below the status bar (top bar, side button columns)."""
  value: object


class Bottom(NamedTuple):
  """A position in coords/reference.py that stays at the bottom of the
  screen (bottom button bar)."""
  value: object


class Center(NamedTuple):
  """A y position given as a number in coords/reference.py that stays
  in the middle of the screen like a plain Point (the map, dialogs)."""
  value: object


class Offset(NamedTuple):
  """A Point or Region in coords/reference.py relative to another
  position (e.g. an icon found on the screen): scaled like a size."""
  value: object

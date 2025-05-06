"""Region encapsulates a region in the image. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atanh, tanh

from PIL.ImageColor import colormap, getcolor
from PySide6.QtGui import QColor
from worktoy.text import monoSpace, stringList
from worktoy.parse import maybe
from worktoy.static import overload, THIS
from worktoy.attr import Field, AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import DispatchException, TypeException

from ..waitaminute import UnitDomainException, IntegerDomainException

from . import Pixel

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias


class Region(BaseObject):
  """Region implements a region in the image."""

  #  Public variables
  left = AttriBox[int](0)
  top = AttriBox[int](0)
  right = AttriBox[int](1)
  bottom = AttriBox[int](1)

  #  Virtual variables
  width = Field()
  height = Field()
  topLeft = Field()
  topRight = Field()
  bottomRight = Field()
  bottomLeft = Field()
  center = Field()

  #  Getters
  @width.GET
  def _getWidth(self) -> int:
    """Get the width of the region."""
    return self.right - self.left

  @height.GET
  def _getHeight(self) -> int:
    """Get the height of the region."""
    return self.bottom - self.top

  @topLeft.GET
  def _getTopLeft(self) -> Pixel:
    """Get the top left pixel of the region."""
    return Pixel(self.left, self.top)

  @topRight.GET
  def _getTopRight(self) -> Pixel:
    """Get the top right pixel of the region."""
    return Pixel(self.right, self.top)

  @bottomRight.GET
  def _getBottomRight(self) -> Pixel:
    """Get the bottom right pixel of the region."""
    return Pixel(self.right, self.bottom)

  @bottomLeft.GET
  def _getBottomLeft(self) -> Pixel:
    """Get the bottom left pixel of the region."""
    return Pixel(self.left, self.bottom)

  @center.GET
  def _getCenter(self) -> Pixel:
    """Get the center pixel of the region."""
    x = int((self.left + self.right) / 2)
    y = int((self.top + self.bottom) / 2)
    return Pixel(x, y)

  @overload(int, int, int, int)  # left, top, right, bottom
  def __init__(self, *args) -> None:
    self.left, self.top, self.right, self.bottom = args

  @overload(Pixel, Pixel)  # topLeft, bottomRight
  def __init__(self, *args) -> None:
    self.left = args[0].x
    self.top = args[0].y
    self.right = args[1].x
    self.bottom = args[1].y

  @overload(Pixel, int, int)  # topLeft, width, height
  def __init__(self, *args) -> None:
    self.left = args[0].x
    self.top = args[0].y
    self.right = args[0].x + args[1]
    self.bottom = args[0].y + args[2]

  @overload(int, int)  # width, height
  def __init__(self, *args) -> None:
    self.__init__(0, 0, *args)

  @overload()  # kwargs
  def __init__(self, **kwargs) -> None:
    leftKeys = stringList("""left, l, x0, xMin""")
    topKeys = stringList("""top, t, y0, yMin""")
    rightKeys = stringList("""right, r, x1, xMax""")
    bottomKeys = stringList("""bottom, b, y1, yMax""")
    widthKeys = stringList("""width, w""")
    heightKeys = stringList("""height, h""")
    kwargValues = dict(
        left=None, top=None, right=None, bottom=None, width=None, height=None
    )
    KEYS = [leftKeys, topKeys, rightKeys, bottomKeys, widthKeys, heightKeys]
    names = [*kwargValues.keys(), ]
    for name, keys in zip(names, KEYS):
      for key in keys:
        if key in kwargs:
          kwargValues[name] = kwargs[key]
          break
    left, top, right, bottom = None, None, None, None
    #  Horizontal limits
    if kwargValues['left'] is None:
      if kwargValues['width'] is None:
        raise ValueError("""Insufficient arguments to create a region""")
      if kwargValues['right'] is None:
        raise ValueError("""Insufficient arguments to create a region""")
      right = kwargValues['right']
      width = kwargValues['width']
      if not isinstance(width, int):
        raise TypeException('width', width, int)
      if not isinstance(right, int):
        raise TypeException('right', right, int)
      left = right - width
    elif kwargValues['right'] is None:
      if kwargValues['width'] is None:
        raise ValueError("""Insufficient arguments to create a region""")
      left = kwargValues['left']
      width = kwargValues['width']
      if not isinstance(width, int):
        raise TypeException('width', width, int)
      if not isinstance(left, int):
        raise TypeException('left', left, int)
      right = left + width
    elif kwargValues['width'] is None:
      left = kwargValues['left']
      right = kwargValues['right']
      if not isinstance(left, int):
        raise TypeException('left', left, int)
      if not isinstance(right, int):
        raise TypeException('right', right, int)
      width = right - left
    else:
      left = kwargValues['left']
      right = kwargValues['right']
      width = kwargValues['width']
      if not isinstance(left, int):
        raise TypeException('left', left, int)
      if not isinstance(right, int):
        raise TypeException('right', right, int)
      if not isinstance(width, int):
        raise TypeException('width', width, int)
      if left + width - right:
        raise ValueError("""Width and left/right are inconsistent""")
    #  Vertical limits
    if kwargValues['top'] is None:
      if kwargValues['height'] is None:
        raise ValueError("""Insufficient arguments to create a region""")
      if kwargValues['bottom'] is None:
        raise ValueError("""Insufficient arguments to create a region""")
      bottom = kwargValues['bottom']
      height = kwargValues['height']
      if not isinstance(height, int):
        raise TypeException('height', height, int)
      if not isinstance(bottom, int):
        raise TypeException('bottom', bottom, int)
      top = bottom - height
    elif kwargValues['bottom'] is None:
      if kwargValues['height'] is None:
        raise ValueError("""Insufficient arguments to create a region""")
      top = kwargValues['top']
      height = kwargValues['height']
      if not isinstance(height, int):
        raise TypeException('height', height, int)
      if not isinstance(top, int):
        raise TypeException('top', top, int)
      bottom = top + height
    elif kwargValues['height'] is None:
      top = kwargValues['top']
      bottom = kwargValues['bottom']
      if not isinstance(top, int):
        raise TypeException('top', top, int)
      if not isinstance(bottom, int):
        raise TypeException('bottom', bottom, int)
      height = bottom - top
    else:
      top = kwargValues['top']
      bottom = kwargValues['bottom']
      height = kwargValues['height']
      if not isinstance(top, int):
        raise TypeException('top', top, int)
      if not isinstance(bottom, int):
        raise TypeException('bottom', bottom, int)
      if not isinstance(height, int):
        raise TypeException('height', height, int)
      if top + height - bottom:
        raise ValueError("""Height and top/bottom are inconsistent""")
    self.__init__(left, top, right, bottom)

  @overload(Pixel)
  def __contains__(self, pixel: Pixel) -> bool:
    """Check if the pixel is in the region."""
    if self.left <= pixel.x < self.right:
      if self.top <= pixel.y < self.bottom:
        return True
    return False

  @overload(THIS)
  def __contains__(self, other: Self) -> bool:
    """Check if the region is in the region."""
    if TYPE_CHECKING:
      assert isinstance(other.topLeft, Pixel)
      assert isinstance(other.bottomRight, Pixel)
    if other.topLeft not in self:
      return False
    if other.bottomRight not in self:
      return False
    return True

  def _resolveOther(self, other: Any) -> Self:
    """Resolve the other object."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    try:
      out = cls(other)
    except (TypeError, ValueError, DispatchException):
      return NotImplemented
    else:
      return out
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        pycharmPlease = 69420
        assert isinstance(pycharmPlease, cls)
        return pycharmPlease
      else:
        pass

  def __eq__(self, other: Any) -> bool:
    """Check if the region is equal to the other region."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    if self.left != other.left:
      return False
    if self.top != other.top:
      return False
    if self.right != other.right:
      return False
    if self.bottom != other.bottom:
      return False
    return True

  def __hash__(self) -> int:
    """Hash the region."""
    return hash((self.left, self.top, self.right, self.bottom))

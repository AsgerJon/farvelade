"""Region encapsulates a part of an image"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attr import AttriBox, Field
from worktoy.ezdata import EZData
from worktoy.mcls import BaseObject
from worktoy.parse import maybe
from worktoy.static import overload, THIS
from worktoy.text import stringList, monoSpace
from worktoy.waitaminute import TypeException, VariableNotNone, \
  ReadOnlyError, ProtectedError

from moreworktoy import BadSet, BadDelete
from . import Pixel

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias, \
    Iterator, Never

  assert issubclass(Field, Pixel)


class Region(BaseObject):
  """
  Region encapsulates a part of an image.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __fallback_left__ = 0
  __fallback_top__ = 0
  __fallback_right__ = 0
  __fallback_bottom__ = 0

  #  Private variables
  __left_value__ = None
  __top_value__ = None
  __right_value__ = None
  __bottom_value__ = None

  #  Public variables
  left = Field()
  top = Field()
  right = Field()
  bottom = Field()

  #  Virtual variables
  topLeft = Field()
  topRight = Field()
  bottomRight = Field()
  bottomLeft = Field()
  width = Field()
  height = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @left.GET
  def _getLeft(self, ) -> int:
    """Get the left coordinate."""
    return maybe(self.__left_value__, self.__fallback_left__)

  @top.GET
  def _getTop(self, ) -> int:
    """Get the top coordinate."""
    return maybe(self.__top_value__, self.__fallback_top__)

  @right.GET
  def _getRight(self, ) -> int:
    """Get the right coordinate."""
    return maybe(self.__right_value__, self.__fallback_right__)

  @bottom.GET
  def _getBottom(self, ) -> int:
    """Get the bottom coordinate."""
    return maybe(self.__bottom_value__, self.__fallback_bottom__)

  @width.GET
  def _getWidth(self, ) -> int:
    """Get the width of the region."""
    return self.right - self.left

  @height.GET
  def _getHeight(self, ) -> int:
    """Get the height of the region."""
    return self.bottom - self.top

  @topLeft.GET
  def _getTopLefT(self, ) -> Pixel:
    """Get the top left pixel."""
    return Pixel(self.left, self.top)

  @topRight.GET
  def _getTopRight(self, ) -> Pixel:
    """Get the top right pixel."""
    return Pixel(self.right, self.top)

  @bottomRight.GET
  def _getBottomRight(self, ) -> Pixel:
    """Get the bottom right pixel."""
    return Pixel(self.right, self.bottom)

  @bottomLeft.GET
  def _getBottomLeft(self, ) -> Pixel:
    """Get the bottom left pixel."""
    return Pixel(self.left, self.bottom)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @left.SET
  def _setLeft(self, leftValue: int) -> None:
    """Setter-function for the left coordinate."""
    if self.__left_value__ is not None:
      raise VariableNotNone('left')
    if not isinstance(leftValue, int):
      raise TypeException('left', leftValue, int)
    if leftValue < 0:
      infoSpec = """Received negative value: '%d' for 'left' coordinate!"""
      info = monoSpace(infoSpec % leftValue)
      raise ValueError(info)
    self.__left_value__ = leftValue

  @top.SET
  def _setTop(self, topValue: int) -> None:
    """Setter-function for the top coordinate."""
    if self.__top_value__ is not None:
      raise VariableNotNone('top')
    if not isinstance(topValue, int):
      raise TypeException('top', topValue, int)
    if topValue < 0:
      infoSpec = """Received negative value: '%d' for 'top' coordinate!"""
      info = monoSpace(infoSpec % topValue)
      raise ValueError(info)
    self.__top_value__ = topValue

  @right.SET
  def _setRight(self, rightValue: int) -> None:
    """Setter-function for the right coordinate."""
    if self.__right_value__ is not None:
      raise VariableNotNone('right')
    if not isinstance(rightValue, int):
      raise TypeException('right', rightValue, int)
    if rightValue < 0:
      infoSpec = """Received negative value: '%d' for 'right' coordinate!"""
      info = monoSpace(infoSpec % rightValue)
      raise ValueError(info)
    self.__right_value__ = rightValue

  @bottom.SET
  def _setBottom(self, bottomValue: int) -> None:
    """Setter-function for the bottom coordinate."""
    if self.__bottom_value__ is not None:
      raise VariableNotNone('bottom')
    if not isinstance(bottomValue, int):
      raise TypeException('bottom', bottomValue, int)
    if bottomValue < 0:
      infoSpec = """Received negative value: '%d' for 'bottom' coordinate!"""
      info = monoSpace(infoSpec % bottomValue)
      raise ValueError(info)
    self.__bottom_value__ = bottomValue

  @topLeft.SET
  @bottomLeft.SET
  @topRight.SET
  @bottomRight.SET
  @width.SET
  @height.SET
  def _badSet(self, value: int) -> Never:
    """Bad setter function"""
    raise BadSet(self, value)

  @topLeft.DELETE
  @bottomLeft.DELETE
  @topRight.DELETE
  @bottomRight.DELETE
  @width.DELETE
  @height.DELETE
  def _badDelete(self, ) -> Never:
    """Bad deleter function"""
    raise BadDelete(self, )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PYTHON API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __setattr__(self, key: str, value: Any) -> None:
    """Set the attribute."""
    try:
      object.__setattr__(self, key, value)
    except BadSet as badSet:
      cls = type(self)
      desc = getattr(cls, key)
      try:
        oldValue = getattr(self, key)
      except Exception as exception:
        oldValue = exception
      raise ReadOnlyError(self, desc, oldValue, value)

  def __delattr__(self, key: str) -> None:
    """Delete the attribute."""
    try:
      object.__delattr__(self, key)
    except BadDelete as badDelete:
      cls = type(self)
      desc = getattr(cls, key)
      try:
        oldValue = getattr(self, key)
      except Exception as exception:
        oldValue = exception
      raise ProtectedError(self, desc, oldValue)

  @overload(Pixel)
  def __contains__(self, pixel: Pixel) -> bool:
    """Check if the pixel is in the region."""
    if self.left < pixel.x < self.right:
      if self.top < pixel.y < self.bottom:
        return True
    return False

  @overload(THIS)
  def __contains__(self, other: Self) -> bool:
    """Check if the region is in the region."""
    if TYPE_CHECKING:
      assert isinstance(other.topLeft, Pixel)
      assert isinstance(other.bottomRight, Pixel)
    if other.topLeft in self:
      if other.bottomRight in self:
        return True
    return False

  def __hash__(self, ) -> int:
    """Hash the region."""
    return hash((self.left, self.top, self.right, self.bottom))

  def __eq__(self, other: Self) -> bool:
    """Check if the region is equal to another region."""
    if TYPE_CHECKING:
      assert isinstance(other, Region)
    if self.left == other.left:
      if self.top == other.top:
        if self.right == other.right:
          if self.bottom == other.bottom:
            return True
    return False

  def __iter__(self, ) -> Iterator[int]:
    """Iterate over the region."""
    yield self.left
    yield self.top
    yield self.right
    yield self.bottom

  def __len__(self, ) -> int:
    """Return the length of the region."""
    return 4

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, int, int, int)
  def __init__(self, *args, **kwargs) -> None:
    """Create a Region with the given coordinates."""
    self.left, self.top, self.right, self.bottom = args
    if kwargs:
      self.__init__(**kwargs)

  @overload(THIS)
  def __init__(self, other: Self, **kwargs) -> None:
    """Create a Region with the given coordinates."""
    self.left = other.left
    self.top = other.top
    self.right = other.right
    self.bottom = other.bottom
    if kwargs:
      self.__init__(**kwargs)

  @overload(Pixel, Pixel)
  def __init__(self, topLeft: Pixel, bottomRight: Pixel, **kwargs) -> None:
    """Create a Region with the given coordinates."""
    self.left = topLeft.x
    self.top = topLeft.y
    self.right = bottomRight.x
    self.bottom = bottomRight.y
    if kwargs:
      self.__init__(**kwargs)

  @overload(int, int)
  def __init__(self, left: int, top: int, **kwargs) -> None:
    """Create a Region with the given coordinates."""
    self.__init__(0, 0, left, top, **kwargs)

  @overload(Pixel)
  def __init__(self, pixel: Pixel, **kwargs) -> None:
    """Create a Region with the given coordinates."""
    self.__init__(pixel.x, pixel.y, **kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    """Create a Region with the given coordinates."""
    leftKeys = stringList("""left, x0""")
    topKeys = stringList("""top, y0""")
    rightKeys = stringList("""right, x1""")
    bottomKeys = stringList("""bottom, y1""")
    KEYS = [leftKeys, topKeys, rightKeys, bottomKeys]
    TYPES = dict(left=int, top=int, right=int, bottom=int)
    VALUES = dict()
    for (keys, (name, type_)) in zip(KEYS, TYPES.items()):
      for key in keys:
        if key in kwargs:
          value = kwargs[key]
          if isinstance(value, type_):
            VALUES[name] = value
            break
          raise TypeException(key, value, type_)
    if 'left' in VALUES:
      self.left = VALUES['left']
    if 'top' in VALUES:
      self.top = VALUES['top']
    if 'right' in VALUES:
      self.right = VALUES['right']
    if 'bottom' in VALUES:
      self.bottom = VALUES['bottom']

  def asTuple(self, ) -> tuple[int, int, int, int]:
    """Return the region as a tuple."""
    return self.left, self.top, self.right, self.bottom

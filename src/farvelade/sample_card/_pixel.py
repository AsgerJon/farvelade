"""Pixel encapsulates a point in the image."""
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

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias


class Pixel(BaseObject):
  """Pixel implements a pixel in the image."""

  #  Python API
  __iter_contents__ = None

  x = AttriBox[int](0)
  y = AttriBox[int](0)

  @overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    self.x = x
    self.y = y

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.x = other.x
    self.y = other.y

  @overload()
  def __init__(self, **kwargs) -> None:
    """Initialize the pixel."""
    xKeys = stringList("""x, X, horizontal, h""")
    yKeys = stringList("""y, Y, vertical, v""")
    kwargValues = dict(x=None, y=None)
    names = [*kwargValues.keys()]
    KEYS = [xKeys, yKeys]
    for name, keys in zip(names, KEYS):
      for key in keys:
        if key in kwargs:
          kwargValues[name] = kwargs[key]
          break
      else:
        kwargValues[name] = 0  # NOQA
    x, y = kwargValues['x'], kwargValues['y']
    if not isinstance(x, int):
      raise TypeException('x', x, int)
    if not isinstance(y, int):
      raise TypeException('y', y, int)
    self.__init__(x, y)

  def __str__(self) -> str:
    """String representation"""
    infoSpec = """%s at [%d, %d]"""
    info = infoSpec % (type(self).__name__, self.x, self.y)
    return info

  def __repr__(self) -> str:
    """String representation"""
    infoSpec = """%s(%d, %d)"""
    info = infoSpec % (type(self).__name__, self.x, self.y)
    return info

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
    """Check if the pixel is equal to another pixel."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    if self.x != other.x:
      return False
    if self.y != other.y:
      return False
    return True

  def __hash__(self) -> int:
    """Hash the pixel."""
    return hash((self.x, self.y))

  def __iter__(self, ) -> Self:
    """Get the pixel."""
    self.__iter_contents__ = [self.x, self.y]
    return self

  def __next__(self) -> int:
    """Get the next pixel."""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

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


class _MetaSlice(type):
  """Allows creation of slices."""

  def __getitem__(cls, arg: Any) -> slice:
    if isinstance(arg, slice):
      return arg
    infoSpec = """Classes derived from %s supports only slices, 
    but received: '%s' of type: '%s'!"""
    clsName = type(cls).__name__
    info = infoSpec % (clsName, str(arg), type(arg).__name__)
    raise TypeError(info)


class _Slicer(metaclass=_MetaSlice):
  """Allows creation of slices."""
  pass


class Pixel(BaseObject):
  """Pixel implements a pixel in the image."""

  #  Python API
  __iter_contents__ = None

  def __iter__(self, ) -> Self:
    """Get the pixel."""
    self.__iter_contents__ = [self.x, self.y]
    return self

  def __next__(self) -> int:
    """Get the next pixel."""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __len__(self, ) -> int:
    """Get the length of the pixel."""
    return 2

  #  Public variables
  x = AttriBox[int](0)
  y = AttriBox[int](0)

  @overload(int, int)
  def __init__(self, x: int, y: int, **kwargs) -> None:
    self.x = x
    self.y = y
    if kwargs:
      self.__init__(**kwargs)

  @overload(THIS)
  def __init__(self, other: Self, **kwargs) -> None:
    self.x = other.x
    self.y = other.y
    if kwargs:
      self.__init__(**kwargs)

  @overload(complex)
  def __init__(self, other: complex, **kwargs) -> None:
    if other.real.is_integer() and other.imag.is_integer():
      self.x = int(other.real)
      self.y = int(other.imag)
    else:
      raise DispatchException
    if kwargs:
      self.__init__(**kwargs)

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
    if isinstance(other, float):
      if other.is_integer():
        return cls(int(other), int(other))
      return NotImplemented
    if isinstance(other, int):
      return cls(other, other)
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
    if isinstance(other, (int, float)):
      return False
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

  def __abs__(self) -> float:
    """The absolute value is understood as the distance to the origin."""
    return (self.x ** 2 + self.y ** 2) ** 0.5

  def __complex__(self) -> complex:
    return self.x + self.y * 1j

  def __bool__(self, ) -> bool:
    """Check if the pixel is not empty."""
    return True if self.x ** 2 + self.y ** 2 else False

  def __neg__(self, ) -> Self:
    """Negate the pixel."""
    cls = type(self)
    return cls(-self.x, -self.y)

  def __invert__(self, ) -> Self:
    cls = type(self)
    return cls(-self.y, self.x)

  def __add__(self, other: Any) -> Self:
    """Add two pixels together."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(self.x + other.x, self.y + other.y)

  def __sub__(self, other: Any) -> Self:
    return self + -other

  def __mul__(self, other: Any) -> Self:
    """
    Returns the Hadamard product
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    return cls(self.x * other.x, self.y * other.y)

  def __matmul__(self, other: Any) -> int:
    """
    Returns the dot product
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return self.x * other.x + self.y * other.y

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

  @overload(str)
  def __getitem__(self, key: str) -> int:
    """Get the pixel by key."""
    if key.lower() == 'x':
      return self.x
    if key.lower() == 'y':
      return self.y
    raise KeyError(key)

  @overload(int)
  def __getitem__(self, index: int) -> int:
    """Get the pixel by index."""
    if index < 0:
      return self.__getitem__(index + len(self))
    if index < len(self):
      return self.y if index else self.x
    raise IndexError(index)

  @overload(slice)
  def __getitem__(self, index: slice) -> list[int]:
    """Get the pixel by index."""
    if index == _Slicer[0:2]:
      return [self.x, self.y]
    if index == _Slicer[0:1]:
      return [self.x]
    if index == _Slicer[1:2]:
      return [self.y]
    if index == _Slicer[::-1]:
      return [self.y, self.x]
    if index == _Slicer[::]:
      return [self.x, self.y]
    raise IndexError(index)

  @overload(str, int)
  def __setitem__(self, key: str, value: int) -> None:
    """Set the pixel by key."""
    if key.lower() == 'x':
      self.x = value
      return
    if key.lower() == 'y':
      self.y = value
      return
    raise KeyError(key)

  @overload(int, int)
  def __setitem__(self, index: int, value: int) -> None:
    """Set the pixel by index."""
    if index < 0:
      return self.__setitem__(index + len(self), value)
    if index < len(self):
      if index == 0:
        self.x = value
      else:
        self.y = value
    raise IndexError(index)

  @overload(slice, list)
  def __setitem__(self, index: slice, value: list[int]) -> None:
    """Set the pixel by index."""
    self.__setitem__(index, tuple(value))

  @overload(slice, tuple)
  def __setitem__(self, index: slice, value: tuple[int, ...]) -> None:
    """Set the pixel by index."""
    if index == _Slicer[0:2]:
      self.x, self.y = value
      return
    if index == _Slicer[0:1]:
      self.x = value[0]
      return
    if index == _Slicer[1:2]:
      self.y = value[0]
      return
    raise IndexError(index)

"""OKLab color space."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atanh, tanh

from PIL.ImageColor import colormap, getcolor
from PySide6.QtGui import QColor
from worktoy.text import monoSpace, stringList
from worktoy.parse import maybe
from worktoy.static import overload, THIS
from worktoy.attr import Field
from worktoy.mcls import BaseObject
from worktoy.waitaminute import DispatchException

from . import RougeVertBleu
from .waitaminute import UnitDomainException, IntegerDomainException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias

  R3: TypeAlias = tuple[float, float, float]

epsilon = 1e-10


class OKLab(RougeVertBleu):
  """OKLab implements the OKLab color space."""

  #  Public variables
  L = Field()
  A = Field()
  B = Field()

  #  Helper functions
  @classmethod
  def _cubeRoot(cls, value: float) -> float:
    """Returns the cube root of the value preserving the sign."""
    if value ** 2 < epsilon:
      return 0.0
    if value < 0:
      return - cls._cubeRoot(-value)
    return value ** (1 / 3)

  def _getLab(self, ) -> R3:
    """Returns the Lab values."""
    r, g, b = self.redGamma, self.greenGamma, self.blueGamma

    L0 = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    M0 = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    S0 = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    L1 = self._cubeRoot(L0)
    M1 = self._cubeRoot(M0)
    S1 = self._cubeRoot(S0)

    #  LMS to OKLab
    L = 0.2104542553 * L1 + 0.7936177850 * M1 - 0.0040720468 * S1
    A = 1.9779984951 * L1 - 2.4285922050 * M1 + 0.4505937099 * S1
    B = 0.0259040371 * L1 + 0.7827717662 * M1 - 0.8086757660 * S1

    return L, A, B

  @classmethod
  def _getGammaRGB(cls, _L: float, _A: float, _B: float) -> R3:
    """
    Returns the RGB values from the Lab values.
    """
    L0 = (_L + 0.3963377774 * _A + 0.2158037573 * _B) ** 3
    M0 = (_L - 0.1055613458 * _A - 0.0638541728 * _B) ** 3
    S0 = (_L - 0.0894841775 * _A - 1.2914855480 * _B) ** 3

    #  OKLab to LMS
    r = (4.0767416621 * L0 - 3.3077115913 * M0 + 0.2309699292 * S0)
    g = (-1.2684380049 * L0 + 2.6097574011 * M0 - 0.3413193965 * S0)
    b = (-0.0041960863 * L0 - 0.7034186147 * M0 + 2.4092283606 * S0)

    return r, g, b

  #  Accessor methods for virtual variables
  # - Getters
  @L.GET
  def _getL(self) -> float:
    """Returns the L value."""
    return self._getLab()[0]

  @A.GET
  def _getA(self) -> float:
    """Returns the A value."""
    return self._getLab()[1]

  @B.GET
  def _getB(self) -> float:
    """Returns the B value."""
    return self._getLab()[2]

  # - Setters
  @L.SET
  def _setL(self, value: float) -> None:
    """Sets the L value."""
    r, g, b = self._getGammaRGB(value, self.A, self.B)
    self.redGamma = r
    self.greenGamma = g
    self.blueGamma = b

  @A.SET
  def _setA(self, value: float) -> None:
    """Sets the A value."""
    r, g, b = self._getGammaRGB(self.L, value, self.B)
    self.redGamma = r
    self.greenGamma = g
    self.blueGamma = b

  @B.SET
  def _setB(self, value: float) -> None:
    """Sets the B value."""
    r, g, b = self._getGammaRGB(self.L, self.A, value)
    self.redGamma = r
    self.greenGamma = g
    self.blueGamma = b

  #  Public methods
  def __add__(self, other: Any) -> Self:
    """
    Adds two OKLab colors together.
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    out = cls()
    out.L = (self.L + other.L) / 2
    out.A = self.A + other.A
    out.B = self.B + other.B
    return out

  def __neg__(self) -> Self:
    """
    Negates the color.
    """
    cls = type(self)
    out = cls()
    out.L = self.L
    out.A = -self.A
    out.B = -self.B
    return out

  def __sub__(self, other: Any) -> Self:
    """
    Subtracts two OKLab colors.
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return self + -other

  def __mul__(self, other: Any) -> Self:
    """
    Multiplies two OKLab colors.
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    rs = self.redReal + other.redReal
    r = self.redReal * other.redReal / rs
    gs = self.greenReal + other.greenReal
    g = self.greenReal * other.greenReal / gs
    bs = self.blueReal + other.blueReal
    b = self.blueReal * other.blueReal / bs
    out = cls()
    out.redReal = r
    out.greenReal = g
    out.blueReal = b
    return out

  def __invert__(self) -> Self:
    """
    Inverts the color.
    """
    cls = type(self)
    out = cls()
    r = 1 / self.redReal
    g = 1 / self.greenReal
    b = 1 / self.blueReal
    out.redReal = r
    out.greenReal = g
    out.blueReal = b
    return out

  def __truediv__(self, other: Any) -> Self:
    """
    Divides two OKLab colors.
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return self * ~other

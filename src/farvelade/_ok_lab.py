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

"""RGB represents a color in RGB space."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atanh, tanh

from worktoy.attr import Field
from worktoy.waitaminute import DispatchException

from farvelade import RougeVertBleu
from farvelade.waitaminute import UnitDomainException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any

epsilon = 1e-10


class RGB(RougeVertBleu):
  """RGB represents a color in RGB space."""

  #  Public Variables
  # - Floating point components
  redF = Field()
  greenF = Field()
  blueF = Field()
  alphaF = Field()

  # - Components mapped to real number-line
  redReal = Field()
  greenReal = Field()
  blueReal = Field()
  alphaReal = Field()

  #  Getter-methods
  # - Floating point components
  @redF.GET
  def _getRedF(self) -> float:
    """Get the red component as a float."""
    return self.red / 255.0

  @greenF.GET
  def _getGreenF(self) -> float:
    """Get the green component as a float."""
    return self.green / 255.0

  @blueF.GET
  def _getBlueF(self) -> float:
    """Get the blue component as a float."""
    return self.blue / 255.0

  @alphaF.GET
  def _getAlphaF(self) -> float:
    """Get the alpha component as a float."""
    return self.alpha / 255.0

  # - Components mapped to real number-line
  @redReal.GET
  def _getRedReal(self) -> float:
    """Get the red component as a real number."""
    return self._unitToReal(self.redF)

  @greenReal.GET
  def _getGreenReal(self) -> float:
    """Get the green component as a real number."""
    return self._unitToReal(self.greenF)

  @blueReal.GET
  def _getBlueReal(self) -> float:
    """Get the blue component as a real number."""
    return self._unitToReal(self.blueF)

  @alphaReal.GET
  def _getAlphaReal(self) -> float:
    """Get the alpha component as a real number."""
    return self._unitToReal(self.alphaF)

  #  Setter-methods
  # - Floating point components
  @redF.SET
  def _setRedF(self, value: float) -> None:
    """Set the red component from a float."""
    if value > 1.0 or value < 0.0:
      raise UnitDomainException(value)
    self.red = int(value * 255)

  @greenF.SET
  def _setGreenF(self, value: float) -> None:
    """Set the green component from a float."""
    if value > 1.0 or value < 0.0:
      raise UnitDomainException(value)
    self.green = int(value * 255)

  @blueF.SET
  def _setBlueF(self, value: float) -> None:
    """Set the blue component from a float."""
    if value > 1.0 or value < 0.0:
      raise UnitDomainException(value)
    self.blue = int(value * 255)

  @alphaF.SET
  def _setAlphaF(self, value: float) -> None:
    """Set the alpha component from a float."""
    if value > 1.0 or value < 0.0:
      raise UnitDomainException(value)
    self.alpha = int(value * 255)

  # - Components mapped to real number-line
  @redReal.SET
  def _setRedReal(self, value: float) -> None:
    """Set the red component from a real number."""
    self.redF = (tanh(value) + 1) / 2

  @greenReal.SET
  def _setGreenReal(self, value: float) -> None:
    """Set the green component from a real number."""
    self.greenF = (tanh(value) + 1) / 2

  @blueReal.SET
  def _setBlueReal(self, value: float) -> None:
    """Set the blue component from a real number."""
    self.blueF = (tanh(value) + 1) / 2

  @alphaReal.SET
  def _setAlphaReal(self, value: float) -> None:
    """Set the alpha component from a real number."""
    self.alphaF = (tanh(value) + 1) / 2

  #  Domain shifting
  @staticmethod
  def _unitToSigned(value: float) -> float:
    """Shifts from unit range (0-1) to signed range (-1, 1)."""
    out = value * 2 - 1
    out = min(1.0 - epsilon, out)
    out = max(-1.0 + epsilon, out)
    return out

  @staticmethod
  def _signedToUnit(value: float) -> float:
    """Shifts from signed range (-1, 1) to unit range (0-1)."""
    out = (value + 1) / 2
    out = min(1.0 - epsilon, out)
    out = max(0.0 + epsilon, out)
    return out

  @classmethod
  def _unitToReal(cls, value: float) -> float:
    """Shifts from unit range to real number line using atanh."""
    if value > 1.0 or value < 0.0:
      raise UnitDomainException(value)
    return atanh(cls._unitToSigned(value))

  @classmethod
  def _realToUnit(cls, value: float) -> float:
    """Shifts from real number line to unit range using tanh."""
    return cls._signedToUnit(tanh(value))

  def __neg__(self, ) -> Self:
    """Negate the RGB object."""
    cls = type(self)
    outR = self._realToUnit(-self._unitToReal(self.redF))
    outG = self._realToUnit(-self._unitToReal(self.greenF))
    outB = self._realToUnit(-self._unitToReal(self.blueF))
    return cls(outR, outG, outB, )

  def __add__(self, other: Any) -> Self:
    """Add two RGB objects."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    cls = type(self)
    r0 = self.redReal
    g0 = self.greenReal
    b0 = self.blueReal
    r1 = other.redReal
    g1 = other.greenReal
    b1 = other.blueReal
    r = self._realToUnit(r0 + r1)
    g = self._realToUnit(g0 + g1)
    b = self._realToUnit(b0 + b1)
    return cls(r, g, b, )

  def __sub__(self, other: Any) -> Self:
    """Subtract two RGB objects."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return self + -other

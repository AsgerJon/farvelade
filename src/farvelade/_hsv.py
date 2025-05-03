"""HSV subclasses RougeVertBleu and adds support for HSV color space."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atanh, tanh

from worktoy.text import monoSpace, stringList
from worktoy.parse import maybe
from worktoy.static import overload, THIS
from worktoy.attr import Field
from worktoy.mcls import BaseObject

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
  from typing import Any, Optional, Union, Self, Callable

epsilon = 1e-10


class HSV(RougeVertBleu):
  """HSV represents a color in HSV space."""

  #  Public Variables
  # - Floating point components
  hueF = Field()
  saturationF = Field()
  valueF = Field()
  alphaF = Field()

  # - Components mapped to real number-line
  hueReal = Field()
  saturationReal = Field()
  valueReal = Field()
  alphaReal = Field()

  # - Components in HSV space
  hue = Field()
  saturation = Field()
  value = Field()

  # Getter-methods

  # - Floating point components (primary)
  @valueF.GET
  def _getValue(self, ) -> float:
    """Get the value component."""
    return max(self.redF, self.greenF, self.blueF)

  @hueF.GET
  def _getHue(self, ) -> float:
    """Get the hue component."""
    r, g, b = self.redF, self.greenF, self.blueF
    maxC = self.valueF
    minC = min(r, g, b)
    delta = maxC - minC
    if delta < epsilon:
      return 0.0
    if maxC == r:
      hue = (g - b) / delta % 6
    elif maxC == g:
      hue = (b - r) / delta + 2
    else:
      hue = (r - g) / delta + 4
    return hue / 6

  @saturationF.GET
  def _getSaturation(self, ) -> float:
    """Get the saturation component."""
    maxC = self.valueF
    minC = min(self.redF, self.greenF, self.blueF)
    delta = maxC - minC
    if maxC < epsilon:
      return 0.0
    if delta < epsilon:
      return 0.0
    return delta / maxC

  # - Components mapped to real number-line (derived

  @hueReal.GET
  def _getHueReal(self, ) -> float:
    """Get the hue component as a real number."""
    return self._unitToReal(self.hueF)

  @saturationReal.GET
  def _getSaturationReal(self, ) -> float:
    """Get the saturation component as a real number."""
    return self._unitToReal(self.saturationF)

  @valueReal.GET
  def _getValueReal(self, ) -> float:
    """Get the value component as a real number."""
    return self._unitToReal(self.valueF)

  # - Components mapped to 8 bit integer domain [0, 255]
  @hue.GET
  def _getHueInt(self, ) -> int:
    """Get the hue component as an integer."""
    return int(round(self.hueF * 255))

  @saturation.GET
  def _getSaturationInt(self, ) -> int:
    """Get the saturation component as an integer."""
    return int(round(self.saturationF * 255))

  @value.GET
  def _getValueInt(self, ) -> int:
    """Get the value component as an integer."""
    return int(round(self.valueF * 255))

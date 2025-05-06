"""SampleCard creates simple image files for demonstrating the colors."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
from math import atanh, tanh

from PIL import Image
from PIL.ImageColor import colormap, getcolor
from PySide6.QtGui import QColor
from worktoy.text import monoSpace, stringList
from worktoy.parse import maybe
from worktoy.static import overload, THIS
from worktoy.attr import Field, AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import DispatchException, TypeException

from ..waitaminute import UnitDomainException, IntegerDomainException
from .. import OKLab
from . import Region, Pixel

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias

  R2: TypeAlias = tuple[float, float]
  PaintRegion: TypeAlias = tuple[Region, OKLab]
  PaintRegions: TypeAlias = list[PaintRegion]


class SampleCard(BaseObject):
  """SampleCard creates simple image files for demonstrating the colors."""

  #  Python API
  __iter_contents__ = None

  #  Fallback variables
  __fallback_width__ = 128
  __fallback_height__ = 128
  __fallback_color__ = lambda: OKLab(255, 255, 255)

  #  Private variables
  __image_width__ = None
  __image_height__ = None
  __base_color__ = None
  __paint_regions__ = None

  #  Public variables
  width = Field()
  height = Field()
  baseColor = Field()
  paintRegions = Field()

  #  Getters
  @width.GET
  def _getWidth(self) -> int:
    """Get the width of the image."""
    return maybe(self.__image_width__, self.__fallback_width__)

  @height.GET
  def _getHeight(self) -> int:
    """Get the height of the image."""
    return maybe(self.__image_height__, self.__fallback_height__)

  @baseColor.GET
  def _getBaseColor(self, **kwargs) -> OKLab:
    """Get the base color of the image."""
    if self.__base_color__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__base_color__ = self.__fallback_color__()
      return self._getBaseColor(_recursion=True)
    if isinstance(self.__base_color__, OKLab):
      return self.__base_color__
    raise TypeException('__base_color__', self.__base_color__, OKLab, )

  @paintRegions.GET
  def _getPaintRegions(self) -> PaintRegions:
    """Get the number of paint regions."""
    return maybe(self.__paint_regions__, [])

  @classmethod
  def _getImageDirectory(cls, ) -> str:
    """Returns the default directory for generated image files. """
    imgDir = os.environ['SAMPLE_CARD_DIR']
    here = os.path.abspath(os.path.dirname(__file__))

  @classmethod
  def _generateFilename(cls, ) -> str:
    """Generate a filename for the image."""
    here = os.path.abspath(os.path.dirname(__file__))
    n = 0
    for item in os.listdir(here):
      if item.startswith(cls.__name__):
        n += 1
    return """%s_%03d.png""" % (cls.__name__, n)

  # Iteration protocol
  def __iter__(self, ) -> Self:
    pixels = []
    for y in range(self.height):
      for x in range(self.width):
        pixels.append(Pixel(x, y))
    self.__iter_contents__ = pixels
    return self

  def __next__(self) -> Pixel:
    """Get the next pixel."""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __len__(self) -> int:
    """Get the number of pixels."""
    return 2

  #  Other functions

  @overload(OKLab, Region)
  def _addPaintRegion(self, color: OKLab, region: Region) -> None:
    """Add a paint region to the image."""
    self._addPaintRegion(region, color)

  @overload(Region, OKLab)
  def _addPaintRegion(self, region: Region, color: OKLab) -> None:
    """Add a paint region to the image."""
    existing = self._getPaintRegions()
    self.__paint_regions__ = [(region, color), *existing]

  @overload(Pixel)
  def __getitem__(self, pixel: Pixel) -> OKLab:
    """Get the color at the given coordinate."""
    for region, color in self.__paint_regions__:
      if pixel in region:
        return color
    return self.baseColor

  @overload(Region)
  def __getitem__(self, regionKey: Region) -> PaintRegions:
    """Get the color at the given coordinate."""
    for region, color in self.__paint_regions__:
      if regionKey in region:
        return color
    return self.baseColor

  def render(self, fid: str = None) -> None:
    """Create the image."""
    fid = maybe(fid, self._generateFilename())
    r = self.baseColor.redF
    g = self.baseColor.greenF
    b = self.baseColor.blueF
    image = Image.new('RGB', (self.width, self.height), (r, g, b))
    for pixel in self:
      for region, color in self.__paint_regions__:
        if not isinstance(pixel, Pixel):
          raise TypeException('pixel', pixel, Pixel)
        if not isinstance(region, Region):
          raise TypeException('region', region, Region)
        if not isinstance(color, OKLab):
          raise TypeException('color', color, OKLab)
        if pixel in region:
          image.putpixel((*pixel,), color.F)  # NOQA
          break
    image.save('sample.png')

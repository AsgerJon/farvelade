"""TestRGB tests the RGB class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import tanh, atanh
from random import shuffle
from unittest import TestCase

from PIL.ImageColor import colormap

from farvelade import RGB

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class TestRGB(TestCase):
  """TestRGB tests the RGB class."""

  @staticmethod
  def randColor() -> RGB:
    """Generate a random RGB color."""
    colorNames = [key for (key, val) in colormap.items()]
    shuffle(colorNames)
    return RGB(colorNames.pop())

  def setUp(self, ) -> None:
    """Set up the test case."""
    self.samples = [self.randColor() for _ in range(10)]

  def test_negation(self) -> None:
    """Test negation of RGB colors."""
    red = RGB('red')
    print("""red: %s""" % str(red))
    print("""-red : %s""" % str(-red))
    print("""red + -red : %s""" % str(red + -red))

  def test_addition(self, ) -> None:
    """Test addition of RGB colors."""
    red = RGB(255, 0, 0)
    green = RGB(0, 255, 0)
    blue = RGB(0, 0, 255)
    purple = red + blue
    print('red: %s' % str(red))
    print('green: %s' % str(green))
    print('blue: %s' % str(blue))
    print('purple: %s' % str(purple))
    susBlue = purple - red
    print('susBlue: %s' % str(susBlue))

"""TestRougeVertBleu tests the RougeVertBleu class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle, random, randint
from unittest import TestCase

from PIL.ImageColor import colormap

from farvelade import RougeVertBleu

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class TestRougeVertBleu(TestCase):
  """TestRougeVertBleu tests the RougeVertBleu class."""

  def assertAlmostEqual(self, a: float, b: float, *args) -> None:
    """Assert that two values are almost equal."""
    if (a - b) ** 2 > 0.05:  # two sigma
      TestCase.assertAlmostEqual(self, a, b, 7)  # Raise
    TestCase.assertAlmostEqual(self, a, b, 1)

  @staticmethod
  def randColor() -> RougeVertBleu:
    """Generate a random RougeVertBleu color."""
    colorNames = [key for (key, val) in colormap.items()]
    shuffle(colorNames)
    return RougeVertBleu(colorNames.pop())

  def setUp(self, ) -> None:
    """Set up the test case."""
    self.samples = [self.randColor() for _ in range(10)]

  def test_init(self, ) -> None:
    """Test the initialization of RougeVertBleu colors."""
    #  Init args
    threeInts = [randint(0, 255) for _ in range(3)]
    oneInt = [randint(0, 255)]
    kwargs = {
        'red'  : threeInts[0],
        'green': threeInts[1],
        'blue' : threeInts[2],
    }

    #  RougeVertBleu instances
    threeIntsRGB = RougeVertBleu(*threeInts)
    oneIntRGB = RougeVertBleu(*oneInt)
    kwargsRGB = RougeVertBleu(**kwargs)
    thisRGB = RougeVertBleu(threeIntsRGB)

    #  Three ints
    self.assertEqual(threeIntsRGB.red, threeInts[0])
    self.assertEqual(threeIntsRGB.green, threeInts[1])
    self.assertEqual(threeIntsRGB.blue, threeInts[2])

    #  One int
    self.assertEqual(oneIntRGB.red, oneInt[0])
    self.assertEqual(oneIntRGB.green, oneInt[0])
    self.assertEqual(oneIntRGB.blue, oneInt[0])

    #  kwargs
    self.assertEqual(kwargsRGB.red, kwargs['red'])
    self.assertEqual(kwargsRGB.green, kwargs['green'])
    self.assertEqual(kwargsRGB.blue, kwargs['blue'])

    #  thisRGB
    self.assertEqual(thisRGB.red, threeIntsRGB.red)
    self.assertEqual(thisRGB.green, threeIntsRGB.green)
    self.assertEqual(thisRGB.blue, threeIntsRGB.blue)

  def test_init_eq(self, ) -> None:
    """Instances that should be equal from different constructors"""

    threeInts = [176, 176, 176]
    oneInt = [176]
    kwargs = {
        'red'  : threeInts[0],
        'green': threeInts[1],
        'blue' : threeInts[2],
    }

    threeIntsRGB = RougeVertBleu(*threeInts)
    oneIntRGB = RougeVertBleu(*oneInt)
    kwargsRGB = RougeVertBleu(**kwargs)
    thisRGB = RougeVertBleu(threeIntsRGB)

    rgb = [
        threeIntsRGB,
        oneIntRGB,
        kwargsRGB,
        thisRGB
    ]

    for i in rgb:
      for j in rgb:
        if i is j:
          continue
        self.assertEqual(i, j)
        self.assertEqual(j, i)

  def test_eq(self, ) -> None:
    """Test the equality of RougeVertBleu colors."""
    for sample in self.samples:
      self.assertEqual(sample, sample)

  def test_set(self) -> None:
    """Tests that the setter functionality"""

"""TestRougeVertBleu tests the RougeVertBleu class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import tanh, atanh
from random import shuffle, random, randint
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


class TestRougeVertBleu(TestCase):
  """TestRougeVertBleu tests the RougeVertBleu class."""

  def assertAlmostEqual(self, a: float, b: float, *args) -> None:
    """Assert that two values are almost equal."""
    if (a - b) ** 2 > 0.05:  # two sigma
      TestCase.assertAlmostEqual(self, a, b, 7)  # Raise
    TestCase.assertAlmostEqual(self, a, b, 1)

  @staticmethod
  def randColor() -> RGB:
    """Generate a random RGB color."""
    colorNames = [key for (key, val) in colormap.items()]
    shuffle(colorNames)
    return RGB(colorNames.pop())

  def setUp(self, ) -> None:
    """Set up the test case."""
    self.samples = [self.randColor() for _ in range(10)]

  def test_init(self, ) -> None:
    """Test the initialization of RGB colors."""
    #  Init args
    fourFloats = [random() for _ in range(4)]
    fourInts = [randint(0, 255) for _ in range(4)]
    threeFloats = [random() for _ in range(3)]
    threeInts = [randint(0, 255) for _ in range(3)]
    twoFloats = [random() for _ in range(2)]
    twoInts = [randint(0, 255) for _ in range(2)]
    oneFloat = [random()]
    oneInt = [randint(0, 255)]
    kwargs = {
        'red'  : fourInts[0],
        'green': fourInts[1],
        'blue' : fourInts[2],
        'alpha': fourInts[3]
    }

    #  RGB instances
    fourFloatsRGB = RGB(*fourFloats)
    fourIntsRGB = RGB(*fourInts)
    threeFloatsRGB = RGB(*threeFloats)
    threeIntsRGB = RGB(*threeInts)
    twoFloatsRGB = RGB(*twoFloats)
    twoIntsRGB = RGB(*twoInts)
    oneFloatRGB = RGB(*oneFloat)
    oneIntRGB = RGB(*oneInt)
    kwargsRGB = RGB(**kwargs)
    thisRGB = RGB(fourFloatsRGB)

    #  Four floats
    self.assertAlmostEqual(fourFloatsRGB.redF, fourFloats[0])
    self.assertAlmostEqual(fourFloatsRGB.greenF, fourFloats[1])
    self.assertAlmostEqual(fourFloatsRGB.blueF, fourFloats[2])
    self.assertAlmostEqual(fourFloatsRGB.alphaF, fourFloats[3])

    #  Four ints
    self.assertEqual(fourIntsRGB.red, fourInts[0])
    self.assertEqual(fourIntsRGB.green, fourInts[1])
    self.assertEqual(fourIntsRGB.blue, fourInts[2])
    self.assertEqual(fourIntsRGB.alpha, fourInts[3])

    #  Three floats
    self.assertAlmostEqual(threeFloatsRGB.redF, threeFloats[0])
    self.assertAlmostEqual(threeFloatsRGB.greenF, threeFloats[1])
    self.assertAlmostEqual(threeFloatsRGB.blueF, threeFloats[2])
    self.assertAlmostEqual(threeFloatsRGB.alphaF, 1.0)

    #  Three ints
    self.assertEqual(threeIntsRGB.red, threeInts[0])
    self.assertEqual(threeIntsRGB.green, threeInts[1])
    self.assertEqual(threeIntsRGB.blue, threeInts[2])
    self.assertEqual(threeIntsRGB.alpha, 255)

    #  Two floats
    self.assertAlmostEqual(twoFloatsRGB.redF, twoFloats[0])
    self.assertAlmostEqual(twoFloatsRGB.greenF, twoFloats[0])
    self.assertAlmostEqual(twoFloatsRGB.blueF, twoFloats[0])
    self.assertAlmostEqual(twoFloatsRGB.alphaF, twoFloats[1])

    #  Two ints
    self.assertEqual(twoIntsRGB.red, twoInts[0])
    self.assertEqual(twoIntsRGB.green, twoInts[0])
    self.assertEqual(twoIntsRGB.blue, twoInts[0])
    self.assertEqual(twoIntsRGB.alpha, twoInts[1])

    #  One float
    self.assertAlmostEqual(oneFloatRGB.redF, oneFloat[0])
    self.assertAlmostEqual(oneFloatRGB.greenF, oneFloat[0])
    self.assertAlmostEqual(oneFloatRGB.blueF, oneFloat[0])
    self.assertAlmostEqual(oneFloatRGB.alphaF, 1.0)

    #  One int
    self.assertEqual(oneIntRGB.red, oneInt[0])
    self.assertEqual(oneIntRGB.green, oneInt[0])
    self.assertEqual(oneIntRGB.blue, oneInt[0])
    self.assertEqual(oneIntRGB.alpha, 255)

    #  kwargs
    self.assertEqual(kwargsRGB.red, kwargs['red'])
    self.assertEqual(kwargsRGB.green, kwargs['green'])
    self.assertEqual(kwargsRGB.blue, kwargs['blue'])
    self.assertEqual(kwargsRGB.alpha, kwargs['alpha'])

    #  thisRGB
    self.assertEqual(thisRGB.red, fourFloatsRGB.red)
    self.assertEqual(thisRGB.green, fourFloatsRGB.green)
    self.assertEqual(thisRGB.blue, fourFloatsRGB.blue)
    self.assertEqual(thisRGB.alpha, fourFloatsRGB.alpha)

  def test_init_eq(self, ) -> None:
    """Instances that should be equal from different constructors"""

    fourFloats = [0.69, 0.69, 0.69, 1.0]
    fourInts = [176, 176, 176, 255]
    threeFloats = [0.69, 0.69, 0.69]
    threeInts = [176, 176, 176]
    twoFloats = [0.69, 1.0]
    twoInts = [176, 255]
    oneFloat = [0.69]
    oneInt = [176]
    kwargs = {
        'red'  : fourInts[0],
        'green': fourInts[1],
        'blue' : fourInts[2],
        'alpha': fourInts[3]
    }

    #  RGB instances
    fourFloatsRGB = RGB(*fourFloats)
    fourIntsRGB = RGB(*fourInts)
    threeFloatsRGB = RGB(*threeFloats)
    threeIntsRGB = RGB(*threeInts)
    twoFloatsRGB = RGB(*twoFloats)
    twoIntsRGB = RGB(*twoInts)
    oneFloatRGB = RGB(*oneFloat)
    oneIntRGB = RGB(*oneInt)
    kwargsRGB = RGB(**kwargs)
    thisRGB = RGB(fourFloatsRGB)

    rgb = [
        fourFloatsRGB,
        fourIntsRGB,
        threeFloatsRGB,
        threeIntsRGB,
        twoFloatsRGB,
        twoIntsRGB,
        oneFloatRGB,
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
    """Test the equality of RGB colors."""
    for sample in self.samples:
      self.assertEqual(sample, sample)

"""TestRougeVertBleu tests the RougeVertBleu class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle, random, randint
from unittest import TestCase

from PIL.ImageColor import colormap
from worktoy.attr import Field
from worktoy.ezdata import EZData
from worktoy.mcls import BaseObject, AbstractMetaclass
from worktoy.parse import maybe

from farvelade import RougeVertBleu

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any, Callable, TypeAlias

epsilon: float = 1e-12


class Component(BaseObject):
  """Component represents a color component."""

  #  Fallback variables
  __fallback_ground__ = 255

  #  Private variables
  __ground_value__ = None

  #  Public variables
  value = Field()

  #  Virtual variables
  unitF = Field()
  realF = Field()

  #  Getters
  @value.GET
  def _getValue(self) -> int:
    """Get the value of the component."""
    return maybe(self.__ground_value__, self.__fallback_ground__)

  @unitF.GET
  def _getUnitF(self) -> float:
    """Get the unit value of the component."""
    return self.value / 255.0

  @realF.GET
  def _getRealF(self) -> float:
    """Get the real value of the component."""
    return RougeVertBleu._unitToReal(self.unitF)  # NOQA

  #  Constructor
  def __init__(self, value: int) -> None:
    """Initialize the component with a value."""
    self.__ground_value__ = value

  @classmethod
  def rand(cls, ) -> Self:
    """Generate a random component."""
    return cls(randint(0, 255))


class MetaSlice(AbstractMetaclass):
  """MetaSlice is a metaclass for the Slice class."""

  def __getitem__(cls, index: Any) -> Any:
    """If index is a slice, returns the slice object."""
    if isinstance(index, slice):
      return index
    return super().__getitem__(index)


class Slice(metaclass=MetaSlice):
  """Allows creation of a slice object with slice syntax. """
  pass


class TestRougeVertBleu(TestCase):
  """TestRougeVertBleu tests the RougeVertBleu class."""

  @staticmethod
  def randColor() -> RougeVertBleu:
    """Generate a random RougeVertBleu color."""
    colorNames = [key for (key, val) in colormap.items()]
    shuffle(colorNames)
    return RougeVertBleu(colorNames.pop())

  def assertAlmostEqual(self, a: float, b: float, *args) -> None:
    """Assert that two values are almost equal."""
    if (a - b) ** 2 > 0.05:  # two sigma
      TestCase.assertAlmostEqual(self, a, b, 7)  # Raise
    TestCase.assertAlmostEqual(self, a, b, 1)

  def assertEqual(self, a: Any, b: Any, *args) -> None:
    """Assert that two values are equal."""
    if isinstance(a, RougeVertBleu) and isinstance(b, RougeVertBleu):
      self.assertEqual(a.red, b.red)
      self.assertEqual(a.green, b.green)
      self.assertEqual(a.blue, b.blue)
      self.assertEqual(a.redF, b.redF)
      self.assertEqual(a.greenF, b.greenF)
      self.assertEqual(a.blueF, b.blueF)
      self.assertEqual(a.redReal, b.redReal)
      self.assertEqual(a.greenReal, b.greenReal)
      self.assertEqual(a.blueReal, b.blueReal)
      self.assertTrue(a == b)
      return TestCase.assertEqual(self, 0, 0, )
    else:
      return TestCase.assertEqual(self, a, b, *args)

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
    self.assertEqual(thisRGB, threeIntsRGB)
    # self.assertEqual(thisRGB.red, threeIntsRGB.red)
    # self.assertEqual(thisRGB.green, threeIntsRGB.green)
    # self.assertEqual(thisRGB.blue, threeIntsRGB.blue)

  def test_init_eq(self, ) -> None:
    """Instances that should be equal from different constructors"""

    c = Component.rand()

    threeInts = [c.value for _ in '123']
    oneInt = [c.value, ]
    kwargs = dict(red=c.value, green=c.value, blue=c.value)

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

  def test_set_base(self) -> None:
    """Tests the setter functionality on the base components. """
    for sample in self.samples:
      newRed = Component.rand()
      newGreen = Component.rand()
      newBlue = Component.rand()
      newRGB = RougeVertBleu(newRed.value, newGreen.value, newBlue.value)
      #  Set the base values
      sample.red = newRed.value
      sample.green = newGreen.value
      sample.blue = newBlue.value
      #  Check the equality
      self.assertEqual(sample, newRGB)

  def test_set_virtual_float(self) -> None:
    """Tests the setter functionality on the virtual components. """
    for sample in self.samples:
      newRed = Component.rand()
      newGreen = Component.rand()
      newBlue = Component.rand()
      newRGB = RougeVertBleu(newRed.value, newGreen.value, newBlue.value)
      #  Set the unitF values
      sample.redF = newRed.unitF
      sample.greenF = newGreen.unitF
      sample.blueF = newBlue.unitF
      #  Check the equality
      self.assertEqual(sample, newRGB)

  def test_set_virtual_real(self, ) -> None:
    """Tests the setter functionality of the virtual components on the
    real number-line. """
    for sample in self.samples:
      newRed = Component.rand()
      newGreen = Component.rand()
      newBlue = Component.rand()
      newRGB = RougeVertBleu(newRed.value, newGreen.value, newBlue.value)
      #  Set the realF values
      sample.redReal = newRed.realF
      sample.greenReal = newGreen.realF
      sample.blueReal = newBlue.realF
      #  Check the equality
      self.assertEqual(sample, newRGB)

  def test_get_item_index(self, ) -> None:
    """Tests that the __getitem__ function works as expected."""
    for sample in self.samples:
      for i, attr in enumerate(['red', 'green', 'blue']):
        #  sample[0] == sample.red and so forth
        self.assertEqual(sample[i], getattr(sample, attr))

  def test_get_item_key(self, ) -> None:
    """Tests that the __getitem__ function works as expected."""
    for sample in self.samples:
      for i, attr in enumerate(['red', 'green', 'blue']):
        #  sample['red'] == sample.red and so forth
        self.assertEqual(sample[attr], getattr(sample, attr))

  def test_get_item_virtual_key(self, ) -> None:
    """Tests that the __getitem__ function works as expected."""
    for sample in self.samples:
      for i, attr in enumerate(['redF', 'greenF', 'blueF']):
        #  sample['redF'] == sample.redF and so forth
        self.assertEqual(sample[attr], getattr(sample, attr))
      for i, attr in enumerate(['redReal', 'greenReal', 'blueReal']):
        #  sample['redReal'] == sample.redReal and so forth
        self.assertEqual(sample[attr], getattr(sample, attr))

  def test_get_item_slices(self, ) -> None:
    """Tests that the __getitem__ function works as expected."""
    slices = [Slice[::], Slice[::-1], Slice[:-1], Slice[1:], Slice[1:-1]]
    for sample in self.samples:
      sampleValues = [sample.red, sample.green, sample.blue]
      for slice_ in slices:
        expectedValues = sampleValues[slice_]
        actualValues = sample[slice_]
        for exp, act in zip(expectedValues, actualValues):
          self.assertEqual(exp, act)

  def test_set_item_index(self, ) -> None:
    """Tests that the __setitem__ function works as expected."""
    for sample in self.samples:
      newRed = Component.rand()
      newGreen = Component.rand()
      newBlue = Component.rand()
      newRGB = RougeVertBleu(newRed.value, newGreen.value, newBlue.value)
      sample[0] = newRed.value
      sample[1] = newGreen.value
      sample[2] = newBlue.value
      #  Check the equality
      self.assertEqual(sample, newRGB)

  def test_set_item_str(self, ) -> None:
    """Tests that the __setitem__ function works as expected."""
    for sample in self.samples:
      newRed = Component.rand()
      newGreen = Component.rand()
      newBlue = Component.rand()
      newRGB = RougeVertBleu(newRed.value, newGreen.value, newBlue.value)
      sample['red'] = newRed.value
      sample['green'] = newGreen.value
      sample['blue'] = newBlue.value
      #  Check the equality
      self.assertEqual(sample, newRGB)

  def test_set_item_unit(self, ) -> None:
    """Tests that the __setitem__ function works as expected."""
    for sample in self.samples:
      newRed = Component.rand()
      newGreen = Component.rand()
      newBlue = Component.rand()
      newRGB = RougeVertBleu(newRed.value, newGreen.value, newBlue.value)
      sample['redF'] = newRed.unitF
      sample['greenF'] = newGreen.unitF
      sample['blueF'] = newBlue.unitF
      #  Check the equality
      self.assertEqual(sample, newRGB)

  def test_set_item_real(self, ) -> None:
    """Tests that the __setitem__ function works as expected."""
    for sample in self.samples:
      newRed = Component.rand()
      newGreen = Component.rand()
      newBlue = Component.rand()
      newRGB = RougeVertBleu(newRed.value, newGreen.value, newBlue.value)
      sample['redReal'] = newRed.realF
      sample['greenReal'] = newGreen.realF
      sample['blueReal'] = newBlue.realF
      #  Check the equality
      self.assertEqual(sample, newRGB)

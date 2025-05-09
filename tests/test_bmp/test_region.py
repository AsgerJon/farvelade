"""TestRegion tests the Region class"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atan2
from unittest import TestCase

from worktoy.attr import Field
from worktoy.mcls import BaseObject
from worktoy.parse import maybe
from worktoy.static import overload, THIS, DELETED
from worktoy.text import stringList
from worktoy.waitaminute import ReadOnlyError, TypeException, ProtectedError

from moreworktoy import BadSet, BadDelete

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, Iterator


class ComplexNumber(BaseObject):
  """Complex number class."""

  #  Fallback variables
  __fallback_real__ = .0
  __fallback_imag__ = .0
  __delete_me__ = 'Have you deleted me yet?'

  #  Private variables
  __real_value__ = None
  __imag_value__ = None

  #  Public variables
  REAL = Field()
  IMAG = Field()

  #  Virtual variables
  ARG = Field()  # Argument
  ABS = Field()  # Absolute value
  DeleteMe = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @REAL.GET
  def _getReal(self, ) -> float:
    """
    Get the real part of the complex number.
    """
    return maybe(self.__real_value__, self.__fallback_real__)

  @IMAG.GET
  def _getImag(self, ) -> float:
    """
    Get the imaginary part of the complex number.
    """
    return maybe(self.__imag_value__, self.__fallback_imag__)

  @DeleteMe.GET
  def _getDeleteMe(self, ) -> str:
    """
    Have you deleted me yet?
    """
    if self.__delete_me__ is DELETED:
      try:
        return getattr(object, '__delete_me__')
      except AttributeError as attributeError:
        raise attributeError
    if isinstance(self.__delete_me__, str):
      return self.__delete_me__
    raise TypeException('__delete_me__', self.__delete_me__, str)

  @ABS.GET
  def _getAbs(self, ) -> float:
    """
    Get the absolute value of the complex number.
    """
    return (self.REAL ** 2 + self.IMAG ** 2) ** .5

  @ARG.GET
  def _getArg(self, ) -> float:
    """
    Get the argument of the complex number.
    """
    if self.ABS < 1e-12:
      raise ZeroDivisionError('Zero has no argument!')
    return atan2(self.IMAG, self.REAL)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @REAL.SET
  def _setReal(self, value: float) -> None:
    """
    Set the real part of the complex number.
    """
    self.__real_value__ = value

  @IMAG.SET
  def _setImag(self, value: float) -> None:
    """
    Set the imaginary part of the complex number.
    """
    self.__imag_value__ = value

  @ABS.SET
  @ARG.SET
  @DeleteMe.SET
  def _badSet(self, value: float) -> None:
    """
    Set the absolute value of the complex number.
    """
    raise BadSet(self, value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DELETERS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @REAL.DELETE
  @IMAG.DELETE
  @ABS.DELETE
  @ARG.DELETE
  def _badDelete(self, ) -> None:
    """
    Bad Deleter
    """
    raise BadDelete(self, )

  @DeleteMe.DELETE
  def _goodDelete(self, ) -> None:
    """
    Good Deleter
    """
    self.__delete_me__ = DELETED

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PYTHON API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[float]:
    """Iterate over the complex number."""
    yield self.REAL
    yield self.IMAG

  def __complex__(self, ) -> complex:
    """Convert the complex number to a complex type."""
    return self.REAL + self.IMAG * 1j

  def __setattr__(self, key: str, value: Any) -> None:
    """Set the attribute."""
    try:
      object.__setattr__(self, key, value)
    except BadSet as badSet:
      cls = type(self)
      desc = getattr(cls, key)
      try:
        oldValue = getattr(self, key)
      except Exception as exception:
        oldValue = exception
      raise ReadOnlyError(self, desc, oldValue, value)

  def __delattr__(self, key: str) -> None:
    """Delete the attribute."""
    try:
      object.__delattr__(self, key)
    except BadDelete as badDelete:
      cls = type(self)
      desc = getattr(cls, key)
      try:
        oldValue = getattr(self, key)
      except Exception as exception:
        oldValue = exception
      raise ProtectedError(desc, self, oldValue, )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(float, float)
  def __init__(self, realPart: float, imagPart: float, **kwargs) -> None:
    self.REAL = realPart
    self.IMAG = imagPart
    if kwargs:
      self.__init__(**kwargs)

  @overload(complex)
  def __init__(self, other: complex, **kwargs) -> None:
    self.__init__(other.real, other.imag, **kwargs)

  @overload(THIS)
  def __init__(self, other: Self, **kwargs) -> None:
    self.__init__(other.REAL, other.IMAG, **kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    realKeys = stringList("""real, realPart, a, x""")
    imagKeys = stringList("""imag, imagPart, b, y""")
    TYPES = dict(REAL=(float, int), IMAG=(float, int))
    KEYS = [realKeys, imagKeys]
    VALUES = dict()
    for keys, (name, type_) in zip(KEYS, TYPES.items()):
      for key in keys:
        if key in kwargs:
          value = kwargs[key]
          if isinstance(value, type_):
            VALUES[name] = value
            break
          raise TypeException(key, value, type_)
    for key, value in VALUES.items():
      setattr(self, key, value)


class TestRegion(TestCase):
  """Test the Region class."""

  def setUp(self) -> None:
    """Set up the test case."""
    self.z0 = ComplexNumber()  # No values, falling back to 0
    self.z1 = ComplexNumber(69, 420)
    self.z2 = ComplexNumber(1337 + 80085 * 1j)
    self.z3 = ComplexNumber(self.z1)
    self.z4 = ComplexNumber(real=1337, imag=80085)

  def test_init(self) -> None:
    """Test the constructors"""
    self.assertAlmostEqual(self.z0.REAL, 0)
    self.assertAlmostEqual(self.z0.IMAG, 0)
    self.assertAlmostEqual(self.z1.REAL, 69)
    self.assertAlmostEqual(self.z1.IMAG, 420)
    self.assertAlmostEqual(self.z2.REAL, 1337)
    self.assertAlmostEqual(self.z2.IMAG, 80085)
    self.assertAlmostEqual(self.z3.REAL, 69)
    self.assertAlmostEqual(self.z3.IMAG, 420)
    self.assertAlmostEqual(self.z4.REAL, 1337)
    self.assertAlmostEqual(self.z4.IMAG, 80085)

  def test_good_set(self, ) -> None:
    """Tests that good setters work"""
    with self.assertRaises(ZeroDivisionError):
      _ = self.z0.ARG

    self.assertAlmostEqual(self.z0.ABS, 0)
    self.assertAlmostEqual(self.z0.REAL, 0)
    self.assertAlmostEqual(self.z0.IMAG, 0)
    self.z0.REAL = 3
    self.z0.IMAG = 4
    self.assertAlmostEqual(self.z0.ABS, 5)
    self.assertAlmostEqual(self.z0.REAL, 3)
    self.assertAlmostEqual(self.z0.IMAG, 4)

  def test_bad_set(self, ) -> None:
    """Tests the bad set"""
    with self.assertRaises(ReadOnlyError) as context:
      self.z0.ABS = 69
    if TYPE_CHECKING:
      assert isinstance(context.exception, ReadOnlyError)
    self.assertEqual(context.exception.owningInstance, self.z0)
    self.assertEqual(context.exception.descriptorObject, ComplexNumber.ABS)
    self.assertAlmostEqual(context.exception.existingValue, 0)
    self.assertAlmostEqual(context.exception.newValue, 69)

  def test_good_delete(self, ) -> None:
    """Tests the good deleters"""
    self.assertAlmostEqual(self.z0.DeleteMe, 'Have you deleted me yet?')
    del self.z0.DeleteMe
    with self.assertRaises(AttributeError) as context:
      _ = self.z0.DeleteMe
    print(context.exception)

  def test_bad_delete(self, ) -> None:
    """Tests the bad deleters"""
    with self.assertRaises(ProtectedError) as context:
      del self.z0.ABS

    self.assertEqual(context.exception.instanceObject, self.z0)
    self.assertEqual(context.exception.descriptorObject, ComplexNumber.ABS)
    self.assertAlmostEqual(context.exception.valueObject, 0)

  def test_iter(self) -> None:
    """Test the iter method"""
    x, y = self.z0
    self.assertAlmostEqual(x, 0)
    self.assertAlmostEqual(y, 0)
    x, y = self.z1
    self.assertAlmostEqual(x, 69)
    self.assertAlmostEqual(y, 420)
    x, y = self.z2
    self.assertAlmostEqual(x, 1337)
    self.assertAlmostEqual(y, 80085)
    x, y = self.z3
    self.assertAlmostEqual(x, 69)
    self.assertAlmostEqual(y, 420)
    x, y = self.z4
    self.assertAlmostEqual(x, 1337)
    self.assertAlmostEqual(y, 80085)

  def test_complex(self) -> None:
    """Test the complex method"""
    self.assertAlmostEqual(complex(self.z0), 0 + 0j)
    self.assertAlmostEqual(complex(self.z1), 69 + 420j)
    self.assertAlmostEqual(complex(self.z2), 1337 + 80085j)
    self.assertAlmostEqual(complex(self.z3), 69 + 420j)
    self.assertAlmostEqual(complex(self.z4), 1337 + 80085j)

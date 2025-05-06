"""RougeVertBleu provides a baseclass for colors based on red, green and
blue color components ('rouge', 'vert' and 'bleu' in French). The class is
used as a base class for other color classes. It provides:
 - Overloaded constructors supporting many argument signatures:

 - Private variables for red, green and blue color components that should
 not be modified by subclasses.

 - __eq__, __ne__ and __hash__ methods to support equality and hashing of
    instances.
  - __repr__ and __str__ methods to support string representation of
    instances.
"""
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

  Getter: TypeAlias = Callable[[], Any]
  Setter: TypeAlias = Callable[[Any], None]
  GetMap: TypeAlias = dict[Union[str, int], Getter]
  SetMap: TypeAlias = dict[Union[str, int], Setter]

  R3: TypeAlias = tuple[float, float, float]

epsilon = 1e-10


class RougeVertBleu(BaseObject):
  """
  RougeVertBleu provides a baseclass for colors based on red, green and
  blue color components ('rouge', 'vert' and 'bleu' in French). The class is
  used as a base class for other color classes. It provides:
  - Overloaded constructors supporting many argument signatures:
  - Private variables for red, green and blue color components that should
    not be modified by subclasses.
  - __eq__, __ne__ and __hash__ methods to support equality and hashing of
      instances.
  - __repr__ and __str__ methods to support string representation of
    instances.
  """

  #  Python API variables
  __iter_contents__ = None

  #  Fallback variables for red, green and blue color components
  __red_fallback__ = 255
  __green_fallback__ = 255
  __blue_fallback__ = 255

  #  Private variables for red, green and blue color components
  __red_channel__ = None
  __green_channel__ = None
  __blue_channel__ = None

  #  Public variables for red, green and blue color components
  red = Field()
  green = Field()
  blue = Field()

  #  Virtual variables
  # - Floating point components
  redF = Field()
  greenF = Field()
  blueF = Field()
  F = Field()

  # - Components mapped to real number-line
  redReal = Field()
  greenReal = Field()
  blueReal = Field()

  # - Gamma corrected components
  redGamma = Field()
  greenGamma = Field()
  blueGamma = Field()

  # - XYZ components
  X = Field()
  Y = Field()
  Z = Field()

  #  Validator methods
  @staticmethod
  def _validateIntegerRange(value: int) -> None:
    """Validate that the value is in the range [0, 255]."""
    if value < 0 or value > 255:
      raise IntegerDomainException(value)

  @staticmethod
  def _validateUnitRange(value: float) -> None:
    """Validate that the value is in the range [0.0, 1.0]."""
    if value < 0.0 or value > 1.0:
      raise UnitDomainException(value)

  #  Domain shift methods
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

  #  Accessor methods for the proper variables red, green and blue
  # - Getters
  @red.GET
  def _getRed(self, ) -> int:
    """Get the red color component."""
    return maybe(self.__red_channel__, self.__red_fallback__)

  @green.GET
  def _getGreen(self, ) -> int:
    """Get the green color component."""
    return maybe(self.__green_channel__, self.__green_fallback__)

  @blue.GET
  def _getBlue(self, ) -> int:
    """Get the blue color component."""
    return maybe(self.__blue_channel__, self.__blue_fallback__)

  # - Setters
  @red.SET
  def _setRed(self, value: int) -> None:
    """Set the red color component."""
    self.__red_channel__ = value

  @green.SET
  def _setGreen(self, value: int) -> None:
    """Set the green color component."""
    self.__green_channel__ = value

  @blue.SET
  def _setBlue(self, value: int) -> None:
    """Set the blue color component."""
    self.__blue_channel__ = value

  #  Accessor methods for virtual variables
  # - Getters
  # - - Floating point components
  @redF.GET
  def _getRedF(self, ) -> float:
    """Get the red component as a float."""
    return float(self.red / 255.0)

  @greenF.GET
  def _getGreenF(self, ) -> float:
    """Get the green component as a float."""
    return float(self.green / 255.0)

  @blueF.GET
  def _getBlueF(self, ) -> float:
    """Get the blue component as a float."""
    return float(self.blue / 255.0)

  @F.GET
  def _getF(self, ) -> R3:
    """Get the color as a float."""
    return self.redF, self.greenF, self.blueF

  # - - Components mapped to real number-line
  @redReal.GET
  def _getRedReal(self, ) -> float:
    """Get the red component as a real number."""
    return float(self._unitToReal(self.redF))

  @greenReal.GET
  def _getGreenReal(self, ) -> float:
    """Get the green component as a real number."""
    return float(self._unitToReal(self.greenF))

  @blueReal.GET
  def _getBlueReal(self, ) -> float:
    """Get the blue component as a real number."""
    return float(self._unitToReal(self.blueF))

  # - - Gamma corrected components
  @staticmethod
  def _applyGamma(value: float) -> float:
    """Apply gamma correction to the value."""
    if value < 0.0 or value > 1.0:
      raise UnitDomainException(value)
    if value < 0.04045:
      return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4

  @redGamma.GET
  def _getRedGamma(self, ) -> float:
    """Get the red component as a gamma corrected value."""
    return float(self._applyGamma(self.redF))

  @greenGamma.GET
  def _getGreenGamma(self, ) -> float:
    """Get the green component as a gamma corrected value."""
    return float(self._applyGamma(self.greenF))

  @blueGamma.GET
  def _getBlueGamma(self, ) -> float:
    """Get the blue component as a gamma corrected value."""
    return float(self._applyGamma(self.blueF))

  @X.GET
  def _getX(self, ) -> float:
    """Get the X component of the color."""
    r, g, b = self.redGamma, self.greenGamma, self.blueGamma
    return 0.4124564 * r + 0.3575761 * g + 0.1804375 * b

  @Y.GET
  def _getY(self, ) -> float:
    """Get the Y component of the color."""
    r, g, b = self.redGamma, self.greenGamma, self.blueGamma
    return 0.2126729 * r + 0.7151522 * g + 0.0721750 * b

  @Z.GET
  def _getZ(self, ) -> float:
    """Get the Z component of the color."""
    r, g, b = self.redGamma, self.greenGamma, self.blueGamma
    return 0.0193339 * r + 0.1191920 * g + 0.9503041 * b

  # - Setters
  # - - Floating point components
  @redF.SET
  def _setRedF(self, value: float) -> None:
    """Set the red component from a float."""
    self._validateUnitRange(value)
    self.__red_channel__ = int(round(value * 255.0))

  @greenF.SET
  def _setGreenF(self, value: float) -> None:
    """Set the green component from a float."""
    self._validateUnitRange(value)
    self.__green_channel__ = int(round(value * 255.0))

  @blueF.SET
  def _setBlueF(self, value: float) -> None:
    """Set the blue component from a float."""
    self._validateUnitRange(value)
    self.__blue_channel__ = int(round(value * 255.0))

  # - - Components mapped to real number-line
  @redReal.SET
  def _setRedReal(self, value: float) -> None:
    """Set the red component from a real number."""
    self.__red_channel__ = int(round(self._realToUnit(value) * 255.0))

  @greenReal.SET
  def _setGreenReal(self, value: float) -> None:
    """Set the green component from a real number."""
    self.__green_channel__ = int(round(self._realToUnit(value) * 255.0))

  @blueReal.SET
  def _setBlueReal(self, value: float) -> None:
    """Set the blue component from a real number."""
    self.__blue_channel__ = int(round(self._realToUnit(value) * 255.0))

  # - - Gamma corrected components
  @staticmethod
  def _unApplyGamma(value: float) -> float:
    """
    Unapply gamma correction to the value.
    """
    if value < 0.0 or value > 1.0:
      raise UnitDomainException(value)
    if value < 0.0031308:
      return value * 12.92
    return 1.055 * (value ** (1 / 2.4)) - 0.055

  @redGamma.SET
  def _setRedGamma(self, value: float) -> None:
    """Set the red component from a gamma corrected value."""
    self.redF = self._unApplyGamma(value)

  @greenGamma.SET
  def _setGreenGamma(self, value: float) -> None:
    """Set the green component from a gamma corrected value."""
    self.greenF = self._unApplyGamma(value)

  @blueGamma.SET
  def _setBlueGamma(self, value: float) -> None:
    """Set the blue component from a gamma corrected value."""
    self.blueF = self._unApplyGamma(value)

  # - - XYZ components
  @X.SET
  def _setX(self, value: float) -> None:
    """Set the X component of the color."""
    r, g, b = self.redGamma, self.greenGamma, self.blueGamma
    self.redGamma = value / 0.4124564
    self.greenGamma = value / 0.3575761
    self.blueGamma = value / 0.1804375

  @Y.SET
  def _setY(self, value: float) -> None:
    """Set the Y component of the color."""
    r, g, b = self.redGamma, self.greenGamma, self.blueGamma
    self.redGamma = value / 0.2126729
    self.greenGamma = value / 0.7151522
    self.blueGamma = value / 0.0721750

  @Z.SET
  def _setZ(self, value: float) -> None:
    """Set the Z component of the color."""
    r, g, b = self.redGamma, self.greenGamma, self.blueGamma
    self.redGamma = value / 0.0193339
    self.greenGamma = value / 0.1191920
    self.blueGamma = value / 0.9503041

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int, int, int)
  def __init__(self, *args: int) -> None:
    """Initialize RougeVertBleu with red, green, and blue values."""
    for arg in args:
      self._validateIntegerRange(arg)
    self.__red_channel__ = args[0]
    self.__green_channel__ = args[1]
    self.__blue_channel__ = args[2]

  @overload(int)
  def __init__(self, monoChrome: int) -> None:
    """Initialize RougeVertBleu with a single integer value."""
    self.__init__(monoChrome, monoChrome, monoChrome)

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    """Initialize RougeVertBleu with a RougeVertBleu instance."""
    if TYPE_CHECKING:
      assert isinstance(other.red, int)
      assert isinstance(other.green, int)
      assert isinstance(other.blue, int)
    self.__init__(other.red, other.green, other.blue)

  @overload(QColor)
  def __init__(self, color: QColor) -> None:
    """Initialize RougeVertBleu with a QColor instance."""
    self.__init__(color.red(), color.green(), color.blue())

  @overload(str)
  def __init__(self, color: str) -> None:
    """Initialize RougeVertBleu with a color name."""
    values = getcolor(color, 'RGB')

  @overload()
  def __init__(self, **kwargs) -> None:
    """Initialize with keyword arguments"""
    redKeys = """red, r, redValue, redComponent"""
    greenKeys = """green, g, greenValue, greenComponent"""
    blueKeys = """blue, b, blueValue, blueComponent"""
    KEYS = [stringList(k) for k in [redKeys, greenKeys, blueKeys]]
    names = stringList("""red, green, blue""")
    defaultValues = dict(red=255, green=255, blue=255, )
    kwargValues = dict(red=-1, green=-1, blue=-1, )
    for name, keys in zip(names, KEYS):
      for key in keys:
        if key in kwargs:
          kwargValues[name] = kwargs[key]
          break
      else:
        kwargValues[name] = defaultValues[name]
    values = [kwargValues[name] for name in names]
    self.__init__(*values)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  IMPLEMENTATION OF ITERATION  # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Self:
    """Iterate over the color components."""
    self.__iter_contents__ = [self.red, self.green, self.blue]
    return self

  def __next__(self, ) -> int:
    """Get the next color component."""
    try:
      out = self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration
    else:
      return out
    finally:
      if not self.__iter_contents__:
        self.__iter_contents__ = None

  def __len__(self, ) -> int:
    """Get the number of color components."""
    return 3

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  IMPLEMENTATION OF DICTIONARY   # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getGetMap(self, ) -> GetMap:
    """Get getter mapping."""
    return {
        'red'      : self._getRed,
        'green'    : self._getGreen,
        'blue'     : self._getBlue,
        'redF'     : self._getRedF,
        'greenF'   : self._getGreenF,
        'blueF'    : self._getBlueF,
        'redReal'  : self._getRedReal,
        'greenReal': self._getGreenReal,
        'blueReal' : self._getBlueReal,
        0          : self._getRed,
        1          : self._getGreen,
        2          : self._getBlue,
    }

  def _getSetMap(self, ) -> Any:
    """Get setter mapping. """
    return {
        'red'      : self._setRed,
        'green'    : self._setGreen,
        'blue'     : self._setBlue,
        'redF'     : self._setRedF,
        'greenF'   : self._setGreenF,
        'blueF'    : self._setBlueF,
        'redReal'  : self._setRedReal,
        'greenReal': self._setGreenReal,
        'blueReal' : self._setBlueReal,
        0          : self._setRed,
        1          : self._setGreen,
        2          : self._setBlue,
    }

  @overload(int)
  def __getitem__(self, index: int) -> int:
    """Get the color component at the given index."""
    if index > 2:
      raise IndexError
    if index < 0:
      return self[len(self) + index]
    data = self._getGetMap()
    try:
      value = data[index]()
    except KeyError:
      raise IndexError
    else:
      return value
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        pycharmPlease = 69420
        assert isinstance(pycharmPlease, int)
        return pycharmPlease
      else:
        pass

  @overload(slice)
  def __getitem__(self, index: slice) -> list[int]:
    """Get the color components in the given range."""
    if index.start is None:
      start = 0
    else:
      start = index.start
    if index.stop is None:
      stop = len(self)
    else:
      stop = index.stop
    if start < 0 or stop > len(self):
      raise IndexError
    return [self[i] for i in range(start, stop)]

  @overload(str)
  def __getitem__(self, key: str) -> int:
    """Get the color component with the given name."""
    data = self._getGetMap()
    try:
      value = data[key]()
    except KeyError:
      raise KeyError
    else:
      return value
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        pycharmPlease = 69420
        assert isinstance(pycharmPlease, int)
        return pycharmPlease
      else:
        pass

  @overload(int, int)
  def __setitem__(self, index: int, value: int) -> None:
    """Set the color component at the given index."""
    if index > 2:
      raise IndexError
    if index < 0:
      return self.__setitem__(len(self) + index, value)
    data = self._getSetMap()
    try:
      setterFunc = data[index]
    except KeyError:
      raise IndexError
    else:
      setterFunc(value)
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        return None
      else:
        return None

  @overload(slice, list)
  def __setitem__(self, index: slice, value: list[int]) -> None:
    """Set the color components in the given range."""
    if index.start is None:
      start = 0
    else:
      start = index.start
    if index.stop is None:
      stop = len(self)
    else:
      stop = index.stop
    if start < 0 or stop > len(self):
      raise IndexError
    for i in range(start, stop):
      self[i] = value[i - start]

  @overload(str, float)
  @overload(str, int)
  def __setitem__(self, key: str, value: int) -> None:
    """Set the color component with the given name."""
    data = self._getSetMap()
    try:
      setterFunc = data[key]
    except KeyError:
      raise KeyError
    else:
      setterFunc(value)
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        return None
      else:
        return None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  IDENTITIES   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _resolveOther(self, other: Any) -> Self:
    """Resolve other object to self."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    if isinstance(other, (tuple, list)):
      args = (*other,)
    else:
      args = other
    try:
      out = cls(*args)
    except DispatchException:
      return NotImplemented
    else:
      return out
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        pycharmPlease = 69420
        assert isinstance(pycharmPlease, cls)
        return pycharmPlease
      else:
        pass

  def __eq__(self, other: Any) -> bool:
    """
    Check if two RougeVertBleu objects are equal.
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    if (self.red - other.red) ** 2:
      return False
    if (self.green - other.green) ** 2:
      return False
    if (self.blue - other.blue) ** 2:
      return False
    return True

  def __hash__(self, ) -> int:
    """Return the hash of the color."""
    return hash((self.red, self.green, self.blue))

  def __abs__(self, ) -> float:
    """Return the absolute value of the color."""
    return (self.red ** 2 + self.green ** 2 + self.blue ** 2) ** 0.5

  def __bool__(self, ) -> bool:
    """Return True if the color is not black."""
    return True if any([*self, ]) else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  String and Code Representation   # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self, ) -> str:
    """String representation has the form #RRGGBBAA if alpha is not 255.
    Otherwise, it has the form #RRGGBB."""
    r = self.red
    g = self.green
    b = self.blue
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

  def __repr__(self, ) -> str:
    """Code representation creates a str that would create self if passed
    to eval. """
    clsName = type(self).__name__
    r = '%d' % self.red
    g = '%d' % self.green
    b = '%d' % self.blue
    infoSpec = """%s(%s, %s, %s)"""
    info = infoSpec % (clsName, r, g, b)
    return info

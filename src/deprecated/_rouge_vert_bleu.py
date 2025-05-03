"""RougeVertBleu provides a dataclass of sorts representing a color in RGB
space including an alpha channel. The class implements a flexible constructor
thanks to the overload system from 'worktoy'. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor
from PIL.ImageColor import getcolor, colormap

from worktoy.static import overload, THIS
from worktoy.attr import AttriBox
from worktoy.mcls import BaseObject
from worktoy.text import stringList, monoSpace
from worktoy.waitaminute import DispatchException

from .waitaminute import UnitRangeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any


class RougeVertBleu(BaseObject):
  """RGB represents a color in RGB space."""

  #  Public Variables
  red = AttriBox[int](255)  # Red component
  green = AttriBox[int](255)  # Green component
  blue = AttriBox[int](255)  # Blue component
  alpha = AttriBox[int](255)  # Alpha component

  @overload(int, int, int, int)
  def __init__(self, *args) -> None:
    """Initialize RougeVertBleu with red, green, blue, and alpha values."""
    self.red, self.green, self.blue, self.alpha = args

  @overload(float, float, float, float)
  def __init__(self, *args) -> None:
    """Initialize RougeVertBleu with red, green, blue, and alpha values."""
    intArgs = []
    for arg in args:
      if arg > 1.0 or arg < 0.0:
        raise UnitRangeException(arg)
      intArgs.append(int(round(arg * 255)))
    self.red, self.green, self.blue, self.alpha = intArgs

  @overload(int, int, int)
  def __init__(self, *args) -> None:
    """Initialize RougeVertBleu with red, green, and blue values."""
    self.__init__(*args, 255)

  @overload(float, float, float)
  def __init__(self, *args) -> None:
    """Initialize RougeVertBleu with red, green, and blue values."""
    self.__init__(*args, 1.0)

  @overload(float, float)
  @overload(int, int)
  def __init__(self, *args) -> None:
    """Initialize RougeVertBleu with red and green values."""
    self.__init__(args[0], args[0], args[0], args[1])

  @overload(int)
  def __init__(self, *args) -> None:
    """Initialize RougeVertBleu with a single integer value."""
    self.__init__(args[0], args[0], args[0], 255)

  @overload(float)
  def __init__(self, *args) -> None:
    """Initialize RougeVertBleu with a single float value."""
    self.__init__(args[0], args[0], args[0], 1.0)

  @overload(str)
  def __init__(self, color: str) -> None:
    """Initialize RougeVertBleu with a color name."""
    if color.lower() in colormap:
      value = colormap[color.lower()]
    try:
      value = getcolor(color, 'RGBA')
    except ValueError as valueError:
      raise ValueError
    else:
      self.__init__(*value)
    finally:
      pass

  @overload(THIS)
  def __init__(self, color: Self) -> None:
    """Initialize RougeVertBleu with another RougeVertBleu object."""
    self.__init__(color.red, color.green, color.blue, color.alpha)

  @overload(QColor)
  def __init__(self, color: QColor) -> None:
    """Initialize RougeVertBleu with a QColor object."""
    self.__init__(color.red(), color.green(), color.blue(), color.alpha())

  @overload()
  def __init__(self, **kwargs) -> None:
    """Initialize RougeVertBleu with no arguments."""
    redKeys = """red, r, redValue, redComponent"""
    greenKeys = """green, g, greenValue, greenComponent"""
    blueKeys = """blue, b, blueValue, blueComponent"""
    alphaKeys = """alpha, a, alphaValue, alphaComponent"""
    KEYS = [stringList(k) for k in [redKeys, greenKeys, blueKeys, alphaKeys]]
    names = stringList("""red, green, blue, alpha""")
    defaultValues = dict(red=255, green=255, blue=255, alpha=255)
    kwargValues = dict(red=-1, green=-1, blue=-1, alpha=-1)
    for name, keys in zip(names, KEYS):
      for key in keys:
        if key in kwargs:
          kwargValues[name] = kwargs[key]
          break
      else:
        kwargValues[name] = defaultValues[name]
    values = [kwargValues[name] for name in names]
    self.__init__(*values)

  def _resolveOther(self, other: Any) -> Self:
    """Resolve other object to self."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    try:
      other = cls(other)
    except DispatchException:
      return NotImplemented
    else:
      return other
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        pycharmPlease = 69420
        assert isinstance(pycharmPlease, cls)
        return pycharmPlease
      else:
        pass

  def __eq__(self, other: Any) -> bool:
    """Check if two RougeVertBleu objects are equal."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    loss = dict(
        red=(self.red - other.red) ** 2,
        green=(self.green - other.green) ** 2,
        blue=(self.blue - other.blue) ** 2,
        alpha=(self.alpha - other.alpha) ** 2
    )
    absLoss = sum(loss.values())
    if not absLoss:
      return True
    if absLoss < 16:
      infoSpec = """Received almost equal with losses: \n%s"""
      components = ['%s: %d' % (key, value) for key, value in loss.items()]
      componentStr = '<br><tab>'.join(components)
      info = monoSpace(infoSpec % componentStr)
      print(info)
      return True
    return False

  def __hash__(self, ) -> int:
    """Return the hash of the color."""
    return hash((self.red, self.green, self.blue, self.alpha))

  def __abs__(self, ) -> float:
    """Return the absolute value of the color."""
    return (self.red ** 2 + self.green ** 2 + self.blue ** 2) ** 0.5

  def __bool__(self, ) -> bool:
    """Return True if the alpha channel is not 0."""
    return True if self.alpha else False

  def __str__(self, ) -> str:
    """String representation has the form #RRGGBBAA if alpha is not 255.
    Otherwise, it has the form #RRGGBB."""
    r = self.red
    g = self.green
    b = self.blue
    a = self.alpha
    if a == 255:
      return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
    else:
      return f"#{int(r):02x}{int(g):02x}{int(b):02x}{int(a):02x}"

  def __repr__(self, ) -> str:
    """Code representation creates a str that would create self if passed
    to eval. """
    clsName = type(self).__name__
    r = '%d' % self.red
    g = '%d' % self.green
    b = '%d' % self.blue
    if self.alpha == 255:
      a = ''
    else:
      a = '%d' % self.alpha
    infoSpec = """%s(%s, %s, %s, %s)"""
    info = infoSpec % (clsName, r, g, b, a)
    return info

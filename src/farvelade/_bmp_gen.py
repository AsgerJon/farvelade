"""BMPGen provides a bitmap file generator."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from io import BufferedIOBase

from worktoy.attr import Field, AttriBox
from worktoy.mcls import BaseObject
from worktoy.parse import maybe
from worktoy.waitaminute import MissingVariable, TypeException, \
  SubclassException
from worktoy.waitaminute import VariableNotNone
from worktoy.work_io import FidGen

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias, Never

  RGB: TypeAlias = tuple[int, int, int]
else:
  try:
    from typing import Callable
  except ImportError:
    try:
      from typing_extensions import Callable
    except ImportError:
      try:
        from types import FunctionType as Callable
      except ImportError:
        def func() -> None:
          pass


        Callable = type(func)


class BMPGen(BaseObject):
  """
  BMPGen provides a bitmap file generator.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  __field_name__ = None
  __field_owner__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """
    Set the name of the BMPGen.
    """
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: Any, owner: type, ) -> Any:
    """Getter-function updates the current owner and instance,
    then returns self. """
    self._setCurrentOwner(owner)
    self._setCurrentInstance(instance)
    return self

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __fallback_painter__ = lambda x, y: (0, 0, 0)

  #  Private variables
  __painter_name__ = None
  __current_instance__ = None
  __current_owner__ = None

  #  Public variables
  width = AttriBox[int](128)
  height = AttriBox[int](128)
  fid = FidGen('mandelbrot', 'bmp')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def _getPainterName(self, ) -> str:
    """
    Get the name of the painter.
    """
    if self.__painter_name__ is None:
      raise MissingVariable('__painter_name__', str)
    if isinstance(self.__painter_name__, str):
      return self.__painter_name__
    raise TypeException('__painter_name__', self.__painter_name__, str)

  def _getCurrentOwner(self, ) -> type:
    """
    Get the current owner of the painter.
    """
    owner = maybe(self.__current_owner__, self.__field_owner__)
    if isinstance(owner, type):
      return owner
    if owner is None:
      raise MissingVariable('__current_owner__', type)
    raise TypeException('__current_owner__', owner, type)

  def _getCurrentInstance(self, ) -> Any:
    """
    Get the current instance of the painter.
    """
    if self.__current_instance__ is None:
      return  # None is allowed
    try:
      owner = self._getCurrentOwner()
    except MissingVariable:
      return self.__current_instance__
    else:
      if isinstance(self.__current_instance__, owner):
        return self.__current_instance__
      raise TypeException(
          '__current_instance__',
          self.__current_instance__,
          owner
      )
    finally:
      pass

  def _getPainter(self, ) -> Callable:
    """Getter-function for the painter function"""
    if self.__painter_name__ is None:
      return self.__fallback_painter__
    instance = self._getCurrentInstance()
    owner = self._getCurrentOwner()
    paintName = self._getPainterName()
    if instance is None:
      if owner is None:
        return self.__fallback_painter__
      painter = getattr(owner, paintName, )
      if isinstance(painter, (staticmethod, classmethod), ):
        return painter

      def wrapper(x: int, y: int) -> tuple[int, int, int]:
        """Fallback pixel RGB function."""
        return painter(None, x, y)

      return wrapper
    painter = getattr(instance, paintName, None)
    if painter is None:
      raise MissingVariable(paintName, Callable)
    if callable(painter):
      return painter
    raise TypeException(paintName, painter, Callable)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setPainterName(self, callMeMaybe: Callable) -> Callable:
    """
    Set the name of the painter.
    """
    if self.__painter_name__ is not None:
      raise VariableNotNone('__painter_name__', )
    if not callable(callMeMaybe):
      raise TypeException('__painter_name__', callMeMaybe, Callable)
    self.__painter_name__ = callMeMaybe.__name__
    return callMeMaybe

  def PAINT(self, callMeMaybe: Callable) -> Callable:
    """
    Set the name of the painter.
    """
    return self._setPainterName(callMeMaybe)

  def _setCurrentOwner(self, owner: type) -> None:
    """Setter-function for the current owner. """
    if not issubclass(owner, self.__field_owner__):
      raise SubclassException(owner, self.__field_owner__)
    self.__current_owner__ = owner

  def _setCurrentInstance(self, instance: Any) -> None:
    """Setter-function for the current instance"""
    if self.__current_instance__ is instance:
      return
    owner = self._getCurrentOwner()
    if not isinstance(instance, owner):
      raise TypeException('__current_instance__', instance, owner)
    self.__current_instance__ = instance

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def render(self, buffer: BufferedIOBase) -> None:
    """
    Render the bitmap to the buffer.
    """
    painter = self._getPainter()
    #  Write the BMP header
    buffer.write(b'BM')
    buffer.write((self.width * self.height * 3 + 54).to_bytes(4, 'little'))
    buffer.write((0).to_bytes(4, 'little'))
    buffer.write((54).to_bytes(4, 'little'))
    #  Write the DIB header
    buffer.write((40).to_bytes(4, 'little'))
    buffer.write(self.width.to_bytes(4, 'little'))
    buffer.write(self.height.to_bytes(4, 'little'))
    buffer.write((1).to_bytes(2, 'little'))
    buffer.write((24).to_bytes(2, 'little'))
    buffer.write((0).to_bytes(4, 'little'))
    buffer.write((self.width * self.height * 3).to_bytes(4, 'little'))
    buffer.write((2835).to_bytes(4, 'little'))
    buffer.write((2835).to_bytes(4, 'little'))
    buffer.write((0).to_bytes(4, 'little'))
    buffer.write((0).to_bytes(4, 'little'))
    #  Write the pixel data
    for y in range(self.height):
      for x in range(self.width):
        r, g, b = painter(x, y)
        buffer.write(bytes([b, g, r]))
      #  Padding to the next 4-byte boundary
      buffer.write(b'\x00' * ((4 - (self.width * 3) % 4) % 4))

  def save(self, ) -> None:
    """
    Save the bitmap to the file.
    """
    buffer = None
    try:
      buffer = open(self.fid.filePath, 'wb')
    except OSError as osError:
      infoSpec = """When trying to generate bitmap file: '%s' the 
      following exception was encountered: '%s'!"""
      info = infoSpec % (self.fid.filePath, type(osError).__name__)
      raise OSError(info) from osError
    else:
      self.render(buffer)
    finally:
      if hasattr(buffer, 'close'):
        buffer.close()
      else:
        pass

  def paint(self, x: int, y: int) -> RGB:
    """
    Paint the pixel at (x, y) with the given RGB value.
    """

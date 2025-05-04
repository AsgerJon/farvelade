"""Luma implements a descriptor for the RougeVertBleu class exposing the
luma color value. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from math import atanh, tanh

from PIL.ImageColor import colormap, getcolor
from PySide6.QtGui import QColor
from worktoy.text import monoSpace, stringList
from worktoy.parse import maybe
from worktoy.static import overload, THIS
from worktoy.attr import Field, AttriBox, AbstractDescriptor
from worktoy.mcls import BaseObject
from worktoy.waitaminute import DispatchException, SubclassException

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

  from . import RougeVertBleu

epsilon = 1e-10


class Luma(AbstractDescriptor):
  """Luma implements a descriptor for the RougeVertBleu class exposing the
  luma color value. """

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field."""
    from . import RougeVertBleu
    if not issubclass(owner, RougeVertBleu):
      raise SubclassException(owner, RougeVertBleu)
    AbstractDescriptor.__set_name__(self, owner, name)

  def _instanceGet(self, instance: Any) -> float:
    """Get the luma value."""

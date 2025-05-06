"""BitMapinator provides a bitmap file generator. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attr import AttriBox, Field
from worktoy.mcls import BaseObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias


class BitMapinator(BaseObject):
  """
  BitMapinator provides a bitmap file generator.
  """

  #  Python API
  __iter_contents__ = None

  def __iter__(self, ) -> Self:
    raise NotImplementedError

  def __next__(self, ) -> Any:
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __len__(self, ) -> int:
    raise NotImplementedError

  def __contains__(self, item: Any) -> bool:
    raise NotImplementedError

  #  Fallback variables
  #  Private variables
  __image_pixels__ = None

  #  Public variables
  width = AttriBox[int](128)
  height = AttriBox[int](128)
  pixels = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Getters  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

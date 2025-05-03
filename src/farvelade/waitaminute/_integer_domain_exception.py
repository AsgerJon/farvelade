"""IntegerDomainException is raised to indicate that a given value failed to
fall in the range of a uint8 value (0-255)."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace
from worktoy.waitaminute import DispatchException

from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


class IntegerDomainException(ValueError):
  """IntegerDomainException is raised to indicate that a given value
  failed to fall in the range of a uint8 value (0-255)."""

  value = _Attribute()

  def __init__(self, value: float) -> None:
    infoSpec = """Expected integer value to be in 8 bit range (0-255),
    but received value: '%d'""" % value
    self.value = value
    info = monoSpace(infoSpec % value)
    ValueError.__init__(self, info)

  def _resolveOther(self, other: Any) -> Self:
    """
    Resolve other object to self.
    """
    cls = type(self)
    if isinstance(other, cls):
      return other
    try:
      out = cls(other)
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
    Check if two IntegerDomainException objects are equal.
    """
    other = self._resolveOther(other)
    if other is NotImplemented:
      return False
    cls = type(self)
    if isinstance(other, cls):
      return self.value == other.value
    return False

"""UnitRangeException is a custom class raised to indicate that a float
were expected in unit range but was not."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

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


class UnitDomainException(ValueError):
  """UnitRangeException is a custom class raised to indicate that a float
  were expected in unit range but was not."""

  value = _Attribute()

  def __init__(self, value: float) -> None:
    infoSpec = """Expected floating point value to be in unit range, 
    but received value: '%.3f'"""
    self.value = value
    info = monoSpace(infoSpec % value)
    ValueError.__init__(self, info)

  def _resolveOther(self, other: Any, ) -> Self:
    """Resolve other object to self."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    if isinstance(other, float):
      return cls(other)
    try:
      other = float(other)
    except (TypeError, ValueError):
      return NotImplemented
    else:
      return cls(other)
    finally:
      if TYPE_CHECKING:  # pycharm, please!
        pycharmPlease = 69420
        assert isinstance(pycharmPlease, cls)
        return pycharmPlease
      else:
        pass

  def __eq__(self, other: Any) -> bool:
    """Check if two UnitRangeException objects are equal."""
    other = self._resolveOther(other)
    if other is NotImplemented:
      return NotImplemented
    return True if (self.value - other.value) ** 2 < 1e-12 else False

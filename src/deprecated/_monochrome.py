"""Monochrome represents a monochrome color in RGB space."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class Monochrome(BaseObject):
  """Monochrome represents a monochrome color in RGB space."""
  pass

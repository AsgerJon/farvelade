"""The 'farvelade' module provides colour representations and interfaces
to external libraries such as QColor in Qt"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._pixel import Pixel

from ._rouge_vert_bleu import RougeVertBleu
from ._ok_lab import OKLab

__all__ = [
    'RougeVertBleu',
    'OKLab',
]

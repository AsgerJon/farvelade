"""TestPixel tests the Pixel class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject

from farvelade.sample_card import Pixel

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Union, Self, Callable, TypeAlias


class TestPixel(TestCase):
  """TestPixel tests the Pixel class."""

  def setUp(self) -> None:
    """Uses different constructor overloads"""
    self.pixel1 = Pixel(69, 420)
    self.pixel11 = Pixel(self.pixel1)
    self.pixel2 = Pixel(1337 + 80085 * 1j)
    self.pixel3 = Pixel(horizontal=1, vertical=1)
    self.pixel4 = Pixel(x=2, y=3)

  def test_init(self, ) -> None:
    """Tests the different constructor overloads"""
    self.assertEqual(self.pixel1.x, 69)
    self.assertEqual(self.pixel1.y, 420)
    self.assertEqual(self.pixel11.x, 69)
    self.assertEqual(self.pixel11.y, 420)
    self.assertEqual(self.pixel2.x, 1337)
    self.assertEqual(self.pixel2.y, 80085)
    self.assertEqual(self.pixel3.x, 1)
    self.assertEqual(self.pixel3.y, 1)
    self.assertEqual(self.pixel4.x, 2)
    self.assertEqual(self.pixel4.y, 3)

  def test_iter(self, ) -> None:
    """Tests the __iter__ method"""
    x1, y1 = self.pixel1
    x2, y2 = self.pixel2
    x3, y3 = self.pixel3
    x4, y4 = self.pixel4
    x11, y11 = self.pixel11
    self.assertEqual(x1, 69)
    self.assertEqual(y1, 420)
    self.assertEqual(x2, 1337)
    self.assertEqual(y2, 80085)
    self.assertEqual(x3, 1)
    self.assertEqual(y3, 1)
    self.assertEqual(x4, 2)
    self.assertEqual(y4, 3)
    self.assertEqual(x11, 69)
    self.assertEqual(y11, 420)

  def test_get_item_index(self) -> None:
    """Tests the __getitem__ method"""
    self.assertEqual(self.pixel1[0], 69)
    self.assertEqual(self.pixel1[1], 420)
    self.assertEqual(self.pixel2[0], 1337)
    self.assertEqual(self.pixel2[1], 80085)
    self.assertEqual(self.pixel3[0], 1)
    self.assertEqual(self.pixel3[1], 1)
    self.assertEqual(self.pixel4[0], 2)
    self.assertEqual(self.pixel4[1], 3)
    self.assertEqual(self.pixel11[0], 69)
    self.assertEqual(self.pixel11[1], 420)

  def test_get_item_key(self, ) -> None:
    """Tests the __getitem__ method"""
    self.assertEqual(self.pixel1["x"], 69)
    self.assertEqual(self.pixel1["y"], 420)
    self.assertEqual(self.pixel2["x"], 1337)
    self.assertEqual(self.pixel2["y"], 80085)
    self.assertEqual(self.pixel3["x"], 1)
    self.assertEqual(self.pixel3["y"], 1)
    self.assertEqual(self.pixel4["x"], 2)
    self.assertEqual(self.pixel4["y"], 3)
    self.assertEqual(self.pixel11["x"], 69)
    self.assertEqual(self.pixel11["y"], 420)

  def test_get_item_slice(self) -> None:
    """Tests the __getitem__ method"""
    x1, y1 = self.pixel1[:]
    y2, x2 = self.pixel2[::-1]
    x3, y3 = self.pixel3[::]
    x4, y4 = self.pixel4[0:2]
    x11 = self.pixel11[0:1]
    y11 = self.pixel11[1:2]
    self.assertEqual(x1, 69)
    self.assertEqual(y1, 420)
    self.assertEqual(x2, 1337)
    self.assertEqual(y2, 80085)
    self.assertEqual(x3, 1)
    self.assertEqual(y3, 1)
    self.assertEqual(x4, 2)
    self.assertEqual(y4, 3)
    self.assertEqual(x11, [69, ])
    self.assertEqual(y11, [420, ])

  def test_set_item_index(self, ) -> None:
    """Tests the __setitem__ method"""
    self.pixel1[0] = 1337
    self.pixel1[1] = 80085
    self.pixel2[0] = 69
    self.pixel2[1] = 420
    self.pixel3[0] = 2
    self.pixel3[1] = 3
    self.pixel4[0] = 69
    self.pixel4[1] = 420
    self.assertEqual(self.pixel1.x, 1337)
    self.assertEqual(self.pixel1.y, 80085)
    self.assertEqual(self.pixel2.x, 69)
    self.assertEqual(self.pixel2.y, 420)
    self.assertEqual(self.pixel3.x, 2)
    self.assertEqual(self.pixel3.y, 3)
    self.assertEqual(self.pixel4.x, 69)
    self.assertEqual(self.pixel4.y, 420)

  def test_set_item_key(self) -> None:
    """Tests the __setitem__ method"""
    self.pixel1["x"] = 1337
    self.pixel1["y"] = 80085
    self.pixel2["x"] = 69
    self.pixel2["y"] = 420
    self.pixel3["x"] = 2
    self.pixel3["y"] = 3
    self.pixel4["x"] = 69
    self.pixel4["y"] = 420
    self.assertEqual(self.pixel1.x, 1337)
    self.assertEqual(self.pixel1.y, 80085)
    self.assertEqual(self.pixel2.x, 69)
    self.assertEqual(self.pixel2.y, 420)
    self.assertEqual(self.pixel3.x, 2)
    self.assertEqual(self.pixel3.y, 3)
    self.assertEqual(self.pixel4.x, 69)
    self.assertEqual(self.pixel4.y, 420)

  def test_set_item_slice(self) -> None:
    """Tests the __setitem__ method"""
    self.pixel1[0:2] = [1337, 80085]
    self.pixel2[0:2] = [69, 420]
    self.pixel3[0:2] = [2, 3]
    self.pixel4[0:2] = [69, 420]
    self.assertEqual(self.pixel1.x, 1337)
    self.assertEqual(self.pixel1.y, 80085)
    self.assertEqual(self.pixel2.x, 69)
    self.assertEqual(self.pixel2.y, 420)
    self.assertEqual(self.pixel3.x, 2)
    self.assertEqual(self.pixel3.y, 3)
    self.assertEqual(self.pixel4.x, 69)
    self.assertEqual(self.pixel4.y, 420)

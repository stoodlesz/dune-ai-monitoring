"""Image tiling helpers for preparing model-ready patches."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import numpy as np


@dataclass(frozen=True)
class TileWindow:
    """Pixel-space tile location."""

    x: int
    y: int
    width: int
    height: int

    @property
    def slices(self) -> tuple[slice, slice]:
        return (slice(self.y, self.y + self.height), slice(self.x, self.x + self.width))


def iter_windows(
    image_width: int,
    image_height: int,
    tile_size: int | tuple[int, int],
    stride: int | tuple[int, int] | None = None,
    *,
    drop_partial: bool = True,
) -> Iterator[TileWindow]:
    """Yield tile windows across an image from top-left to bottom-right."""

    tile_width, tile_height = _as_pair(tile_size)
    stride_width, stride_height = _as_pair(stride or tile_size)
    _validate_positive("image_width", image_width)
    _validate_positive("image_height", image_height)
    _validate_positive("tile_width", tile_width)
    _validate_positive("tile_height", tile_height)
    _validate_positive("stride_width", stride_width)
    _validate_positive("stride_height", stride_height)

    for y in range(0, image_height, stride_height):
        for x in range(0, image_width, stride_width):
            width = min(tile_width, image_width - x)
            height = min(tile_height, image_height - y)
            if drop_partial and (width != tile_width or height != tile_height):
                continue
            yield TileWindow(x=x, y=y, width=width, height=height)


def tile_array(
    image: np.ndarray,
    tile_size: int | tuple[int, int],
    stride: int | tuple[int, int] | None = None,
    *,
    drop_partial: bool = True,
) -> list[np.ndarray]:
    """Split a 2D or channel-last 3D image array into tiles."""

    if image.ndim not in (2, 3):
        raise ValueError("image must be a 2D array or a channel-last 3D array")

    height, width = image.shape[:2]
    tiles = []
    for window in iter_windows(width, height, tile_size, stride, drop_partial=drop_partial):
        y_slice, x_slice = window.slices
        tiles.append(image[y_slice, x_slice].copy())
    return tiles


def _as_pair(value: int | tuple[int, int]) -> tuple[int, int]:
    if isinstance(value, int):
        return value, value
    if len(value) != 2:
        raise ValueError("expected an int or a two-item tuple")
    return value


def _validate_positive(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


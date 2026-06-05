"""Spectral index helpers for vegetation and water signals."""

from __future__ import annotations

import numpy as np


def normalized_difference(
    band_a: np.ndarray,
    band_b: np.ndarray,
    *,
    epsilon: float = 1e-10,
) -> np.ndarray:
    """Compute (A - B) / (A + B) with stable zero handling."""

    a = np.asarray(band_a, dtype=np.float32)
    b = np.asarray(band_b, dtype=np.float32)
    if a.shape != b.shape:
        raise ValueError("band_a and band_b must have the same shape")
    return (a - b) / (a + b + epsilon)


def ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """Compute Normalized Difference Vegetation Index from NIR and red bands."""

    return normalized_difference(nir, red)


def ndwi(green: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """Compute Normalized Difference Water Index from green and NIR bands."""

    return normalized_difference(green, nir)


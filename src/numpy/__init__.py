"""
NumPy Matrix/Image Processing and Conversion Module.
Exposes utility functions for converting and manipulating N-dimensional arrays.
"""

from .converter import (
    normalize_matrix,
    convert_to_grayscale,
    apply_threshold_mask,
    rotate_matrix_90,
    downsample_matrix,
)

__all__ = [
    "normalize_matrix",
    "convert_to_grayscale",
    "apply_threshold_mask",
    "rotate_matrix_90",
    "downsample_matrix",
]
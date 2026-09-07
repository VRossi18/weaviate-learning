import numpy as np
import pytest

from src.numpy.converter import convert_to_grayscale, normalize_matrix


class TestNormalizeMatrix:
    """Tests for Challenge 1: Min-Max Normalization"""

    def test_normalize_basic_array(self):
        matrix = np.array([[0, 5], [10, 5]], dtype=float)
        expected = np.array([[0.0, 0.5], [1.0, 0.5]], dtype=float)

        result = normalize_matrix(matrix)

        np.testing.assert_allclose(result, expected)
        assert result.dtype == np.float64

    def test_normalize_same_min_max_returns_zeros(self):
        matrix = np.array([[5, 5], [5, 5]], dtype=float)
        expected = np.zeros_like(matrix, dtype=np.float64)

        result = normalize_matrix(matrix)

        np.testing.assert_array_equal(result, expected)

    def test_normalize_3d_array(self):
        matrix = np.array([[[0, 100]], [[50, 200]]], dtype=float)
        result = normalize_matrix(matrix)

        assert result.min() == 0.0
        assert result.max() == 1.0


class TestConvertToGrayscale:
    """Tests for Challenge 2: RGB -> Grayscale Conversion"""

    def test_convert_grayscale_valid_shape(self):
        # Pure White (255, 255, 255) and Pure Black (0, 0, 0)
        rgb_image = np.array(
            [[[255, 255, 255], [0, 0, 0]], [[100, 150, 200], [50, 50, 50]]],
            dtype=float,
        )

        result = convert_to_grayscale(rgb_image)

        assert result.shape == (2, 2)
        # Check white pixel luminance (0.299*255 + 0.587*255 + 0.114*255 = 255)
        assert pytest.approx(result[0, 0], 0.01) == 255.0
        # Check black pixel luminance
        assert pytest.approx(result[0, 1], 0.01) == 0.0

    def test_convert_grayscale_invalid_channels_raises_value_error(self):
        # Passing an image with 4 channels (RGBA) instead of 3 (RGB)
        invalid_image = np.zeros((10, 10, 4))

        with pytest.raises(ValueError):
            convert_to_grayscale(invalid_image)
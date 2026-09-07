import numpy as np 

def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Challenge 1: Min-Max Normalization
    
    Scales all numerical values in the array to a dynamic range between 0.0 and 1.0.
    
    Formula: (X - min) / (max - min)
    
    Requirements:
    - Must work for 2D or 3D arrays with any numeric data type.
    - Return a NumPy array with dtype float64.
    - Handle the edge case where max == min (return a zero-filled array of the same shape).
    """
    normalized = (matrix - np.min(matrix) - (np.max(matrix) - np.min(matrix)))
    return normalized


def convert_to_grayscale(rgb_image: np.ndarray) -> np.ndarray:
    """
    Challenge 2: RGB -> Grayscale Conversion (Luminance)
    
    Takes a 3D array representing an RGB image (height, width, 3 channels)
    and converts it to a 2D array (height, width) using weighted luminance.
    
    Luminance Formula: Y = 0.299 * R + 0.587 * G + 0.114 * B
    
    Requirements:
    - The input array must have shape (H, W, 3). Raise ValueError if channels count is not 3.
    - Use matrix dot product or vectorized broadcasting (e.g., np.dot or np.sum with weights).
    - Return a 2D float array.
    """
    if rgb_image.ndim != 3 or rgb_image.shape[2] != 3:
        raise ValueError(f"Input must have shape (H, W, 3). Got shape {rgb_image.shape}")

    weights = np.array([0.299, 0.587, 0.114])

    return np.dot(rgb_image, weights)


def apply_threshold_mask(
    matrix: np.ndarray, 
    threshold: float, 
    replacement_value: float = 0.0
) -> np.ndarray:
    """
    Challenge 3: Binarization / Boolean Masking
    
    Applies a boolean mask: all elements strictly less than 'threshold' 
    must be replaced by 'replacement_value'. Elements greater than or equal 
    to the threshold must remain unchanged.
    
    Requirements:
    - Use native NumPy boolean indexing or np.where.
    - Do not modify the original array (return a modified copy).
    """
    # TODO: Implement using boolean indexing or np.where
    raise NotImplementedError("Implement apply_threshold_mask function")


def rotate_matrix_90(matrix: np.ndarray, clockwise: bool = True) -> np.ndarray:
    """
    Challenge 4: Axis Manipulation & Linear Algebra
    
    Rotates a 2D matrix by 90 degrees clockwise or counter-clockwise.
    
    Requirements:
    - Hint: A 90-degree rotation can be achieved by combining matrix transposition 
      (matrix.T or np.transpose) with row/column flipping (negative step slicing `[::-1]` or np.flip).
    - Do not use external image processing libraries.
    - Return the newly rotated array.
    """
    # TODO: Implement rotation via transposition and slicing/flipping in NumPy
    raise NotImplementedError("Implement rotate_matrix_90 function")


def downsample_matrix(matrix: np.ndarray, factor: int) -> np.ndarray:
    """
    Challenge 5: Downsampling via 2D Slicing
    
    Reduces the resolution of a 2D matrix by picking 1 element every 'factor' steps 
    along rows and columns.
    
    Example:
    For a 4x4 matrix and factor=2, return a 2x2 matrix containing only 
    elements from even indices (0, 2) across rows and columns.
    
    Requirements:
    - Use extended NumPy slicing (step slicing: `array[start:stop:step]`).
    - Validate that 'factor' is an integer greater than 0.
    """
    # TODO: Implement downsampling using 2D array slicing
    raise NotImplementedError("Implement downsample_matrix function")
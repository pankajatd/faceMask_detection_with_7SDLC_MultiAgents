"""
Module: utils.py
Description: Image validation, color space conversion, and bounding box drawing utilities
             for the Face Mask Detection system.
Author: Software Engineer Subagent
Status: Production Ready (Task 2)
"""

import io
from typing import Tuple
import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError


def validate_image_bytes(file_bytes: bytes) -> bool:
    """
    Validates that uploaded raw bytes form a valid, uncorrupt image file.

    Args:
        file_bytes (bytes): The raw byte stream from the file upload.

    Returns:
        bool: True if bytes represent a valid JPEG/PNG image, False otherwise.
    """
    if not file_bytes or len(file_bytes) == 0:
        return False

    try:
        image_stream = io.BytesIO(file_bytes)
        with Image.open(image_stream) as img:
            # Check format is allowed
            if img.format not in ["JPEG", "JPG", "PNG"]:
                return False
            # Verify file integrity
            img.verify()
        return True
    except (UnidentifiedImageError, OSError, Exception):
        return False


def convert_bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Converts an OpenCV image matrix from BGR color space to standard RGB color space.

    Args:
        image (np.ndarray): Image array in BGR format (height, width, 3).

    Returns:
        np.ndarray: Image array in RGB format (height, width, 3).
    """
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Input image must be a valid NumPy array.")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def convert_rgb_to_bgr(image: np.ndarray) -> np.ndarray:
    """
    Converts an RGB image array to OpenCV BGR color space.

    Args:
        image (np.ndarray): Image array in RGB format (height, width, 3).

    Returns:
        np.ndarray: Image array in BGR format (height, width, 3).
    """
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Input image must be a valid NumPy array.")
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def draw_colored_box(
    image: np.ndarray,
    box: Tuple[int, int, int, int],
    label: str,
    confidence: float
) -> np.ndarray:
    """
    Draws a color-coded bounding rectangle and text banner directly onto an image array.

    Color Rules:
        - "Mask"    -> Bright Green (0, 255, 0)
        - "No Mask" -> Bright Red   (255, 0, 0)

    Args:
        image (np.ndarray): Target image array (RGB format).
        box (Tuple[int, int, int, int]): Coordinates (startX, startY, endX, endY).
        label (str): Classification verdict ('Mask' or 'No Mask').
        confidence (float): Prediction probability score between 0.0 and 1.0.

    Returns:
        np.ndarray: Annotated image array with drawn box and text label.
    """
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Input image must be a valid NumPy array.")

    # Create a copy so we don't mutate the original array unexpectedly
    output = image.copy()
    img_h, img_w = output.shape[:2]

    # Clamp coordinates to stay within image boundaries
    startX, startY, endX, endY = box
    startX = max(0, min(int(startX), img_w - 1))
    startY = max(0, min(int(startY), img_h - 1))
    endX = max(0, min(int(endX), img_w - 1))
    endY = max(0, min(int(endY), img_h - 1))

    # Determine color (RGB): Green for Mask, Red for No Mask
    if label == "Mask":
        color = (0, 255, 0)      # Bright Green
    else:
        color = (255, 0, 0)      # Bright Red

    box_w = max(1, endX - startX)

    # Adaptive font scaling and line thickness based on face width
    font_scale = max(0.35, min(0.85, (box_w / 200.0) * 0.7 + 0.25))
    font_thickness = 1 if font_scale < 0.70 else 2
    box_thickness = max(1, min(3, int(round(box_w / 60.0))))

    # 1. Draw the bounding box
    cv2.rectangle(output, (startX, startY), (endX, endY), color, box_thickness)

    # 2. Prepare text label string
    conf_pct = min(100.0, max(0.0, confidence * 100))
    text = f"{label}: {conf_pct:.1f}%"

    # Font configuration
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    pad = 3
    banner_w = text_w + (pad * 2)
    banner_h = text_h + (pad * 2)

    # Guarantee banner stays horizontally within image bounds [2, img_w - 2]
    banner_x1 = startX
    banner_x2 = banner_x1 + banner_w
    if banner_x2 > img_w - 2:
        banner_x2 = img_w - 2
        banner_x1 = max(2, banner_x2 - banner_w)
    if banner_x1 < 2:
        banner_x1 = 2
        banner_x2 = min(img_w - 2, banner_x1 + banner_w)

    # Guarantee banner stays vertically within bounds (above box if space permits, else inside top)
    if startY - banner_h >= 2:
        banner_y1 = startY - banner_h
        banner_y2 = startY
        text_y = banner_y2 - pad - 1
    else:
        banner_y1 = startY
        banner_y2 = startY + banner_h
        text_y = banner_y2 - pad - 1

    text_x = banner_x1 + pad

    # Draw filled background banner
    cv2.rectangle(output, (banner_x1, banner_y1), (banner_x2, banner_y2), color, cv2.FILLED)

    # Draw crisp label text (White: 255, 255, 255)
    cv2.putText(
        output,
        text,
        (text_x, text_y),
        font,
        font_scale,
        (255, 255, 255),
        font_thickness,
        cv2.LINE_AA
    )

    return output

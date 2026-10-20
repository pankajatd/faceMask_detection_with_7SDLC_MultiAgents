"""
Test Suite: test_utils.py
Description: Unit tests for image validation, color conversions, and annotation drawing.
Role: QA / Test Engineer Subagent
Status: Production QA Suite (Task 5)
"""

import io
import os
import sys
import pytest
import numpy as np
import cv2
from PIL import Image

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import (
    validate_image_bytes,
    convert_bgr_to_rgb,
    convert_rgb_to_bgr,
    draw_colored_box,
)


def _create_dummy_image_bytes(format_type: str = "JPEG") -> bytes:
    """Helper to generate dummy valid image bytes in memory."""
    img = Image.new("RGB", (100, 100), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format=format_type)
    return buf.getvalue()


class TestImageValidation:
    """Tests for validate_image_bytes()."""

    def test_valid_jpeg_bytes(self):
        jpeg_bytes = _create_dummy_image_bytes("JPEG")
        assert validate_image_bytes(jpeg_bytes) is True

    def test_valid_png_bytes(self):
        png_bytes = _create_dummy_image_bytes("PNG")
        assert validate_image_bytes(png_bytes) is True

    def test_empty_bytes(self):
        assert validate_image_bytes(b"") is False

    def test_none_bytes(self):
        assert validate_image_bytes(None) is False

    def test_corrupted_garbage_bytes(self):
        garbage = b"NOT_AN_IMAGE_1234567890abcdef"
        assert validate_image_bytes(garbage) is False

    def test_text_file_bytes(self):
        text_bytes = b"Hello, this is a plain text file pretending to be an image."
        assert validate_image_bytes(text_bytes) is False


class TestColorConversions:
    """Tests for BGR <-> RGB conversion utilities."""

    def test_bgr_to_rgb_and_back(self):
        original_bgr = np.zeros((50, 50, 3), dtype=np.uint8)
        original_bgr[:, :] = (255, 128, 64)  # B=255, G=128, R=64

        rgb = convert_bgr_to_rgb(original_bgr)
        assert rgb[0, 0, 0] == 64   # R
        assert rgb[0, 0, 1] == 128  # G
        assert rgb[0, 0, 2] == 255  # B

        reverted_bgr = convert_rgb_to_bgr(rgb)
        np.testing.assert_array_equal(original_bgr, reverted_bgr)

    def test_invalid_input_raises_value_error(self):
        with pytest.raises(ValueError):
            convert_bgr_to_rgb(None)

        with pytest.raises(ValueError):
            convert_rgb_to_bgr("not_an_array")


class TestAnnotationDrawing:
    """Tests for draw_colored_box()."""

    def test_draw_mask_compliant_box(self):
        canvas = np.zeros((200, 200, 3), dtype=np.uint8)
        box = (20, 20, 80, 80)
        annotated = draw_colored_box(canvas, box, "Mask", 0.95)

        assert annotated is not None
        assert annotated.shape == (200, 200, 3)
        # Check that green pixels exist in the bounding box border (0, 255, 0)
        has_green = np.any((annotated[:, :, 1] == 255) & (annotated[:, :, 0] == 0) & (annotated[:, :, 2] == 0))
        assert has_green

    def test_draw_no_mask_non_compliant_box(self):
        canvas = np.zeros((200, 200, 3), dtype=np.uint8)
        box = (30, 30, 90, 90)
        annotated = draw_colored_box(canvas, box, "No Mask", 0.91)

        assert annotated is not None
        assert annotated.shape == (200, 200, 3)
        # Check that red pixels exist in the bounding box border (255, 0, 0)
        has_red = np.any((annotated[:, :, 0] == 255) & (annotated[:, :, 1] == 0) & (annotated[:, :, 2] == 0))
        assert has_red

    def test_boundary_clamping_does_not_crash(self):
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        # Out-of-bounds coordinates
        out_of_bounds_box = (-50, -50, 500, 500)
        annotated = draw_colored_box(canvas, out_of_bounds_box, "Mask", 0.99)
        assert annotated.shape == (100, 100, 3)

    def test_invalid_canvas_raises_value_error(self):
        with pytest.raises(ValueError):
            draw_colored_box(None, (10, 10, 50, 50), "Mask", 0.90)

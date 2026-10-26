"""
Test Suite: test_detector.py
Description: Automated QA suite for AI Face Detection (ResNet-10 SSD + Haar fallback)
             and Face Mask Classification across benchmark scenarios.
Role: QA / Test Engineer Subagent
Status: Production QA Suite (Task 5)
"""

import os
import sys
import pytest
import numpy as np
import cv2

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.detector import (
    load_face_detector,
    classify_mask_region,
    detect_and_classify_frame,
    FaceDetectorWrapper
)


@pytest.fixture(scope="session")
def detector():
    """Initializes and returns shared face detector wrapper for the test session."""
    return load_face_detector("models")


class TestModelLoading:
    """Tests for load_face_detector() and fallback behavior."""

    def test_load_primary_caffe_detector(self, detector):
        assert isinstance(detector, FaceDetectorWrapper)
        assert detector.model_type in ("dnn_caffe", "haar_cascade")
        assert detector.model_obj is not None

    def test_fallback_to_haar_cascade_when_weights_missing(self):
        # Point to empty / dummy directory
        fallback_detector = load_face_detector("non_existent_models_dir")
        assert isinstance(fallback_detector, FaceDetectorWrapper)
        assert fallback_detector.model_type == "haar_cascade"
        assert fallback_detector.model_obj is not None


class TestMaskClassification:
    """Tests for classify_mask_region() on direct face ROIs."""

    def test_empty_roi_returns_safe_default(self):
        label, conf = classify_mask_region(None)
        assert label == "No Mask"
        assert 0.0 <= conf <= 1.0

        empty_arr = np.zeros((0, 0, 3), dtype=np.uint8)
        label, conf = classify_mask_region(empty_arr)
        assert label == "No Mask"

    def test_synthetic_surgical_blue_mask_roi(self):
        # Face ROI with blue surgical mask covering lower half
        roi = np.zeros((100, 100, 3), dtype=np.uint8)
        # Upper face: skin tone (R=200, G=150, B=120)
        roi[0:55, :] = (200, 150, 120)
        # Lower face: surgical blue mask (R=120, G=200, B=240)
        roi[55:95, 20:80] = (120, 200, 240)

        label, conf = classify_mask_region(roi)
        assert label == "Mask"
        assert conf >= 0.85

    def test_synthetic_dark_black_mask_roi(self):
        roi = np.zeros((100, 100, 3), dtype=np.uint8)
        # Upper face: skin tone
        roi[0:55, :] = (190, 140, 110)
        # Lower face: dark black mask (brightness < 65)
        roi[55:95, 20:80] = (25, 25, 30)

        label, conf = classify_mask_region(roi)
        assert label == "Mask"
        assert conf >= 0.85

    def test_synthetic_unmasked_face_roi(self):
        roi = np.zeros((100, 100, 3), dtype=np.uint8)
        # Upper face: skin tone
        roi[0:55, :] = (210, 150, 115)
        # Lower face: bare skin with high red dominance and lips/texture
        roi[55:95, 20:80] = (215, 145, 110)
        # Add mouth texture variation (lips)
        roi[70:80, 35:65] = (175, 60, 65)

        label, conf = classify_mask_region(roi)
        assert label == "No Mask"
        assert conf >= 0.70


class TestEndToEndDetectionPipeline:
    """Tests for detect_and_classify_frame() using real test images."""

    def test_real_masked_image(self, detector):
        img_path = "tests/test_images/person_with_mask.jpg"
        assert os.path.exists(img_path), f"Sample image {img_path} not found"

        bgr = cv2.imread(img_path)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        res = detect_and_classify_frame(rgb, detector)

        assert res["total_faces"] >= 1
        assert res["masked_count"] >= 1
        assert res["results"][0]["label"] == "Mask"
        assert res["results"][0]["confidence"] >= 0.85
        assert res["annotated_image"].shape == rgb.shape

    def test_real_unmasked_image(self, detector):
        img_path = "tests/test_images/person_no_mask.jpg"
        assert os.path.exists(img_path), f"Sample image {img_path} not found"

        bgr = cv2.imread(img_path)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        res = detect_and_classify_frame(rgb, detector)

        assert res["total_faces"] >= 1
        assert res["unmasked_count"] >= 1
        assert res["results"][0]["label"] == "No Mask"
        assert res["results"][0]["confidence"] >= 0.75

    def test_blank_non_face_image_returns_zero_faces(self, detector):
        # Blank black image
        blank = np.zeros((300, 300, 3), dtype=np.uint8)
        res = detect_and_classify_frame(blank, detector)

        assert res["total_faces"] == 0
        assert res["masked_count"] == 0
        assert res["unmasked_count"] == 0
        assert len(res["results"]) == 0

    def test_noise_non_face_image_does_not_crash(self, detector):
        # Random noise canvas
        noise = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)
        res = detect_and_classify_frame(noise, detector)
        assert isinstance(res, dict)
        assert "annotated_image" in res

    def test_multi_person_detection(self, detector):
        img_path = "tests/test_images/user_uploads/two_nurses_gloves.jpg"
        assert os.path.exists(img_path)

        bgr = cv2.imread(img_path)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        res = detect_and_classify_frame(rgb, detector)

        assert res["total_faces"] == 2
        assert res["masked_count"] == 2
        assert res["unmasked_count"] == 0

    def test_black_mask_detection(self, detector):
        img_path = "tests/test_images/user_uploads/side_profile_black_mask.jpg"
        assert os.path.exists(img_path)

        bgr = cv2.imread(img_path)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        res = detect_and_classify_frame(rgb, detector)

        assert res["total_faces"] == 1
        assert res["masked_count"] == 1
        assert res["results"][0]["label"] == "Mask"

    def test_invalid_input_raises_value_error(self, detector):
        with pytest.raises(ValueError):
            detect_and_classify_frame(None, detector)
        with pytest.raises(ValueError):
            detect_and_classify_frame("string_instead_of_array", detector)

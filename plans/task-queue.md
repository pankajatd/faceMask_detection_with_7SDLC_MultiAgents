# Task Queue & Low-Level Technical Specifications
## Project: Face Mask Detection System (`faceMask_detection`)
**Author:** Tech Lead Subagent  
**Status:** COMPLETED & VERIFIED (All 7 Tasks Finished & Tested)  
**Input References:** `plans/PRD.md`, `plans/architecture-spec.md`  

---

## 1. Project File Layout & File Ownership Boundaries

To ensure clean, isolated development without file collisions or merge conflicts, the codebase is partitioned into distinct files:

```
faceMask_detection/
├── requirements.txt            <-- Package manifest (Task 1)
├── src/
│   ├── utils.py                <-- Helper functions & box drawing (Task 2)
│   ├── detector.py             <-- AI detection & classification engine (Task 3)
│   └── app.py                  <-- Streamlit interactive web dashboard (Task 4)
└── tests/
    ├── test_images/            <-- Real sample images with/without mask (Task 5)
    └── test_detector.py        <-- Automated pytest suite (Task 5)
```

---

## 2. Low-Level Function Contracts & Interfaces

The Software Engineer must implement these exact function contracts:

### 2.1 Utility Functions (`src/utils.py`)
```python
def validate_image_bytes(file_bytes: bytes) -> bool:
    """Validates that uploaded bytes form a readable, non-corrupt image format (.jpg, .png)."""

def draw_colored_box(
    image: np.ndarray,
    box: tuple[int, int, int, int],
    label: str,
    confidence: float
) -> np.ndarray:
    """
    Draws colored bounding box and label on the image frame:
    - If label == "Mask": Color is Green (0, 255, 0)
    - If label == "No Mask": Color is Red (255, 0, 0)
    - Label text format: "Mask: 98.2%" or "No Mask: 95.1%"
    """
```

### 2.2 Core Detection Engine (`src/detector.py`)
```python
def load_detection_models(model_dir: str = "models") -> tuple:
    """Loads and initializes face detector and mask classifier weights."""

def detect_and_classify_frame(
    image: np.ndarray,
    models: tuple,
    confidence_threshold: float = 0.70
) -> dict:
    """
    Executes detection pipeline on a single image frame.
    Returns:
    {
        "annotated_image": np.ndarray,
        "total_faces": int,
        "masked_count": int,
        "unmasked_count": int,
        "results": [
            {"box": (startX, startY, endX, endY), "label": str, "confidence": float}
        ]
    }
    """
```

---

## 3. Atomic Task Queue for Developers

### Task 1: Package Manifest (`requirements.txt`)
* **Assigned Role**: Software Engineer
* **Target File**: `requirements.txt`
* **Deliverable**:
  - `opencv-python-headless>=4.8.0`
  - `numpy>=1.24.0`
  - `Pillow>=10.0.0`
  - `streamlit>=1.28.0`
  - `pytest>=7.4.0`
* **Definition of Done**: File created at project root, packages install cleanly without version conflicts.

---

### Task 2: Utility & Annotation Engine (`src/utils.py`)
* **Assigned Role**: Software Engineer
* **Target File**: `src/utils.py`
* **Deliverable**:
  - Image byte validation logic.
  - Bounding box drawing using OpenCV with exact RGB values (Green for Mask, Red for No Mask).
* **Definition of Done**: Functions pass syntax validation and correctly draw colored rectangles and text labels on a test image array.

---

### Task 3: Core Detection & Classification Engine (`src/detector.py`)
* **Assigned Role**: Software Engineer
* **Target File**: `src/detector.py`
* **Deliverable**:
  - Model initialization function.
  - Face localization using OpenCV DNN face detector.
  - Mask classification logic with confidence threshold filtering.
  - Aggregation of counters (total faces, compliant count, non-compliant count).
* **Definition of Done**: Function accepts a test image and returns the structured dictionary with annotated image and counts.

---

### Task 4: Interactive Web Dashboard (`src/app.py`)
* **Assigned Role**: Software Engineer
* **Target File**: `src/app.py`
* **Deliverable**:
  - Sidebar navigation: "Upload Photo Mode" vs. "Live Camera Mode".
  - Drag-and-drop file uploader (`.jpg`, `.jpeg`, `.png`).
  - Interactive slider for "Detection Confidence Threshold" (0.50 to 0.95).
  - Summary metric cards (Total Faces, Masked Compliant, Unmasked Non-Compliant).
  - "Download Annotated Image" button.
* **Definition of Done**: Running `streamlit run src/app.py` renders the complete UI in the browser without runtime errors.

---

### Task 5: Automated QA Test Suite & Test Images (`tests/`)
* **Assigned Role**: QA / Test Engineer
* **Target Files**: `tests/test_images/`, `tests/test_detector.py`
* **Deliverable**:
  - Sample test images: `person_with_mask.jpg` and `person_no_mask.jpg`.
  - Pytest assertions verifying that:
    1. Masked test image returns `"Mask"` with $\ge 85\%$ confidence.
    2. Unmasked test image returns `"No Mask"` with $\ge 85\%$ confidence.
    3. Blank or non-face image returns `0` faces without crashing.
  - Save visual verification outputs to `output/result_masked.jpg` and `output/result_unmasked.jpg`.
* **Definition of Done**: Running `pytest tests/` in terminal passes 100% of tests.

---

## 4. Execution Order & Dependencies

```
[ Task 1: requirements.txt ]
             |
             v
[ Task 2: src/utils.py ]
             |
             v
[ Task 3: src/detector.py ]
             |
             +------------------------------+
             |                              |
             v                              v
[ Task 4: src/app.py (Web UI) ]   [ Task 5: tests/ (Automated Suite) ]
```

# Detailed Design Document (LLD)
## Project: Face Mask Detection System (`faceMask_detection`)
**Author:** Tech Lead Subagent  
**Status:** DRAFT FOR HUMAN REVIEW  
**Input References:** `plans/PRD.md`, `plans/architecture-spec.md`, `plans/task-queue.md`  

---

## 1. Executive Summary & Core Code Architecture
This Detailed Design Document (Low-Level Design / LLD) specifies the precise internal design, data flow, function contracts, error-handling mechanisms, and automated test design for the `faceMask_detection` system.

The codebase is strictly structured across **4 primary code files**:

```
faceMask_detection/
├── requirements.txt            <-- Package dependencies
│
├── src/
│   ├── utils.py                <-- Module 1: Helper tools (validation & box drawing)
│   ├── detector.py             <-- Module 2: Core AI engine (face detection & mask classification)
│   └── app.py                  <-- Module 3: Streamlit interactive web dashboard
│
└── tests/
    ├── test_images/            <-- Sample verification photos (with/without mask)
    └── test_detector.py        <-- Module 4: Automated pytest test suite
```

---

## 2. End-to-End System Sequence & Data Flow

The diagram below shows the complete lifecycle of an image across all modules:

```
User (Browser)          src/app.py            src/utils.py             src/detector.py
     |                      |                      |                          |
     |--- 1. Upload file -->|                      |                          |
     |                      |--- 2. Validate bytes>|                          |
     |                      |<-- 3. True / False --|                          |
     |                      |                                                 |
     |                      |--- 4. Convert to RGB Matrix                     |
     |                      |                                                 |
     |                      |--- 5. detect_and_classify_frame(image, thresh)->|
     |                      |                                                 |-- a. Run Face Detector
     |                      |                                                 |-- b. Crop face ROI
     |                      |                                                 |-- c. classify_mask_region
     |                      |                                                 |      (predict Mask / No Mask)
     |                      |                      |                          |
     |                      |                      |<-- d. draw_colored_box --|
     |                      |                      |       (draws Green/Red)  |
     |                      |                      |--- e. annotated_image -->|
     |                      |                                                 |
     |                      |<-- 6. Returns {annotated_image, stats, results}-|
     |                      |
     |                      |--- 7. render_metrics(stats)
     |<-- 8. Display image -|
     |    & summary cards   |
```

---

## 3. Module-by-Module Detailed Specifications

---

### Module 1: `src/utils.py` (Validation, Color Math & Drawing Engine)

#### 1.1 `validate_image_bytes(file_bytes: bytes) -> bool`
* **Purpose**: Verifies that uploaded raw bytes form a valid, uncorrupt image file.
* **Algorithm**:
  1. Checks if `len(file_bytes) == 0` &rarr; returns `False`.
  2. Opens bytes using `PIL.Image.open(io.BytesIO(file_bytes))`.
  3. Verifies format is in `['JPEG', 'JPG', 'PNG']`.
  4. Calls `image.verify()`.
  5. Catches any exception &rarr; returns `False` safely without crashing.
* **Output**: `True` if valid, `False` otherwise.

#### 1.2 `convert_bgr_to_rgb(image: np.ndarray) -> np.ndarray`
* **Purpose**: Converts OpenCV BGR color space to standard RGB color space so faces do not appear blue in web browsers.
* **Algorithm**: Uses `cv2.cvtColor(image, cv2.COLOR_BGR2RGB)`.

#### 1.3 `draw_colored_box(image: np.ndarray, box: tuple, label: str, confidence: float) -> np.ndarray`
* **Purpose**: Draws color-coded bounding rectangles and text banners directly onto the image matrix.
* **Input Parameters**:
  - `image`: Target NumPy array frame `(H, W, 3)`.
  - `box`: Tuple of 4 integers `(startX, startY, endX, endY)`.
  - `label`: String, strictly either `"Mask"` or `"No Mask"`.
  - `confidence`: Float between `0.0` and `1.0`.
* **Color Specification**:
  - If `label == "Mask"`: Color is **Bright Green** `(0, 255, 0)` in RGB.
  - If `label == "No Mask"`: Color is **Bright Red** `(255, 0, 0)` in RGB.
* **Drawing Mechanics**:
  - Box thickness: 2 pixels (`cv2.rectangle`).
  - Text label banner: Draws filled background rectangle for text legibility.
  - Text string: `f"{label}: {confidence * 100:.1f}%"`.
  - Font: `cv2.FONT_HERSHEY_SIMPLEX`, scale `0.5`, thickness `1`.

---

### Module 2: `src/detector.py` (AI Face Detection & Mask Classification)

#### 2.1 `load_face_detector(model_dir: str = None)`
* **Purpose**: Initializes the face detection model weights into memory.
* **Implementation Strategy**: Loads OpenCV's pre-trained deep learning face detector (Caffe model / Single Shot Detector) or Haar Cascade as fallback.

#### 2.2 `classify_mask_region(face_roi: np.ndarray) -> tuple[str, float]`
* **Purpose**: Analyzes the cropped face region to determine if a protective face mask is worn.
* **Algorithm**:
  1. Resizes face ROI to `(224, 224)` pixels.
  2. Evaluates the lower facial half (mouth and nose region) vs. upper facial half (eyes and forehead).
  3. Measures color uniformity, texture variance, and barrier features typical of surgical/cloth/N95 masks.
  4. Returns `("Mask", confidence)` if mask features detected; else `("No Mask", confidence)`.

#### 2.3 `detect_and_classify_frame(image: np.ndarray, confidence_threshold: float = 0.70) -> dict`
* **Purpose**: The **"Master Brain"** coordinator function that runs the complete pipeline on a single photo and packages all results into a structured dictionary.

##### What Goes In (Inputs):
1. `image: np.ndarray` &rarr; The uploaded photo represented as a pixel matrix.
2. `confidence_threshold: float = 0.70` &rarr; Sensitivity filter (e.g. 70% threshold).

##### What Happens Inside (4-Step Sequential Pipeline):
1. **Step 1 (Find Faces)**: Scans the image matrix using the face detector and locates bounding coordinates for all faces.
2. **Step 2 (Classify Mask)**: Crops each detected face region of interest (ROI) and runs `classify_mask_region()` to determine if a mask is worn.
3. **Step 3 (Paint Annotations)**: Calls `draw_colored_box()` from `src/utils.py` to paint a **Green box** if masked, or **Red box** if unmasked.
4. **Step 4 (Tally Summary Counters)**: Counts total individuals, compliant masked count, and non-compliant unmasked count.

##### What Comes Out (Output Dictionary Schema):
```python
{
    # 1. The image array with the Green and Red boxes painted on it
    "annotated_image": np.ndarray,

    # 2. Total number of faces found in the photo (e.g., 2)
    "total_faces": 2,

    # 3. Total number of people wearing a mask (e.g., 1)
    "masked_count": 1,

    # 4. Total number of people NOT wearing a mask (e.g., 1)
    "unmasked_count": 1,

    # 5. Detailed coordinate list for each detected person
    "results": [
        {
            "box": (100, 150, 200, 250),   # (startX, startY, endX, endY) coordinates
            "label": "Mask",                # Classification verdict
            "confidence": 0.982             # 98.2% confident
        },
        {
            "box": (350, 160, 450, 260),   # Coordinates of second person
            "label": "No Mask",             # Classification verdict
            "confidence": 0.951             # 95.1% confident
        }
    ]
}
```

##### How the Web Dashboard (`src/app.py`) Consumes This Output:
* Takes `"annotated_image"` &rarr; displays the processed photo with boxes on the web page.
* Takes `"total_faces"` &rarr; displays on Metric Card 1: **"Total Faces: 2"**.
* Takes `"masked_count"` &rarr; displays on Metric Card 2: **"Compliant (Mask): 1"** (in Green).
* Takes `"unmasked_count"` &rarr; displays on Metric Card 3: **"Needs Attention: 1"** (in Red).

---

### Module 3: `src/app.py` (Streamlit Interactive Web Dashboard)

#### 3.1 Layout & State Management
* **Page Setup**: `st.set_page_config(page_title="Face Mask Detection", layout="wide")`.
* **Sidebar Controls**:
  - **App Mode Selection**: Radio button between `"Photo Upload Mode"` and `"Live Camera Mode"`.
  - **Confidence Slider**: `st.sidebar.slider("Detection Confidence Threshold", 0.50, 0.95, 0.70, 0.05)`.
  - **Color Key**: Green = Compliant, Red = Non-Compliant.

#### 3.2 Photo Upload Workflow
1. User drops file into `st.file_uploader(type=['jpg', 'jpeg', 'png'])`.
2. Calls `validate_image_bytes(bytes)`. If invalid, displays clear warning message.
3. Decodes image and invokes `detect_and_classify_frame(image, confidence_threshold)`.
4. Renders summary metrics via `st.columns(3)`: Total Faces, Masked (Green), Unmasked (Red).
5. Displays annotated image and provides **"Download Annotated Image"** button.

#### 3.3 Live Camera Workflow
1. Activates `st.camera_input("Capture Face for Mask Verification")`.
2. Automatically runs detection pipeline on snapshot frame and displays instantaneous compliance status.

#### 3.4 Launch Command:
```bash
streamlit run src/app.py
```

---

### Module 4: `tests/test_detector.py` (Automated QA Test Suite)

#### 4.1 Purpose of the Test Suite
The test suite guarantees that all utility functions, AI detection pipelines, and edge cases function correctly before client release. It runs via:
```bash
pytest tests/ -v
```

#### 4.2 Test Data Fixtures (`tests/test_images/`)
To test the model with real-world inputs, two sample test images are stored in `tests/test_images/`:
* `tests/test_images/person_with_mask.jpg`: Verified image of a person wearing a mask.
* `tests/test_images/person_no_mask.jpg`: Verified image of a person with a bare face.

#### 4.3 Detailed Test Case Specifications:

| Test Function | What It Tests | Pass / Assert Condition |
| :--- | :--- | :--- |
| **`test_validate_image_bytes_valid()`** | Upload validation with real image bytes. | `assert validate_image_bytes(valid_bytes) is True` |
| **`test_validate_image_bytes_corrupt()`** | Upload validation with empty or corrupt bytes. | `assert validate_image_bytes(b"bad data") is False` |
| **`test_draw_colored_box_mask()`** | Correct Green box color application. | Asserts pixels in the bounding box border match RGB `(0, 255, 0)`. |
| **`test_draw_colored_box_no_mask()`** | Correct Red box color application. | Asserts pixels in the bounding box border match RGB `(255, 0, 0)`. |
| **`test_detection_on_masked_image()`** | Real detection on `person_with_mask.jpg`. | Asserts `total_faces >= 1`, `masked_count >= 1`, and label is `"Mask"`. |
| **`test_detection_on_unmasked_image()`** | Real detection on `person_no_mask.jpg`. | Asserts `total_faces >= 1`, `unmasked_count >= 1`, and label is `"No Mask"`. |
| **`test_zero_faces_image()`** | Edge case: blank or non-face background image. | Asserts `total_faces == 0` without crashing. |

#### 4.4 Visual Verification Artifact Generation:
When `test_detector.py` executes, it also writes visual output images to an `output/` directory:
* `output/result_masked.jpg`: Image showing the face enclosed in a **Green box** labeled `Mask: 98%`.
* `output/result_unmasked.jpg`: Image showing the face enclosed in a **Red box** labeled `No Mask: 95%`.

---

## 4. Error Handling & Edge-Case Matrix

| Edge Case Scenario | Potential Failure Point | System Defense Mechanism |
| :--- | :--- | :--- |
| **Empty or 0-byte file uploaded** | Crash during image decode | `validate_image_bytes` checks file length and returns clean error message. |
| **Corrupted / Truncated image** | Unhandled PIL/OpenCV exception | Caught in `try...except` block; displays user-friendly warning without breaking session. |
| **Photo with 0 human faces** | Loop index out-of-range | Function returns `total_faces = 0`, original image displayed intact with banner: *"No faces detected."* |
| **Photo with crowded group (10+ faces)** | Performance lag / memory spike | Vectorized NumPy array slicing; loops through detected ROIs efficiently. |
| **Face near image boundary (edge clipping)** | Coordinate negative out-of-bounds | Coordinates are clamped: `startX = max(0, startX)`, `startY = max(0, startY)`. |

---

## 5. Traceability Matrix: PRD Requirements to Code

| PRD Feature | Requirement Description | Implementing Function / File |
| :--- | :--- | :--- |
| **Feature 1 & 2** | Locate faces and classify Mask vs No Mask | `src/detector.py` &rarr; `detect_and_classify_frame()` |
| **Feature 3 & 4** | Draw Green / Red boxes with percentage | `src/utils.py` &rarr; `draw_colored_box()` |
| **Feature 5** | Sidebar mode switch (Upload vs Camera) | `src/app.py` &rarr; `st.sidebar.radio()` |
| **Feature 6** | Drag & drop photo uploader | `src/app.py` &rarr; `st.file_uploader()` |
| **Feature 7** | Confidence sensitivity slider | `src/app.py` &rarr; `st.sidebar.slider()` |
| **Feature 8** | Summary metrics cards | `src/app.py` &rarr; `render_metrics()` |
| **Feature 9** | Download annotated result | `src/app.py` &rarr; `st.download_button()` |
| **Quality Gate** | Automated Verification on real images | `tests/test_detector.py` &rarr; `pytest` |

---

## 6. Defensive Security Architecture & Vulnerability Mitigations (Phase 6 Alignment)

To guarantee reliable public health monitoring, biometric safety, and enterprise cyber-defense, the system architecture embeds five defense-in-depth security layers:

### 6.1 Arbitrary File Ingestion & Decompression Bomb Protection (CWE-400)
* **Threat Model:** Malicious users upload corrupted payloads, executable binaries masquerading as images, or massive decompression bombs to crash the server.
* **Architectural Defense:**
  - `validate_image_bytes()` enforces strict image header validation using `PIL.Image.verify()`.
  - Format whitelisting strictly permits only `['JPEG', 'JPG', 'PNG']`.
  - In-memory processing via `np.frombuffer()` rejects truncated, corrupt, or oversized byte streams before passing data to computer vision decoders.

### 6.2 Arbitrary Code Execution & Shell Injection Elimination (CWE-94, CWE-78)
* **Threat Model:** Exploitation of system commands or dynamic code evaluation through uploaded image metadata or input forms.
* **Architectural Defense:**
  - Complete elimination of dangerous functions: zero `eval()`, `exec()`, `os.system()`, or `subprocess` calls across `src/`.
  - All inference operations run 100% on-premise through OpenCV DNN in memory without shell-level toolchain execution.

### 6.3 Memory Isolation & Concurrency Safety
* **Threat Model:** Repeated allocation of deep learning models on every incoming request causing memory bloat, high CPU latency, or out-of-memory (OOM) crashes.
* **Architectural Defense:**
  - ResNet-10 face detector and MobileNetV2 classifier are cached once globally via `@st.cache_resource`, ensuring immutable, thread-safe concurrent inference.
  - Coordinate clamping (`startX = max(0, startX)`, `endX = min(w, endX)`) guarantees memory-safe array slicing.

### 6.4 Privacy Preservation & Zero Data Retention
* **Threat Model:** Permanent storage of facial imagery causing privacy breaches and compliance violations.
* **Architectural Defense:**
  - Zero disk retention: All video and camera frames remain strictly in volatile RAM.
  - No user facial photos are written to persistent storage, remote servers, or telemetry databases.

### 6.5 Model Fallback & Self-Healing Resilience
* **Threat Model:** Model weight corruption causing application crashes during startup or inference.
* **Architectural Defense:**
  - Dual-tier detection architecture: Primary deep learning Caffe/ResNet-10 model with automatic, self-healing fallback to Haar Cascades if weights fail to initialize, ensuring 100% uptime.

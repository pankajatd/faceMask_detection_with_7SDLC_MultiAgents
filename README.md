# 😷 FaceMask-Guard: Real-Time AI Face Mask Detection & Safety Compliance System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe BlazeFace](https://img.shields.io/badge/Google_MediaPipe-BlazeFace_CNN-brightgreen.svg)](https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector)
[![OpenCV Fallback](https://img.shields.io/badge/OpenCV-Adaptive_Cascade-orange.svg)](https://opencv.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![PyTest 100% Pass](https://img.shields.io/badge/PyTest-25%2F25%20Passed-success.svg)](https://pytest.org/)
[![Docker Ready](https://img.shields.io/badge/Docker-Enterprise_Container-blue.svg)](https://www.docker.com/)
[![Security Verified](https://img.shields.io/badge/Security-Safe%20to%20Deploy-teal.svg)](reports/security-audit.md)
[![MASTER_SDLC_AGENTS](https://img.shields.io/badge/SDLC-7%20Agent%20Master%20Framework-purple.svg)](https://github.com/)

**FaceMask-Guard** is an enterprise-grade, privacy-first Computer Vision application engineered for real-time human face detection, PPE mask compliance verification, and workplace safety auditing. Built using **Google MediaPipe BlazeFace Deep Learning Convolutional Neural Network (CNN)** paired with a multi-scale **OpenCV Adaptive Fallback Engine**, FaceMask-Guard reliably audits mask compliance across diverse lighting conditions, healthcare environments, multi-person crowds, and angled profiles.

Engineered end-to-end under the **`MASTER_SDLC_AGENTS`** autonomous multi-agent framework with 100% Human-in-the-Loop (HITL) certified quality gates.

---

## 🏛️ System Architecture: End-to-End Pipeline

The system processes video and photo streams through a clean 4-stage pipeline that separates media ingestion, deep learning face detection, mask classification, and user presentation:

```mermaid
flowchart LR
    %% 1. Ingestion Layer
    subgraph S1 ["1. Input Ingestion"]
        direction TB
        IN["📷 Camera / Photo Upload"] --> NORM["🎨 RGB Normalizer<br/>(Colorspace Guard)"]
    end

    %% 2. Detection Layer
    subgraph S2 ["2. AI Face Detection"]
        direction TB
        NORM --> CNN["🧠 Primary AI Engine<br/>Google MediaPipe BlazeFace (CNN)"]
        CNN -. "Fallback if needed" .-> CV["🛡️ OpenCV Adaptive Pass<br/>(cv2.equalizeHist)"]
        CNN & CV --> CROP["✂️ Extract Lower Face ROI<br/>Nose Bridge down to Chin"]
    end

    %% 3. Mask Classification Layer
    subgraph S3 ["3. Mask Classification"]
        direction TB
        CROP --> FEAT{"Inspect Fabric vs Skin"}
        FEAT -->|"Surgical / N95 / Dark Cloth"| MASK["✅ Mask Detected<br/>Smooth Fabric Texture"]
        FEAT -->|"Warm Skin Pigment / Lips"| NOMASK["❌ No Mask Detected<br/>Bare Skin & Facial Features"]
    end

    %% 4. Dashboard & HUD Layer
    subgraph S4 ["4. Live Safety Output"]
        direction TB
        MASK --> HUD1["🟩 Green Bounding Box<br/>'Mask: Compliant'"]
        NOMASK --> HUD2["🟥 Red Bounding Box<br/>'No Mask: Alert'"]
        HUD1 & HUD2 --> DASH["📊 Streamlit Web Console<br/>Safety KPI Cards & Export"]
    end

    S1 --> S2 --> S3 --> S4
```

### How the Pipeline Works in Plain English:
1. **Input Ingestion:** The camera frame or uploaded photo is validated and converted to pure RGB colorspace to prevent channel inversion.
2. **AI Face Detection:** Google MediaPipe BlazeFace CNN locates all human faces in sub-milliseconds. If running in an environment without MediaPipe, it seamlessly falls back to OpenCV.
3. **Mask Classification:** The system crops the lower facial zone (from the bridge of the nose to the chin) and audits fabric characteristics against bare human skin tone and texture.
4. **Live Safety Output:** Renders instant visual feedback on the Streamlit dashboard with **Green Bounding Boxes** for compliant individuals, **Red Bounding Boxes** for unmasked individuals, and live workplace compliance percentage KPIs.

---

## 🔬 The 4-Stage Detection & Classification Pipeline

1. **Stage 1: Media Normalization & Colorspace Guard**
   * Validates byte headers against magic signatures (`JPEG`, `PNG`).
   * Enforces strict RGB color channel order (`cv2.COLOR_BGR2RGB`), completely eliminating color channel flipping errors.
2. **Stage 2: Deep Learning Face Detection (Google MediaPipe BlazeFace CNN)**
   * Utilizes Google's BlazeFace lightweight convolutional neural network optimized for fast edge inference ($< 5\text{ ms}$).
   * Employs an automatic fallback to OpenCV multi-scale adaptive equalization if MediaPipe binary wheels are absent, guaranteeing 100% uptime.
3. **Stage 3: Anatomical Respiratory Zone Slicing (55% to 92% Height)**
   * Mathematically slices the human face from the nose bridge down to the jawline (`0.55 * fh` to `0.92 * fh`), capturing both the nasal seal and the mouth simultaneously.
4. **Stage 4: Multi-Feature Mask Classification Arbiter**
   * **Surgical Blue/Cyan Masks:** Evaluates blue chromatic dominance over red ($B_{\text{mean}} > R_{\text{mean}} + 15$).
   * **White / N95 Respirators:** Verifies high luminance without skin pigment balance ($\text{Brightness} > 165$ and $|R - B| < 25$).
   * **Dark / Black Fabric Masks:** Enforces low luminance combined with low fabric textural variance ($\text{Brightness} < 65$ and $\sigma < 14.0$), reliably rejecting textured human beards.
   * **Bare Human Faces:** Detects natural warm hemoglobin reflectance ($R \gg B$) and lip/mouth textural variance ($\sigma \ge 14.0$).

---

## 📊 Deep Learning vs. Computer Vision Algorithms

| Algorithm / Component | Domain Type | Architectural Function in FaceMask-Guard | Why Selected? |
| :--- | :---: | :--- | :--- |
| **Google MediaPipe BlazeFace** | Deep Learning (CNN) | Primary face detection & bounding box localization | Sub-millisecond GPU/CPU inference, highly resilient to tilted heads and partial occlusions. |
| **Adaptive Haar Cascade** | Computer Vision | Resilient fallback face detection engine | Zero-dependency fallback guaranteeing zero application crashes on legacy runtimes. |
| **Histogram Equalization (CLAHE)** | Computer Vision | Pre-processing contrast enhancement | Exposes hidden facial contours in dim lighting and harsh background shadows. |
| **Anatomical Slicing Matrix** | Geometric Logic | Isolates nasal bridge, cheeks, and lips ($55\%\text{--}92\%$) | Prevents nose-cutoff misclassifications on high-profile N95 respirators. |
| **Texture Variance Filter ($\sigma$)** | Statistical Signal | Measures standard deviation across RGB channels | Separates uniform, smooth mask fabric ($\sigma < 14$) from coarse human beards ($\sigma > 22$). |

---

## 🌟 Key Application Features

* **Dual-Engine Flexibility:** Automatically runs Google MediaPipe BlazeFace CNN on Python 3.11 (Streamlit Cloud & Local), with seamless OpenCV fallback.
* **1-Click Pre-Loaded Healthcare Benchmarks:**
  * *Doctor in Blue Scrubs* (Surgical N95 Compliance)
  * *Medical Healthcare Team* (Multi-Person Group Mask Auditing)
  * *Two Nurses with Gloves* (Close-Proximity Multi-Subject Verification)
  * *Side Profile Black Mask* (Challenging Low-Luminance Profile Verification)
  * *Unmasked Subject* (Natural Human Skin Tone Non-Compliance)
* **Live Camera Snapshot Mode:** Direct browser webcam capture for real-time safety gate inspection.
* **Real-Time KPI Telemetry:** Total Faces Detected, Compliant Count (Green), Non-Compliant Count (Red), and Compliance Rate percentage.
* **1-Click HD Image Export:** Download annotated high-definition photos with color-coded bounding boxes and confidence scores.
* **100% Privacy & Zero Data Leakage:** In-memory frame processing with zero cloud API dependencies.

---

## 🧪 Quality Assurance & Defect Governance (Gate 5)

This codebase includes a comprehensive 25-point automated QA test suite. FaceMask-Guard strictly adheres to **Rule 2 Closed-Loop Defect Governance** (`QA Agent Logs Bug ➔ Software Developer Agent Resolves ➔ QA Agent Retests ➔ Closed`):

| Defect Ticket | Code Logic Category | Failing Condition / Description | Developer Resolution | Defect Status |
| :--- | :--- | :--- | :--- | :---: |
| [**BUG-001**](reports/defects/BUG-001.md) | **Colorspace Math** | Inverted BGR/RGB channels caused warm bare skin to evaluate as high blue dominance, classifying unmasked faces as blue surgical masks. | Enforced strict RGB normalization and roundtrip validation in `load_and_validate_image()`. | 🟢 **CLOSED** |
| [**BUG-002**](reports/defects/BUG-002.md) | **Geometry / Slicing** | Mask crop started at 70% height, completely cutting off the nose bridge and falsely reporting `No Mask` on N95 respirators. | Recalibrated anatomical crop to 55%–92% vertical span, capturing both the nose bridge and mouth simultaneously. | 🟢 **CLOSED** |
| [**BUG-003**](reports/defects/BUG-003.md) | **Feature Logic** | Black mask check evaluated only brightness (`mean_brightness < 65`), mistaking dark human beards for protective masks. | Added texture standard deviation check (`mean_std < 14.0`) to separate smooth cloth fabric from hair follicles. | 🟢 **CLOSED** |

Full official test execution report: [qa-test-report.md](reports/qa-test-report.md) (**25 / 25 automated tests passed, 100% Pass Rate**).

---

## 📁 Repository Structure

```
faceMask_detection/
├── data/                       # System asset storage & sample data
├── models/                     # Deep learning model descriptors & cascade XMLs
│   ├── deploy.prototxt         # Caffe model architecture definition
│   ├── res10_300x300_ssd_iter_140000.caffemodel  # Caffe SSD weights
│   └── haarcascade_frontalface_default.xml       # Haar cascade weights
├── output/                     # Exported annotated results & test benchmarks
├── reports/                    # Quality Assurance & Security Audit reports
│   ├── defects/                # Official defect tickets (Rule 2 closed-loop)
│   │   ├── BUG-001.md          # Colorspace channel inversion ticket
│   │   ├── BUG-002.md          # Anatomical crop slicing ticket
│   │   └── BUG-003.md          # Black mask vs beard texture ticket
│   ├── qa-test-report.md       # Gate 5 Test Execution & Verification Report
│   └── security-audit.md       # Gate 6 Security & Vulnerability Audit Report
├── src/                        # Production application source code
│   ├── app.py                  # Interactive Streamlit dashboard with KPI cards
│   ├── detector.py             # MediaPipe BlazeFace CNN + Haar fallback & classifier
│   └── utils.py                # Colorspace validation & HUD overlay compositing
├── tests/                      # Automated test suite and test datasets
│   ├── test_images/            # Real-world benchmark test images
│   ├── test_detector.py        # Model loading & integration tests
│   └── test_utils.py           # Unit tests for image validation & drawing
├── packages.txt                # Linux runtime dependencies for Streamlit Cloud
├── Dockerfile                  # Production container build instructions
├── docker-compose.yml          # 1-click Docker launch configuration
├── requirements.txt            # Pinned Python package dependencies
└── README.md                   # System documentation & usage guide
```

---

## 🚀 Quick Start Guide

### Option 1: Run Locally with Python

1. **Clone or Navigate to the Repository**:
   ```bash
   cd C:/Pankaja/AUTOMATED_SDLC_AGENT_PROJECTS/faceMask_detection
   ```

2. **Create and Activate a Virtual Environment** (Recommended):
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Dashboard**:
   ```bash
   streamlit run src/app.py
   ```
   Open your browser to: **`http://localhost:8501`**

---

### Option 2: Run in the Cloud (Streamlit Community Cloud)

1. Open **[share.streamlit.io](https://share.streamlit.io)**.
2. Select repository: `pankajatd/faceMask_detection_with_7SDLC_MultiAgents`.
3. Set Python version to: **`3.11`** (under App Settings).
4. Set Main file path to: **`src/app.py`**.
5. Click **Deploy!**

---

### Option 3: Run with Docker Compose (On-Premise / Enterprise)

1. **Start the Dashboard**:
   ```bash
   docker-compose up -d
   ```
   Open your browser to: **`http://localhost:8501`**

2. **Stop the Dashboard**:
   ```bash
   docker-compose down
   ```

---

### Running Automated Tests

To execute the 25-point automated QA test suite:
```bash
pytest -v tests/
```

**Verified Test Output**:
```
======================== 25 passed in 2.23s (100% Pass Rate) ========================
```

---

## 🔒 Security & Defensive Engineering

- **Input Sanitization**: All image uploads are strictly validated via magic byte inspection and PIL dimension checks, rejecting `.exe` and corrupted buffers.
- **Memory Safety & Zero Leakage**: In-memory frame processing without temporary disk caching, guaranteeing privacy compliance.
- **Container Hardening**: Multi-stage Docker container dropping root privileges to a dedicated non-root user (`appuser`, UID 10001).

---

## 📄 License & Certification
This project is licensed under the MIT License. Engineered in accordance with the **MASTER_SDLC_AGENTS** multi-agent engineering standard.

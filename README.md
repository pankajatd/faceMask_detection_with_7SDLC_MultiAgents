# 😷 AI Face Mask Detection & Safety Compliance Dashboard

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Deep Learning](https://img.shields.io/badge/Model-MediaPipe%20BlazeFace%20(CNN)-green.svg)](https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-25%2F25%20Passing-brightgreen.svg)]()

An enterprise-ready, on-premise Computer Vision application that performs real-time face detection, protective mask verification, and workplace safety compliance auditing. Built using Google MediaPipe BlazeFace Deep Learning Convolutional Neural Network (CNN) with an automatic OpenCV Haar Cascade fallback engine.

---

## 🌟 Key Features

- **High-Accuracy Deep Learning Face Detector**: Utilizes a pre-trained Caffe ResNet-10 SSD architecture ($300 \times 300$), robust against head tilts, side-angle profiles, low-lighting, and multi-person crowds.
- **Fail-Safe Fallback**: Automatically activates OpenCV's built-in Frontal Face Haar Cascade detector if deep learning model weights are absent, guaranteeing zero application crashes.
- **Multi-Feature Mask Classifier**: Evaluates lower facial regions ($55\%\text{--}92\%$ height) against surgical light blue, white N95, dark fabric/black, and texture uniformity.
- **Interactive Web Dashboard**:
  - **Photo Analysis Mode**: Drag-and-drop custom file uploader (`.jpg`, `.jpeg`, `.png`) with byte corruption validation.
  - **1-Click Demo Samples**: Pre-loaded benchmark samples (Doctor in Scrubs, Medical Team, Two Nurses, Black Mask, White N95, Bare Face).
  - **Live Camera Snapshot Mode**: Direct webcam frame capture for real-time verification.
  - **Real-Time KPI Cards**: Total Faces Detected, Compliant Count (Green), Non-Compliant Count (Red), and Compliance Rate percentage.
  - **Export Capabilities**: 1-click download of high-definition annotated images with color-coded bounding boxes and confidence labels.
- **100% On-Premise & Privacy-First**: Zero external cloud API calls, zero telemetry, and zero data leakage.

---

## 📁 Repository Structure

```
faceMask_detection/
├── models/                     # Deep learning model weights & architecture
│   ├── deploy.prototxt         # Caffe model architecture definition
│   └── res10_300x300_ssd_iter_140000.caffemodel  # Trained ResNet-10 SSD weights
├── src/                        # Production application source code
│   ├── app.py                  # Streamlit web dashboard application
│   ├── detector.py             # ResNet-10 SSD + Haar fallback & mask classifier
│   └── utils.py                # Image validation, conversions, and adaptive labels
├── tests/                      # Automated test suite and test datasets
│   ├── test_images/            # Real-world benchmark test images
│   ├── test_detector.py        # Model loading & integration tests
│   └── test_utils.py           # Unit tests for image validation & drawing
├── packages.txt                # Linux system dependencies for Streamlit Cloud
├── Dockerfile                  # Container build instructions (Mini-Linux + OpenCV)
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

2. **Create and Activate a Virtual Environment** (Optional but recommended):
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

1. Open **[share.streamlit.io](https://share.streamlit.io)**
2. Click **New app** $\rightarrow$ select this repository.
3. Set Main file path to: `src/app.py`
4. Click **Deploy!**

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

## 🧪 Quality Assurance & Defect Governance (Gate 5)

The codebase includes a comprehensive 25-point automated QA test suite. This project strictly adheres to **Rule 2 Closed-Loop Defect Governance** (`QA Agent Logs Bug ➔ Software Developer Agent Resolves ➔ QA Agent Retests ➔ Closed`):

| Defect Ticket | Code Logic Category | Failing Condition / Description | Developer Resolution | Defect Status |
| :--- | :--- | :--- | :--- | :---: |
| [**BUG-001**](reports/defects/BUG-001.md) | **Colorspace Math** | Inverted BGR/RGB channels made warm bare skin evaluate as a blue surgical mask | Enforced strict RGB normalization before channel math | 🟢 **CLOSED** |
| [**BUG-002**](reports/defects/BUG-002.md) | **Geometry / Slicing** | Mask crop started at 70% height, cutting off nose on N95 respirators | Expanded anatomical crop to 55%–92% covering nose & mouth | 🟢 **CLOSED** |
| [**BUG-003**](reports/defects/BUG-003.md) | **Feature Logic** | Dark mask check only evaluated brightness, mistaking human beards for black masks | Added texture variance check (`mean_std < 14.0`) to separate fabric from hair | 🟢 **CLOSED** |

Full official test execution report: [qa-test-report.md](reports/qa-test-report.md) (**25 / 25 automated tests passed, 100% Pass Rate**).

To execute tests:
```bash
pytest -v tests/
```

**Expected Output**:
```
======================== 25 passed in 2.55s ========================
```

---

## 🔒 Security & Privacy

- **Input Sanitization**: Image uploads are verified via `PIL.Image.verify()` and format whitelisting (`JPEG`, `PNG`).
- **Memory Safety**: No temporary user files are saved to disk during web inspection; all frames are decoded from memory buffers.
- **Container Hardening**: The Dockerfile runs as a dedicated non-root user (`appuser`, UID 1000) with stripped build dependencies.

---

## 📄 License
This project is licensed under the MIT License.

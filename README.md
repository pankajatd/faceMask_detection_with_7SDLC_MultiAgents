# 😷 AI Face Mask Detection & Safety Compliance Dashboard

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Deep Learning](https://img.shields.io/badge/Model-ResNet--10%20SSD-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-25%2F25%20Passing-brightgreen.svg)]()

An enterprise-ready, on-premise Computer Vision application that performs real-time face detection, protective mask verification, and workplace safety compliance auditing. Built using a deep-learning ResNet-10 Single Shot Multibox Detector (SSD) with an automatic OpenCV Haar Cascade fallback engine.

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
├── Dockerfile                  # Production container definition
├── docker-compose.yml          # Single-command container deployment
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

### Option 2: Run with Docker

1. **Build the Container Image**:
   ```bash
   docker build -t facemask-detection:1.0.0 .
   ```

2. **Run the Container**:
   ```bash
   docker run -d -p 8501:8501 --name facemask_app facemask-detection:1.0.0
   ```
   Access the dashboard at **`http://localhost:8501`**.

---

### Option 3: Run with Docker Compose

To start the service in background daemon mode:
```bash
docker-compose up -d
```

To stop the service:
```bash
docker-compose down
```

---

## 🧪 Running Automated Tests

The codebase includes a comprehensive 25-point automated QA test suite covering happy paths, negative paths, boundary clipping, and corrupt inputs.

To execute tests:
```bash
pytest -v tests/
```

**Expected Output**:
```
======================== 25 passed in 0.80s ========================
```

---

## 🔒 Security & Privacy

- **Input Sanitization**: Image uploads are verified via `PIL.Image.verify()` and format whitelisting (`JPEG`, `PNG`).
- **Memory Safety**: No temporary user files are saved to disk during web inspection; all frames are decoded from memory buffers.
- **Container Hardening**: The Dockerfile runs as a dedicated non-root user (`appuser`, UID 1000) with stripped build dependencies.

---

## 📄 License
This project is licensed under the MIT License.

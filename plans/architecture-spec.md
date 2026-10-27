# Technical Architecture Specification
## Project: Face Mask Detection System (`faceMask_detection`)
**Author:** Technical Architect Subagent  
**Status:** DRAFT FOR HITL GATE 2 REVIEW  
**Scope:** High-Level System Design & Technology Stack Selection  

---

## 1. System Overview & Architectural Approach
To satisfy the business needs defined in `plans/PRD.md`, the system is architected as a **modular, client-server web application** divided into two primary high-level systems:

```
+-------------------------------------------------------------+
|                 PRESENTATION LAYER (Web UI)                 |
|   - Handles user file uploads (.jpg, .png)                  |
|   - Handles real-time camera video stream                   |
|   - Provides interactive sensitivity controls (sliders)     |
|   - Renders visual results (Green / Red alerts)             |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                 AI INFERENCE ENGINE (Backend)               |
|   - Stage 1: Face Detection (Locates faces in image)        |
|   - Stage 2: Mask Classification (Detects mask presence)    |
|   - Stage 3: Annotation Renderer (Draws boxes & statistics) |
+-------------------------------------------------------------+
```

---

## 2. Technology Stack Selection & Rationale

| System Layer | Selected Technology | Architectural Rationale |
| :--- | :--- | :--- |
| **Core Runtime** | **Python 3.10+** | Industry standard for machine learning, computer vision, and rapid application development. |
| **Computer Vision Engine** | **OpenCV** | Provides ultra-fast, CPU-optimized image decoding, color conversion, and image rendering without requiring expensive GPU hardware. |
| **AI Inference Model** | **Pretrained Deep Learning Model (CNN)** | A two-stage convolutional neural network: one to detect face boundaries, and one lightweight binary classifier to predict mask compliance with high accuracy. |
| **Web UI Framework** | **Streamlit** | Enables building clean, interactive web applications directly in Python with built-in support for file drag-and-drop, sliders, and camera feeds. |
| **Automated Test Runner** | **Pytest** | Standard test runner for verifying image processing pipelines and detection accuracy. |

---

## 3. High-Level System Components & Boundaries

### Component A: Web Presentation Layer
* **Responsibility**: Manages all user-facing interactions.
* **Boundaries**: Strictly handles user inputs, file uploads, display of annotated images, and download actions. Contains no AI detection algorithms.

### Component B: AI Detection & Inference Engine
* **Responsibility**: Ingests raw image matrices, locates faces, and determines mask compliance.
* **Boundaries**: Pure analytical engine. Operates independently of the web framework so it can be tested in isolation or reused in other interfaces.

### Component C: Annotation & Visualization Engine
* **Responsibility**: Combines detection results with the original image.
* **Boundaries**: Applies color-coded overlays (**Green for Mask**, **Red for No Mask**) and calculates compliance statistics (total faces, compliant count, non-compliant count).

---

## 4. Non-Functional System Attributes

* **Hardware Efficiency**: Architected to execute efficiently on standard multi-core consumer/server CPUs without requiring dedicated GPUs.
* **Modularity**: The AI engine is decoupled from the UI layer to allow independent testing and future upgrades.
* **Security & Isolation**: The internal development tools (`.agents/`) are completely decoupled from the production application.

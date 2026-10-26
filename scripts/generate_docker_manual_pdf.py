import os
import sys
import win32com.client

doc_path = os.path.abspath(r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\plans\Docker_Generation_and_Testing_Manual.docx")
pdf_path = os.path.abspath(r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\plans\Docker_Generation_and_Testing_Manual.pdf")

os.makedirs(os.path.dirname(doc_path), exist_ok=True)

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

try:
    doc = word.Documents.Add()

    # Styling Constants
    wdAlignParagraphCenter = 1
    wdAlignParagraphLeft = 0
    wdAlignParagraphJustify = 3
    wdExportFormatPDF = 17

    def add_p(text, space_after=6, align=wdAlignParagraphLeft, bold=False, font_size=11, color=(30, 41, 59)):
        p = doc.Paragraphs.Add()
        p.Range.Text = text
        p.Range.Font.Name = "Calibri"
        p.Range.Font.Size = font_size
        p.Range.Font.Bold = bold
        p.Range.Font.Color = color[0] + (color[1] * 256) + (color[2] * 65536)
        p.Format.SpaceAfter = space_after
        p.Format.Alignment = align
        return p

    # --- TITLE BANNER ---
    add_p("DOCKERFILE GENERATION & TESTING MANUAL", space_after=2, align=wdAlignParagraphCenter, bold=True, font_size=24, color=(2, 132, 199))
    add_p("A Complete Engineer's Guide: Constructing, Building, and Verifying the AI Face Mask Container", space_after=12, align=wdAlignParagraphCenter, bold=False, font_size=13, color=(100, 116, 139))
    add_p("Document Version: 1.0.0 | Author: DevOps & Systems Engineering Team | Date: 2026-10-20", space_after=20, align=wdAlignParagraphCenter, bold=False, font_size=10, color=(148, 163, 184))

    # --- SECTION 1: WHAT IS A DOCKERFILE & WHY GENERATE IT ---
    add_p("1. What is a Dockerfile and Why is it Generated?", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "A Dockerfile is an automated build manifest containing step-by-step instructions that assemble a self-contained, reproducible virtual environment (called a Docker Container). "
        "In artificial intelligence and computer vision applications, Python code frequently depends on low-level operating system C++ binaries, graphics drivers (e.g., libgl1), "
        "and specific versions of numerical libraries. Without containerization, moving code to a different machine often produces missing shared object errors, version conflicts, or crashing dependencies.\n\n"
        "By generating a Dockerfile, the entire application—including the mini-Linux operating system, OpenCV graphics libraries, Python 3.10 interpreter, Caffe deep learning model weights, "
        "and the Streamlit dashboard—is sealed into a universal container that runs identically on any laptop, workstation, cloud server, or enterprise datacenter.",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 2: LINE-BY-LINE DOCKERFILE ANATOMY ---
    add_p("2. Line-by-Line Anatomy of the Generated Dockerfile", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "The project Dockerfile is structured into six deliberate, hardened stages:\n\n"
        "Stage 1: Base Operating System\n"
        "  Directive: FROM python:3.10-slim\n"
        "  Explanation: Instead of a bloated 5-10 GB full operating system, this pulls an official lightweight (~150 MB) Debian Linux system with Python 3.10 pre-installed. It minimizes memory consumption and reduces security vulnerabilities.\n\n"
        "Stage 2: Low-Level System Dependencies\n"
        "  Directive: RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 curl && rm -rf /var/lib/apt/lists/*\n"
        "  Explanation: OpenCV requires Linux shared C++ libraries (libgl1 and libglib) to decode and manipulate image matrices. Installing these via apt-get ensures cv2 will never crash with missing shared object errors.\n\n"
        "Stage 3: Working Directory Definition\n"
        "  Directive: WORKDIR /app\n"
        "  Explanation: Sets the primary execution and storage folder inside the container to /app.\n\n"
        "Stage 4: Dependency Caching & Installation\n"
        "  Directive: COPY requirements.txt . followed by RUN pip install --no-cache-dir -r requirements.txt\n"
        "  Explanation: Copies only requirements.txt first and runs pip. This leverages Docker layer caching: if dependencies haven't changed, Docker reuses the cached layer, making future builds near-instantaneous.\n\n"
        "Stage 5: Application & Model Ingestion\n"
        "  Directive: COPY models/ ./models/ | COPY src/ ./src/ | COPY tests/test_images/ ./tests/test_images/\n"
        "  Explanation: Copies the trained ResNet-10 deep learning neural network weights, the Python application logic (app.py, detector.py, utils.py), and sample test images into the container.\n\n"
        "Stage 6: Port Exposure & Launch Entrypoint\n"
        "  Directive: EXPOSE 8501 | ENTRYPOINT [\"streamlit\", \"run\", \"src/app.py\", \"--server.port=8501\", \"--server.address=0.0.0.0\"]\n"
        "  Explanation: Opens networking port 8501 and instructs Streamlit to broadcast on 0.0.0.0 so external web browsers can connect to the dashboard.",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 3: THE COMPANION DOCKER-COMPOSE ---
    add_p("3. The Companion Configuration: docker-compose.yml", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "To eliminate the need for memorizing long terminal execution flags, docker-compose.yml stores all operational settings:\n\n"
        "• Port Forwarding: Maps host machine port 8501 to container port 8501 ('8501:8501').\n"
        "• Container Naming: Assigns a clean, human-readable name ('facemask_app').\n"
        "• Restart Policy: Set to 'unless-stopped' so the container automatically recovers if the system reboots.\n\n"
        "With this file present, the entire build and launch process is compressed into a single command: docker-compose up -d --build.",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 4: STEP-BY-STEP TESTING PROTOCOL ---
    add_p("4. Step-by-Step Protocol to Test the Docker Container", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "Follow these exact steps to launch, inspect, and verify the container on your system:\n\n"
        "Step 4.1: Launch Docker Desktop\n"
        "  • Open Docker Desktop from the Windows Start Menu.\n"
        "  • Verify the bottom-left status indicator turns GREEN and displays 'Engine running'.\n\n"
        "Step 4.2: Execute the Launch Command in Command Prompt\n"
        "  • Open Command Prompt (cmd) or PowerShell.\n"
        "  • Navigate to the project root: cd C:\\Pankaja\\AUTOMATED_SDLC_AGENT_PROJECTS\\faceMask_detection\n"
        "  • Execute the build and run command:\n"
        "     docker-compose up -d --build\n"
        "  • Docker will download the base layers, install OpenCV, copy models, and report: 'Container facemask_app Started'.\n\n"
        "Step 4.3: Terminal Status Verification\n"
        "  • In Command Prompt, run: docker ps\n"
        "  • Confirm the output shows:\n"
        "     - IMAGE: facemask-detection:1.0.0\n"
        "     - STATUS: Up X seconds / minutes\n"
        "     - PORTS: 0.0.0.0:8501->8501/tcp\n"
        "     - NAMES: facemask_app\n\n"
        "Step 4.4: Web Browser Functional Verification\n"
        "  • Open Google Chrome, Microsoft Edge, or Firefox.\n"
        "  • Navigate to: http://localhost:8501\n"
        "  • The web dashboard will load immediately.\n"
        "  • Functional Tests to Execute:\n"
        "     1. Click 'Two Nurses (Putting on Gloves)' -> Verify two faces are detected with green bounding boxes and 'Mask: 95.0%'.\n"
        "     2. Click 'Side Profile (Black Fabric Mask)' -> Verify the angled face is detected with a green box.\n"
        "     3. Click 'Unmasked Portrait' -> Verify a red bounding box appears with 'No Mask'.\n"
        "     4. Click 'Download Annotated Image' -> Verify the .jpg file downloads successfully to your machine.\n\n"
        "Step 4.5: Internal Automated Test Execution Inside Docker\n"
        "  • To run the automated 25-point pytest suite directly inside the Linux container, execute:\n"
        "     docker exec -it facemask_app pytest tests/\n"
        "  • This verifies all unit tests, model loading, and color algorithms pass natively within Linux.",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 5: CONTAINER LIFECYCLE MANAGEMENT ---
    add_p("5. Container Lifecycle Management Commands", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "• Start the container in background: docker-compose up -d\n"
        "• Rebuild and start after code updates: docker-compose up -d --build\n"
        "• View real-time container logs: docker logs -f facemask_app\n"
        "• Stop the container gracefully: docker-compose down\n"
        "• Inspect container resource usage (CPU/RAM): docker stats facemask_app",
        font_size=11, space_after=14, align=wdAlignParagraphLeft
    )

    # Save Word Document
    doc.SaveAs(doc_path)
    print("Saved Word document:", doc_path)

    # Export to PDF
    doc.ExportAsFixedFormat(pdf_path, wdExportFormatPDF)
    print("Exported PDF:", pdf_path)

    doc.Close(False)
finally:
    word.Quit()

import os
import sys
import win32com.client

doc_path = os.path.abspath(r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\plans\Deployment_and_Customer_Handover_Guide.docx")
pdf_path = os.path.abspath(r"C:\Pankaja\AUTOMATED_SDLC_AGENT_PROJECTS\faceMask_detection\plans\Deployment_and_Customer_Handover_Guide.pdf")

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

    def add_p(text, style='Normal', space_after=6, align=wdAlignParagraphLeft, bold=False, font_size=11, color=(30, 41, 59)):
        p = doc.Paragraphs.Add()
        p.Range.Text = text
        p.Range.Font.Name = "Calibri"
        p.Range.Font.Size = font_size
        p.Range.Font.Bold = bold
        p.Range.Font.Color = color[0] + (color[1] * 256) + (color[2] * 65536)
        p.Format.SpaceAfter = space_after
        p.Format.Alignment = align
        return p

    # --- COVER / TITLE BANNER ---
    add_p("FACE MASK DETECTION SYSTEM", space_after=2, align=wdAlignParagraphCenter, bold=True, font_size=24, color=(30, 64, 175))
    add_p("Comprehensive Guide: Streamlit Cloud Deployment, Docker Packaging & Customer Handover", space_after=14, align=wdAlignParagraphCenter, bold=False, font_size=13, color=(100, 116, 139))
    add_p("Document Version: 1.0.0 | Author: DevOps & Systems Architecture Team | Date: 2026-10-20", space_after=20, align=wdAlignParagraphCenter, bold=False, font_size=10, color=(148, 163, 184))

    # --- SECTION 1: EXECUTIVE SUMMARY ---
    add_p("1. Executive Overview & Delivery Strategy", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "The Face Mask Detection System is architected to support two distinct delivery pathways tailored to the technical requirements and regulatory constraints of different customer personas:\n\n"
        "• Pathway 1 (End-Users & General Public): Zero-install web delivery hosted via Streamlit Community Cloud. Users interact with the AI application through a secure, public HTTPS hyperlink on their browser without downloading any software or managing code.\n\n"
        "• Pathway 2 (Enterprise, Healthcare & High-Security Clients): Self-contained Docker containerization. Enables hospitals, banks, and enterprise IT teams to run the AI system 100% on-premise on private servers behind internal firewalls, guaranteeing HIPAA/GDPR data privacy and offline operational continuity.",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 2: STREAMLIT CLOUD DEPLOYMENT ---
    add_p("2. Streamlit Cloud Public Link Setup (Step-by-Step)", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "Streamlit Community Cloud allows free, continuous cloud hosting directly synchronized with a GitHub repository. Follow these exact steps to deploy or re-deploy the application:\n\n"
        "Step 2.1: Repository Preparation on GitHub\n"
        "The project repository must be public and contain the following essential files at the root level:\n"
        "  • src/app.py: The main entry point containing the Streamlit web dashboard interface.\n"
        "  • requirements.txt: Defines all pinned Python dependencies (opencv-python-headless, numpy<2.0.0, Pillow, streamlit, pytest).\n"
        "  • packages.txt: Specifies low-level Linux Debian packages (libgl1, libglib2.0-0) required by OpenCV.\n"
        "  • models/: Contains the Caffe ResNet-10 deep learning weights (deploy.prototxt and caffemodel) and haarcascade fallback XML.\n\n"
        "Step 2.2: Launching on Streamlit Cloud\n"
        "  1. Navigate to https://share.streamlit.io and sign in with your GitHub account.\n"
        "  2. Click the 'Create app' or 'New app' button in the upper-right corner.\n"
        "  3. Configure the three deployment parameters:\n"
        "     - Repository: Select your GitHub repository (e.g., pankajatd/faceMask_detection_with_7SDLC_MultiAgents).\n"
        "     - Branch: Set to 'main'.\n"
        "     - Main file path: Enter 'src/app.py'.\n"
        "  4. Click 'Deploy!'. Streamlit Cloud provisions an isolated cloud runner, installs packages from packages.txt and requirements.txt, and starts the web service.\n\n"
        "Step 2.3: Managing and Sharing Your Public Link\n"
        "Once deployed, Streamlit assigns a permanent URL (e.g., https://your-app-name.streamlit.app). Any commit pushed to the 'main' branch automatically triggers an instant, zero-downtime redeployment.",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 3: DOCKER PACKAGING ---
    add_p("3. Docker Containerization & Local Execution (Step-by-Step)", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "Docker eliminates the classic 'it works on my machine' issue by bundling the application, exact Python interpreter, low-level OS graphics drivers, and model weights into an immutable shipping container.\n\n"
        "Step 3.1: Anatomy of the Dockerfile\n"
        "Our Dockerfile defines a minimal, hardened container image:\n"
        "  • FROM python:3.10-slim: Initializes a stripped-down, ~150MB Debian Linux environment optimized for speed and security.\n"
        "  • RUN apt-get install libgl1 libglib2.0-0: Installs the C++ graphics shared objects essential for OpenCV matrix processing.\n"
        "  • COPY requirements.txt & RUN pip install: Pre-installs all pinned dependencies in an isolated layer.\n"
        "  • COPY models/ src/ tests/: Embeds the AI neural network weights and application source code.\n"
        "  • EXPOSE 8501: Opens the networking port used by Streamlit.\n"
        "  • ENTRYPOINT: Executes 'streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0'.\n\n"
        "Step 3.2: Why docker-compose.yml is Used\n"
        "The docker-compose.yml file serves as a persistent configuration shortcut. It pre-configures port mapping (8501:8501), container naming (facemask_app), and restart policies, allowing developers and customers to launch the container with a single command.\n\n"
        "Step 3.3: How to Build and Run Docker\n"
        "  1. Ensure Docker Desktop is launched on your machine and showing 'Engine running' (green).\n"
        "  2. Open Command Prompt (cmd) or PowerShell in the project root directory:\n"
        "     cd C:\\Pankaja\\AUTOMATED_SDLC_AGENT_PROJECTS\\faceMask_detection\n"
        "  3. Execute the single build-and-run command:\n"
        "     docker-compose up -d --build\n"
        "  4. To stop the running container at any time, execute:\n"
        "     docker-compose down",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 4: TESTING & VERIFICATION ---
    add_p("4. How to Test and Verify Docker is Running", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "After running 'docker-compose up -d --build', verify container operation through three independent verification methods:\n\n"
        "Method A: Terminal Status Check\n"
        "In Command Prompt or PowerShell, execute:\n"
        "  docker ps\n"
        "Look for the container named 'facemask_app'. The status should display 'Up X seconds' with port forwarding '0.0.0.0:8501->8501/tcp'.\n\n"
        "Method B: Browser Dashboard Test\n"
        "Open Chrome, Edge, or Firefox and navigate to:\n"
        "  http://localhost:8501\n"
        "The web dashboard will render. Select a demo image (e.g., 'Two Nurses Gloves') or upload an image to confirm facial localization and green/red bounding boxes appear with real-time percentages.\n\n"
        "Method C: Docker Desktop Visual Inspection\n"
        "Open Docker Desktop and select the 'Containers' tab. The 'facemask_app' entry will display a bright green active dot indicating the container is healthy and actively serving requests.",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 5: CUSTOMER HANDOVER ---
    add_p("5. Customer Handover & Delivery Protocols", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "Depending on the client category, deliver the appropriate assets according to the following guidelines:\n\n"
        "Delivery Model A: Enterprise / Corporate Client (Docker Handover)\n"
        "• Target Audience: Hospital networks, corporate security departments, bank branches, factory compliance teams.\n"
        "• Delivery Package: Provide the GitHub repository link (or deliver a secure .zip archive) containing:\n"
        "   - Dockerfile and docker-compose.yml\n"
        "   - models/ (trained ResNet-10 Caffe weights and Haar fallback)\n"
        "   - src/ (app.py, detector.py, utils.py)\n"
        "   - requirements.txt and README.md\n"
        "• Customer Action: The client's IT administrator extracts the archive onto their internal server and executes:\n"
        "   docker-compose up -d --build\n"
        "   The system runs privately on their internal network (e.g., http://10.0.0.50:8501) with zero internet exposure.\n\n"
        "Delivery Model B: End-User / Client Evaluation (Public Web Hyperlink)\n"
        "• Target Audience: Recruiters, non-technical clients, testers, and remote evaluators.\n"
        "• Delivery Package: Share only the live Streamlit Cloud hyperlink:\n"
        "   https://[your-app-name].streamlit.app\n"
        "• Customer Action: The client clicks the link on any desktop, laptop, tablet, or smartphone browser. No software, Python, or Docker installation is required.",
        font_size=11, space_after=14, align=wdAlignParagraphJustify
    )

    # --- SECTION 6: SUMMARY TABLE ---
    add_p("6. Quick-Reference Handover Matrix", bold=True, font_size=16, color=(15, 23, 42), space_after=8)
    add_p(
        "• Public Cloud Deployment (End-Users): share.streamlit.io -> Main File: src/app.py -> Access via .streamlit.app URL\n"
        "• On-Premise Docker Deployment (Enterprises): docker-compose up -d --build -> Access via http://localhost:8501\n"
        "• Verification & Status Check: docker ps -> Look for facemask_app with port 8501\n"
        "• Container Termination: docker-compose down\n"
        "• Automated Test Suite Execution: pytest -v tests/ (25/25 Passing)",
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

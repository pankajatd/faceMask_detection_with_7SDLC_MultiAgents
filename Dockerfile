# Base operating system: Python 3.10 on lightweight Linux
FROM python:3.10-slim

# Install system-level graphics libraries required by OpenCV on Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code, AI models, and sample test images
COPY models/ ./models/
COPY src/ ./src/
COPY tests/test_images/ ./tests/test_images/

# Expose Streamlit port
EXPOSE 8501

# Command to launch the dashboard when the container starts
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

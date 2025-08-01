FROM python:3.9-slim

# Install system dependencies including wget and build essentials
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    libsndfile1 \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Pre-download model during build
RUN mkdir -p /models && \
    wget -O /models/onsets_frames_wavinput.tflite \
    https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==20.1.0

COPY . .

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/_health || exit 1

# Use exec form for proper signal handling
CMD ["gunicorn", "--bind", ":$PORT", "--timeout", "300", "--workers", "1", "--preload", "app:app"]

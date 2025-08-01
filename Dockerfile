FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including libsndfile and ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Pre-download model during build
RUN mkdir -p /models && \
    wget -O /models/onsets_frames_wavinput.tflite \
    https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==20.1.0

COPY . .

# Use exec form for CMD and explicit port binding
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "300", "--workers", "1", "app:app"]

FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pre-download model to avoid startup delays
RUN mkdir -p /models && \
    wget -O /models/onsets_frames_wavinput.tflite \
    https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==20.1.0

COPY . .

# Use exec form for CMD and explicit port binding
CMD exec gunicorn --bind :$PORT --timeout 300 --workers 1 --threads 8 app:app

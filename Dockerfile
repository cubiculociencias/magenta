FROM python:3.9-slim

# Instala dependencias incluyendo curl (más confiable que wget)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Descarga el modelo DURANTE EL BUILD (crítico)
RUN mkdir -p /models && \
    curl -f -s -S --retry 5 -o /models/onsets_frames_wavinput.tflite \
    https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput_no_offset_uni.tflite

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==20.1.0

COPY . .

# Health check optimizado
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f

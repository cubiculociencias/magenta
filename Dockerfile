FROM python:3.9-slim

# 1. Install wget first
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 2. Then download the model
RUN mkdir -p /models && \
    wget -O /models/onsets_frames_wavinput.tflite \
    https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==20.1.0

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "--bind", ":$PORT", "--timeout", "300", "--workers", "1", "app:app"]

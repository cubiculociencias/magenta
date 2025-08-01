# Usa una imagen base de Python
FROM python:3.9-slim

# Crea el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema operativo y curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Descarga el modelo DURANTE EL BUILD y lo guarda en /app/models
RUN mkdir -p /app/models && \
    curl -f -s -S --retry 5 -o /app/models/onsets_frames_wavinput.tflite \
    https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para iniciar la aplicación con Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

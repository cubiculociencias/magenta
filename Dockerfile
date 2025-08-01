# Usa una imagen base con Python 3.7 (compatible con TensorFlow 1.15)
FROM python:3.7-slim

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Instala pip y las dependencias con versiones específicas
RUN pip install --upgrade pip && \
    pip install numpy==1.16.4 tensorflow==1.15.5 magenta==1.1.7 flask==2.0.3

# Copia el código (evita copiar antes de instalar dependencias)
COPY . .

CMD ["python", "main.py"]

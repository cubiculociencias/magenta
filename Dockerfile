# Usa una imagen específica de Python 3.7 con Slim
FROM python:3.7-slim

WORKDIR /app

# Instala dependencias del sistema CRÍTICAS
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    build-essential \  # Necesario para compilar algunas dependencias
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias en ORDEN específico para evitar conflictos
RUN pip install --upgrade pip==20.2.4 && \
    pip install numpy==1.16.4 && \
    pip install tensorflow==1.15.5 && \
    pip install magenta==1.1.7 --no-deps && \
    pip install flask==2.0.3

COPY . .

CMD ["python", "main.py"]

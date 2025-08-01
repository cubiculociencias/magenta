# Usa una imagen base más reciente pero compatible
FROM python:3.7-slim

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Instala TensorFlow y Magenta con versiones específicas
RUN pip install --upgrade pip && \
    pip install tensorflow==1.15.5 \
    magenta==1.1.7 \
    flask \
    numpy==1.16.4  # Versión compatible con TF 1.15

# Copia el código
COPY . .

CMD ["python", "main.py"]

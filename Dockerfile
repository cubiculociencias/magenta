FROM tensorflow/tensorflow:1.15.5-py3

WORKDIR /app

# Instalar herramientas de sistema para compilar paquetes (evita errores como el tuyo)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Instalar numpy primero
RUN pip install --upgrade pip
RUN pip install numpy

# Copiar requirements.txt y luego el resto
COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]

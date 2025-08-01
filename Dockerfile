# Imagen base ligera compatible con Cloud Run
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Crear carpeta de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Puerto por defecto de Flask
ENV PORT=8080

# Comando para lanzar el servidor
CMD ["python", "main.py"]

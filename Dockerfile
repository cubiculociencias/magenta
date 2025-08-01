FROM tensorflow/tensorflow:1.15.5-py3

WORKDIR /app

COPY requirements.txt .  

# Instalamos numpy primero para evitar errores de dependencias
RUN pip install --upgrade pip && \
    pip install numpy && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]

# Usa una imagen base oficial de Node.js
FROM node:18-slim

# Instala wget para poder descargar archivos
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Crea y establece el directorio de trabajo
WORKDIR /app

# Descarga el modelo de Magenta
RUN mkdir -p /app/modelos && \
    wget -O /app/modelos/onsets_frames_wavinput.tflite \
    https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite

# Copia los archivos de manifiesto del proyecto (package.json y package-lock.json)
# para instalar las dependencias
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto de los archivos de la aplicación
COPY . .

# Cloud Run escuchará en el puerto definido por la variable de entorno $PORT
ENV PORT 8080
EXPOSE $PORT

# Define el comando para ejecutar tu aplicación
CMD ["npm", "start"]

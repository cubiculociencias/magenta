# Usa una imagen base oficial de Node.js
FROM node:18-slim

# Crea y establece el directorio de trabajo
WORKDIR /app

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

const express = require('express');
const app = express();

// Cloud Run proporciona el puerto en la variable de entorno PORT
const port = parseInt(process.env.PORT) || 8080;

app.get('/', (req, res) => {
  res.send('Hola desde Cloud Run!');
});

app.listen(port, () => {
  console.log(`La aplicación se está ejecutando en el puerto ${port}`);
});

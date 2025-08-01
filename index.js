const express = require('express');
const app = express();
const mm = require('@magenta/music');

// Cloud Run proporciona el puerto en la variable de entorno PORT
const port = parseInt(process.env.PORT) || 8080;

app.get('/', (req, res) => {
  res.send('Hola desde Cloud Run! Usa /generar para invocar a Magenta.');
});

// Endpoint para invocar una función de Magenta (ejemplo)
app.get('/generar', async (req, res) => {
  try {
    const music_vae = new mm.MusicVAE('/path/to/checkpoint');
    await music_vae.initialize();
    
    // Aquí iría tu lógica con la librería Magenta
    // Por ejemplo, generar una melodía
    const result = await music_vae.sample(1);

    res.json({
      message: 'Melodía generada con éxito',
      melodia: result
    });

  } catch (error) {
    res.status(500).send('Ocurrió un error al generar la música: ' + error.message);
  }
});

app.listen(port, () => {
  console.log(`La aplicación se está ejecutando en el puerto ${port}`);
});

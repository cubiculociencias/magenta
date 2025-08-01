const express = require('express');
const app = express();
// Importar los módulos específicos de Magenta para Node
const core = require('@magenta/music/node/core');
const music_vae = require('@magenta/music/node/music_vae');

// Cloud Run proporciona el puerto en la variable de entorno PORT
const port = parseInt(process.env.PORT) || 8080;

app.get('/', (req, res) => {
  res.send('Hola desde Cloud Run! Usa /generar para invocar a Magenta.');
});

// Endpoint para invocar una función de Magenta (ejemplo)
app.get('/generar', async (req, res) => {
  try {
    // La documentación sugiere inicializar el modelo de esta forma
    const vaeModel = new music_vae.MusicVAE('https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite');
    await vaeModel.initialize();
    
    // Aquí iría tu lógica con la librería Magenta
    // Por ejemplo, generar una melodía
    const result = await vaeModel.sample(1);

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

import express from 'express';
import multer from 'multer';
import { OnsetsAndFrames } from '@magenta/music/node/transcription';
import { midiToSequenceProto } from '@magenta/music/node/protobuf';
import fs from 'fs';
import librosa from 'librosa';

const app = express();
const upload = multer({ dest: 'uploads/' });

// Configuración del modelo
const MODEL_URL = 'https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite';
const model = new OnsetsAndFrames(MODEL_URL);

app.post('/transcribe', upload.single('audio'), async (req, res) => {
  try {
    // 1. Cargar audio usando librosa
    const { audioBuffer, sampleRate } = await librosa.load(req.file.path, { sr: 16000, mono: true });

    // 2. Inicializar modelo
    await model.initialize();

    // 3. Transcribir audio a MIDI
    const ns = await model.transcribeFromAudioBuffer(audioBuffer, sampleRate);

    // 4. Convertir a archivo MIDI
    const midiBytes = midiToSequenceProto(ns);
    
    // 5. Enviar como descarga
    res.setHeader('Content-Type', 'audio/midi');
    res.setHeader('Content-Disposition', 'attachment; filename=converted.mid');
    res.send(Buffer.from(midiBytes));

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error en la conversión' });
  } finally {
    // Limpiar archivo temporal
    fs.unlinkSync(req.file.path);
  }
});

app.listen(8080, () => {
  console.log('Servidor escuchando en http://localhost:8080');
});

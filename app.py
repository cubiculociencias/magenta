from flask import Flask, request, jsonify, send_file
import os
import numpy as np
import tempfile
import soundfile as sf
import pretty_midi
from utils.tflite_model import Model

app = Flask(__name__)

# Descargar el modelo TFLite primero (ejecutar una vez)
MODEL_URL = "https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite"
MODEL_PATH = "onsets_frames_wavinput.tflite"

if not os.path.exists(MODEL_PATH):
    import urllib.request
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

model = Model(MODEL_PATH)

@app.route('/')
def home():
    return 'Servidor de transcripción Magenta TFLite en Cloud Run.'

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se envió un archivo de audio'}), 400

    audio_file = request.files['audio']
    
    try:
        # Guardar temporalmente y cargar audio
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            audio, sr = sf.read(tmp.name, dtype='float32')
            
            # Redimensionar a mono y remuestrear si es necesario
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)
            if sr != model.sample_rate:
                from librosa import resample
                audio = resample(audio, orig_sr=sr, target_sr=model.sample_rate)
            
            # Rellenar/recortar a la longitud esperada
            if len(audio) < model.get_input_wav_length():
                audio = np.pad(audio, (0, model.get_input_wav_length() - len(audio)))
            else:
                audio = audio[:model.get_input_wav_length()]
            
            # Añadir dimensión de batch
            audio = np.expand_dims(audio, axis=0)

        # Inferencia
        result = model.infer(audio)
        
        # Convertir a MIDI
        midi = pretty_midi.PrettyMIDI()
        piano = pretty_midi.Instrument(program=0)
        
        onsets = result[0][0]  # Obtener resultados de onsets
        frames = result[1][0]  # Obtener resultados de frames
        
        active_notes = {}
        timestep = model.get_timestep() / 1000.0  # Convertir a segundos
        
        for t in range(onsets.shape[0]):
            for pitch in range(onsets.shape[1]):
                # Detección de onsets
                if onsets[t, pitch] > 0.5:  # Umbral
                    start_time = t * timestep
                    note = pretty_midi.Note(
                        velocity=100,
                        pitch=pitch + 21,  # A1 (21) es el pitch más bajo en el modelo
                        start=start_time,
                        end=start_time + 0.1  # Duración inicial corta
                    )
                    piano.notes.append(note)
                    active_notes[pitch] = note
                
                # Extender notas activas si el frame aún está activo
                elif pitch in active_notes and frames[t, pitch] > 0.5:
                    active_notes[pitch].end = t * timestep

        midi.instruments.append(piano)
        
        # Devolver como archivo MIDI
        midi_path = tempfile.NamedTemporaryFile(suffix=".mid", delete=False).name
        midi.write(midi_path)
        
        return send_file(
            midi_path,
            mimetype='audio/midi',
            as_attachment=True,
            download_name="transcription.mid"
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'midi_path' in locals() and os.path.exists(midi_path):
            os.remove(midi_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

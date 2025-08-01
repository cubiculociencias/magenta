from flask import Flask, request, jsonify
import soundfile as sf
import numpy as np
import tempfile
import os
import subprocess
import urllib.request
import tensorflow as tf

app = Flask(__name__)

MODEL_URL = 'https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite'
MODEL_PATH = 'onsets_frames_wavinput.tflite'

# Descargar modelo si no existe
if not os.path.exists(MODEL_PATH):
    print('Descargando modelo...')
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

# Cargar modelo TFLite
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@app.route('/')
def index():
    return 'Magenta Audio to MIDI Transcriber (Cloud Run Backend)'

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'input.webm')
        wav_path = os.path.join(tmpdir, 'converted.wav')
        audio_file.save(input_path)

        try:
            # Convertir webm a wav (mono, 16kHz)
            subprocess.run(['ffmpeg', '-i', input_path, '-ar', '16000', '-ac', '1', wav_path], check=True)

            # Cargar audio
            audio, sr = sf.read(wav_path)
            if sr != 16000:
                return jsonify({'error': 'Sample rate mismatch after conversion'}), 500

            # Asegurarse de que el audio tenga forma (N,1) o (N,)
            if audio.ndim == 2:
                audio = audio[:, 0]

            # Preprocesamiento simple (normalizar y reshape)
            audio = audio / np.max(np.abs(audio))
            audio = np.expand_dims(audio.astype(np.float32), axis=0)

            # Ajustar tamaño si es necesario
            expected_len = input_details[0]['shape'][1]
            if audio.shape[1] > expected_len:
                audio = audio[:, :expected_len]
            elif audio.shape[1] < expected_len:
                pad_width = expected_len - audio.shape[1]
                audio = np.pad(audio, ((0, 0), (0, pad_width)), mode='constant')

            # Ejecutar modelo
            interpreter.set_tensor(input_details[0]['index'], audio)
            interpreter.invoke()

            output = interpreter.get_tensor(output_details[0]['index'])

            # Simulación: generar notas falsas desde el output
            notes = []
            for i, prob in enumerate(output[0]):
                if prob > 0.5:
                    notes.append({
                        'pitch': 60 + (i % 12),
                        'startTime': i * 0.1,
                        'endTime': (i + 1) * 0.1
                    })

            return jsonify({'notes': notes})

        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'FFmpeg failed', 'details': str(e)}), 500
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

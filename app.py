from flask import Flask, request, jsonify, send_file
import os
import numpy as np
import tempfile
import wave
import pretty_midi
from utils.tflite_model import Model

app = Flask(__name__)
model = Model("https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite")

@app.route('/')
def home():
    return 'Servidor de transcripción Magenta TFLite en Cloud Run.'

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se envió un archivo de audio .wav'}), 400

    audio_file = request.files['audio']

    # Guardar temporalmente
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_path = tmp.name
        audio_file.save(audio_path)

    try:
        # Leer archivo WAV
        with wave.open(audio_path, 'rb') as wf:
            samples = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
            samples = samples.astype(np.float32) / 32768.0
            samples = np.expand_dims(samples[:model.get_input_wav_length()], axis=0)

        result = model.infer(samples)

        # Aquí deberías convertir `result` en una secuencia MIDI (simplificado)
        midi = pretty_midi.PrettyMIDI()
        piano = pretty_midi.Instrument(program=0)

        timestep = model.get_timestep() / 1000.0  # ms to seconds
        threshold = 0.5

        for t, time_slice in enumerate(result[0]):
            for n, (frame, onset) in enumerate(time_slice[:, :2]):
                if onset > threshold:
                    start = t * timestep
                    end = start + 0.3
                    note = pretty_midi.Note(velocity=100, pitch=21 + n, start=start, end=end)
                    piano.notes.append(note)

        midi.instruments.append(piano)

        output_path = tempfile.NamedTemporaryFile(suffix=".mid", delete=False).name
        midi.write(output_path)

        return send_file(output_path, as_attachment=True, download_name="transcription.mid")

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(audio_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

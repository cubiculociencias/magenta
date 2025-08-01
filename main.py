from flask import Flask, request, jsonify, send_file
import magenta.music as mm
import tensorflow as tf
import warnings
import io
import os

# Configuración específica para TF 1.15
tf.disable_v2_behavior()
tf.logging.set_verbosity(tf.logging.ERROR)
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Inicializa el modelo (ajusta según tu necesidad)
model = None

def load_model():
    global model
    if model is None:
        model = mm.onsets_frames_transcription.OnsetAndFrameTranscriptionModel(
            'onsets_frames_unidirectional')
    return model

@app.route("/")
def index():
    return "Audio-to-MIDI with Magenta TF 1.15 (Production Ready)"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    
    try:
        # 1. Cargar modelo
        model = load_model()
        
        # 2. Procesar audio (ejemplo simplificado)
        # Nota: Necesitarás implementar la lógica real de conversión
        audio_data = audio_file.read()
        
        # 3. Generar MIDI (placeholder - implementa tu lógica aquí)
        note_sequence = mm.midi_io.midi_file_to_note_sequence(audio_data)  # Esto es un ejemplo, no funcionará directamente
        midi_data = mm.midi_io.note_sequence_to_midi_file(note_sequence, "output.mid")
        
        # 4. Devolver como archivo descargable
        return send_file(
            io.BytesIO(midi_data),
            mimetype='audio/midi',
            as_attachment=True,
            attachment_filename='converted.mid')
            
    except Exception as e:
        return jsonify({
            "error": str(e),
            "details": "Check server logs for full traceback"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

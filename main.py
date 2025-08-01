from flask import Flask, request, jsonify
import magenta.music as mm
import tensorflow as tf
import warnings

# Suprime warnings de TensorFlow
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
warnings.filterwarnings("ignore")

app = Flask(__name__)

@app.route("/")
def index():
    return "Audio-to-MIDI with Magenta TF 1.15 (Stable Version)"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
        
    try:
        # Procesamiento simulado (reemplaza con tu lógica real)
        return jsonify({
            "status": "success",
            "message": "MIDI data placeholder"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

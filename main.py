from flask import Flask, request, jsonify
import numpy as np
import tensorflow.lite as tflite
import tempfile
import os

app = Flask(__name__)

# Cargar el modelo desde la URL pública de GCS
MODEL_URL = "https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput_no_offset_uni.tflite"
interpreter = None

def download_and_load_model():
    import requests
    global interpreter

    with tempfile.NamedTemporaryFile(delete=False, suffix=".tflite") as tmp:
        print("Descargando modelo...")
        r = requests.get(MODEL_URL)
        tmp.write(r.content)
        tmp.flush()
        interpreter = tflite.Interpreter(model_path=tmp.name)
        interpreter.allocate_tensors()
        print("Modelo cargado.")

@app.route('/_health')
def health_check():
    return jsonify({"status": "ready"}), 200

# Endpoint de preparación (readyness)
@app.route('/_ready')
def ready_check():
    # Verifica si el modelo está cargado
    if model_initialized:  # Reemplaza con tu variable de estado
        return jsonify({"status": "ready"}), 200
    else:
        return jsonify({"status": "loading"}), 503

@app.route("/predict", methods=["POST"])
def predict():
    if "audio" not in request.files:
        return jsonify({"error": "Debes subir un archivo de audio (audio)"}), 400

    file = request.files["audio"]
    audio_path = os.path.join(tempfile.gettempdir(), file.filename)
    file.save(audio_path)

    # Aquí deberías procesar el audio (resamplear, normalizar, convertir a espectrograma, etc.)
    # Este paso depende mucho del modelo. Por ahora solo placeholder.
    return jsonify({"status": "audio recibido, procesamiento pendiente"})


@app.route("/")
def home():
    return "Magenta Cloud Run backend listo."

if __name__ == "__main__":
    download_and_load_model()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

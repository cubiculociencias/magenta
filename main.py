from flask import Flask, jsonify
import os
import logging
from utils.tflite_model import Model

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carga el modelo de forma SÍNCRONA al inicio
MODEL_PATH = "models/onsets_frames_wavinput.tflite"

logger.info("Loading model...")
try:
    model = Model(MODEL_PATH)
    logger.info("Model loaded successfully")
except FileNotFoundError:
    logger.error(f"Error: Model file not found at {MODEL_PATH}")
    model = None
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    if model:
        return 'Ready for transcriptions'
    else:
        return 'Model failed to load. Check logs for details.', 500

@app.route('/_health')
def health_check():
    if model:
        return jsonify({"status": "healthy"}), 200
    else:
        return jsonify({"status": "unhealthy", "message": "Model not loaded"}), 503

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if not model:
        return 'Model not ready', 503
    
    # ... (rest of your existing transcribe logic)

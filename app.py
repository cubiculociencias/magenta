from flask import Flask, request, send_file
import os
import logging
from utils.tflite_model import Model

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health check endpoint (required by Cloud Run)
@app.route('/_health')
def health_check():
    return 'OK', 200

# Initialize model in background
model = None

def initialize_model():
    global model
    MODEL_URL = "https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/tflite/onsets_frames_wavinput.tflite"
    MODEL_PATH = "/tmp/onsets_frames_wavinput.tflite"
    
    if not os.path.exists(MODEL_PATH):
        logger.info("Downloading model...")
        import urllib.request
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    
    logger.info("Loading model...")
    model = Model(MODEL_PATH)
    logger.info("Model loaded successfully")

# Start initialization immediately
initialize_model()

@app.route('/')
def home():
    return 'Ready for transcriptions' if model else 'Initializing...'

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if model is None:
        return 'Model not ready', 503
    
    # ... (rest of your existing transcribe logic)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=True)

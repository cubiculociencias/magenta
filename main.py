from flask import Flask, request, jsonify
import magenta.music as mm
import tensorflow as tf

app = Flask(__name__)

@app.route("/")
def index():
    return "Audio-to-MIDI with Magenta and TF 1.15"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    return jsonify({"message": "Transcription logic placeholder."})

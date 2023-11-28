'''
from flask import Flask, render_template, request
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os

app = Flask(__name__)

# Load the ASR model from Hugging Face
device = "cpu"
torch_dtype = torch.float32

model_id = "openai/whisper-large-v3"

try:
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)
    model.to(device)
except Exception as e:
    print(f"error with automodel : {e}")

try:
    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )
except Exception as e:
    print(f"error with pipeline : {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio_file' not in request.files:
        return render_template('error.html', error='No file part')

    audio_file = request.files['audio_file']

    if audio_file.filename == '':
        return render_template('error.html', error='No selected file')

    try:
        # Perform ASR using the Hugging Face model
        transcription = pipe(audio_file.read())[0]['sentence']

        return render_template('result.html', transcription=transcription)

    except Exception as e:
        return render_template('error.html', error=str(e))
'''
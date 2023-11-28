from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load the ASR model from Hugging Face
asr_model = pipeline(task="automatic-speech-recognition", model="facebook/whisper-large-v3")

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
        transcription = asr_model(audio_file.read())[0]['sentence']

        return render_template('result.html', transcription=transcription)

    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

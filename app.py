import whisperx
from flask import Flask, request, jsonify, render_template
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/')
def index():
    return render_template('./load.html')

@app.route('/upload', methods=['POST'])


def upload_file():

    if 'audio_file' not in request.files:
        return 'No se proporcionó ningún archivo'

    uploaded_file = request.files['audio_file']

    if uploaded_file.filename == '':
        return 'No se proporcionó ningún archivo'

    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        # Realiza la transcripción y alineación
        device = "cuda"
        batch_size = 16
        compute_type = "float16"

        # Transcripción
        model = whisperx.load_model("large-v2", device, compute_type=compute_type)
        audio = whisperx.load_audio(file_path)
        result = model.transcribe(audio, language='es', batch_size=batch_size)

        # Alineación
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

        # Concatenating the transcribed segments
        transcription_text = "\n".join([segment['text'] for segment in result["segments"]])
        return f'Archivo de audio "{file_path}" cargado con éxito.\n {transcription_text}'
    else:
        return 'No se proporcionó ningún archivo de audio.'


    return transcription_text
if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify
import os
from notes_generate import generate_notes, transcribe_audio, split_audio, transcribe_directory

app = Flask(__name__)

@app.route('/transcribe_and_generate_notes', methods=['POST'])
def transcribe_and_generate_notes():
    if 'audio_file' not in request.files:
        return "No audio_file key in request.files", 400

    file = request.files['audio_file']

    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        output_directory = "audio_chunks"
        chunk_length_ms = 5 * 60 * 1000  # 5 minutes in milliseconds
        
        # Save the file
        audio_file_path = os.path.join(output_directory, file.filename)
        file.save(audio_file_path)

        # Process the audio file
        split_audio(audio_file_path, output_directory, chunk_length_ms)
        transcription = transcribe_directory(output_directory)
        notes = generate_notes('gpt-3.5', transcription)  # 'davinci' or any other model you want to use

        return jsonify(notes)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'mp3', 'm4a'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
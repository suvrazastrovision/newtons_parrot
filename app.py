import os
import wave
from flask import Flask, request, send_file, render_template, jsonify
from io import BytesIO
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
MODEL_NAME = "gemini-3-flash-preview"
TTS_MODEL_NAME = "gemini-3.1-flash-tts-preview"
VOICE_NAME = "Kore"

def text_to_audio_file(text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=TTS_MODEL_NAME,
        contents=f"Speak naturally in a friendly, conversational tone: {text}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=VOICE_NAME
                    )
                )
            ),
        ),
    )
    audio_data = response.candidates[0].content.parts[0].inline_data.data
    audio_file = BytesIO()
    with wave.open(audio_file, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_data)
    audio_file.seek(0)
    return audio_file


def ask_question(content):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable")

    question_content = f"Answer clearly and conversationally: {content}"

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=question_content
    )
    print(response.text)
    return response.text
# ask_question("how are you?")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    sentence = request.form.get('sentence')
    print(sentence)
    print(type(sentence))

    if not sentence:
        return {"error": "Please provide a sentence"}, 400
    try:
        answer = ask_question(sentence)
        if not answer:
            return jsonify({"error": "AI returned an empty answer"}), 502
        audio_file = text_to_audio_file(answer)
    except Exception as exc:
        return jsonify({"error": f"AI service error: {exc}"}), 502

    return send_file(audio_file, mimetype='audio/wav', download_name='response.wav')


if __name__ == '__main__':
    app.run(debug=True)

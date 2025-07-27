import os
import wave
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

# Load the Vosk model only once
MODEL_PATH = "models/vosk-model-small-en-us-0.15"  # Download and place model here
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Vosk model not found at {MODEL_PATH}")
model = Model(MODEL_PATH)

def convert_to_wav(uploaded_file) -> str:
    """Convert uploaded audio file to 16kHz WAV and return path"""
    audio = AudioSegment.from_file(uploaded_file.file)
    audio = audio.set_channels(1).set_frame_rate(16000)

    temp_file = NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_file.name, format="wav")
    return temp_file.name

def transcribe_audio(wav_path: str) -> str:
    """Transcribe WAV file using Vosk"""
    wf = wave.open(wav_path, "rb")
    recognizer = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            results.append(json.loads(recognizer.Result())["text"])
    results.append(json.loads(recognizer.FinalResult())["text"])

    return " ".join(results)

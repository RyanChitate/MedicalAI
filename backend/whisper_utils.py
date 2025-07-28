import whisper
import os
from datetime import datetime

model = whisper.load_model("base")  # Use "tiny" or "small" for better speed

def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(file_path)
    return result["text"]

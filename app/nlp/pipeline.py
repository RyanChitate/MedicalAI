from app.nlp.transcriber import convert_to_wav, transcribe_audio
from app.nlp.extractor import extract_medical_info
import os

def process_audio(uploaded_file):
    # Step 1: Convert to compatible WAV format
    wav_path = convert_to_wav(uploaded_file)

    try:
        # Step 2: Transcribe audio to text
        transcript = transcribe_audio(wav_path)

        # Step 3: Extract medical entities using NLP
        entities = extract_medical_info(transcript)

        return {
            "transcript": transcript,
            "entities": entities
        }

    finally:
        # Clean up temporary WAV file
        if os.path.exists(wav_path):
            os.remove(wav_path)

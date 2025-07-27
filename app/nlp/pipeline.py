from app.nlp.transcriber import convert_to_wav, transcribe_audio
from app.nlp.extractor import extract_medical_info

def process_audio(uploaded_file):
    wav_path = convert_to_wav(uploaded_file)
    transcript = transcribe_audio(wav_path)
    entities = extract_medical_info(transcript)

    return {
        "transcript": transcript,
        "entities": entities
    }

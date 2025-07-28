import spacy
from typing import Dict

nlp = spacy.load("en_core_web_sm")

def section_soap_note(text: str) -> Dict[str, str]:
    sections = {"subjective": [], "objective": [], "assessment": [], "plan": []}
    doc = nlp(text.lower())

    for sent in doc.sents:
        s = sent.text.strip()
        if any(k in s for k in ["complains", "reports", "feels", "describes"]):
            sections["subjective"].append(s)
        elif any(k in s for k in ["examined", "noted", "bp", "pulse", "on inspection"]):
            sections["objective"].append(s)
        elif any(k in s for k in ["impression", "diagnosis", "we suspect", "assessment"]):
            sections["assessment"].append(s)
        elif any(k in s for k in ["plan", "we will", "start", "prescribe", "recommend"]):
            sections["plan"].append(s)
        else:
            sections["subjective"].append(s)  # Default bucket

    return {k: " ".join(v) for k, v in sections.items()}

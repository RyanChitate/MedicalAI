import spacy

try:
    nlp = spacy.load("en_core_med7_lg")
except:
    raise RuntimeError("Med7 model not installed. Install it from: https://med7.s3.eu-west-2.amazonaws.com/en_core_med7_lg-0.0.1.tar.gz")

# Med7 supported entities: DRUG, STRENGTH, FORM, DOSAGE, ROUTE, FREQUENCY, DURATION
def extract_medical_info(text: str):
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        results.append({
            "text": ent.text,
            "label": ent.label_
        })
    return results

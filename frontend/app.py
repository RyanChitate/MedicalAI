import streamlit as st
import requests
import os
import sys
from pathlib import Path

# Add the project root (MedicalAI/) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Local processing imports
from backend.whisper_utils import transcribe_audio
from backend.nlp import section_soap_note

# Constants
API_URL = "http://localhost:8000"
AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

st.title("🩺 Voice-to-EHR: Offline SOAP Notes")

# --- Fetch patients from backend ---
patients = requests.get(f"{API_URL}/patients").json()
patient_names = [p["name"] for p in patients]
patient_map = {p["name"]: p["id"] for p in patients}

# --- Select or create a patient ---
if patient_names:
    selected = st.selectbox("👤 Select Patient", options=patient_names)
    selected_id = patient_map[selected] if selected else None
else:
    st.warning("⚠️ No patients found. Please create one first.")
    selected = None
    selected_id = None

with st.expander("➕ Create New Patient"):
    with st.form("create_patient_form"):
        new_name = st.text_input("Enter Patient Name")
        submitted = st.form_submit_button("Create")
        if submitted and new_name:
            r = requests.post(f"{API_URL}/patients/", json={"name": new_name})
            if r.status_code == 200:
                st.success(f"✅ Patient '{new_name}' created!")
                st.experimental_rerun()
            else:
                st.error("❌ Failed to create patient.")

# --- Upload and transcribe voice note ---
if selected_id:
    st.header("📤 Upload Voice Note")
    audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a"])

    if audio_file:
        file_path = AUDIO_DIR / audio_file.name
        with open(file_path, "wb") as f:
            f.write(audio_file.getbuffer())
        st.success("✅ Audio uploaded and saved.")

        if st.button("🎙️ Transcribe & Process"):
            with st.spinner("Transcribing..."):
                transcript = transcribe_audio(str(file_path))
            with st.spinner("Processing with NLP..."):
                soap = section_soap_note(transcript)

            st.subheader("📝 Generated SOAP Note")
            st.text_area("Subjective", value=soap["subjective"], height=100)
            st.text_area("Objective", value=soap["objective"], height=100)
            st.text_area("Assessment", value=soap["assessment"], height=100)
            st.text_area("Plan", value=soap["plan"], height=100)

            # Save note to backend
            note_payload = {
                "subjective": soap["subjective"],
                "objective": soap["objective"],
                "assessment": soap["assessment"],
                "plan": soap["plan"]
            }

            save_note = requests.post(f"{API_URL}/patients/{selected_id}/notes", json=note_payload)
            if save_note.status_code == 200:
                st.success("💾 SOAP note saved to database!")
            else:
                st.error("❌ Failed to save note.")

# --- Patient note history ---
if selected_id and st.checkbox("📚 Show Patient History"):
    st.subheader("🧾 Previous Notes")
    notes = requests.get(f"{API_URL}/patients/{selected_id}/notes").json()

    if notes:
        for note in reversed(notes):
            st.markdown("---")
            st.write(f"🗓️ **Date**: {note['date']}")
            for sec in ["subjective", "objective", "assessment", "plan"]:
                st.markdown(f"**{sec.title()}:**")
                st.markdown(note[sec])
    else:
        st.info("ℹ️ No notes found for this patient.")

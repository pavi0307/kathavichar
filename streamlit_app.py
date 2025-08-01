import streamlit as st
import requests
import tempfile
import os
import base64
from pydub import AudioSegment
import speech_recognition as sr

st.set_page_config(page_title="KathaVichar", layout="centered")

# App UI
st.title("🎙️ KathaVichar - Voice to Story Translator")
st.write("Translate your spoken English story into Telugu.")

# Step 1: Voice input
st.subheader("Step 1: Record or Upload Your Voice")

uploaded_file = st.file_uploader("Upload an audio file (WAV/MP3)", type=["wav", "mp3"])
text_input = None

if uploaded_file:
    st.audio(uploaded_file, format='audio/wav')

    # Save uploaded file to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(uploaded_file.read())
        temp_audio_path = temp_audio_file.name

    # Convert MP3 to WAV if needed
    if uploaded_file.name.endswith(".mp3"):
        sound = AudioSegment.from_mp3(temp_audio_path)
        temp_wav_path = temp_audio_path.replace(".mp3", ".wav")
        sound.export(temp_wav_path, format="wav")
        temp_audio_path = temp_wav_path

    # Transcribe using SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text_input = recognizer.recognize_google(audio_data)
            st.success("Transcription successful!")
            st.write("🔤 Transcribed Text:")
            st.write(text_input)
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Speech Recognition error: {e}")

# Step 2: Translation
if text_input:
    st.subheader("Step 2: Translate to Telugu")

    if st.button("Translate"):
        with st.spinner("Translating..."):
            # Send to Hugging Face API
            api_url = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-te"
            headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
            payload = {"inputs": text_input}

            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                translated = response.json()[0]["translation_text"]
                st.success("🈯 Translated Telugu Output:")
                st.write(translated)
            else:
                st.error(f"Translation failed. Status code: {response.status_code}")

# Cleanup
if uploaded_file:
    os.remove(temp_audio_path)

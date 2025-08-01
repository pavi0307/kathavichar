import streamlit as st
from datetime import datetime
import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr

st.set_page_config(page_title="KathaVichar - Image to Story", layout="centered")

st.title("📸 KathaVichar - Image to Story")
st.markdown("Choose an image, speak or write a story it brings to your mind!")

# --- Image options ---
image_options = {
    "Charminar": "prompts/charminar.jpg",
    "Fort": "prompts/fort.jpg",
    "Market": "prompts/market.jpg"
}

selected_image = st.selectbox("Select an image:", list(image_options.keys()))
st.image(image_options[selected_image], caption=f"Story prompt: {selected_image}", use_container_width=True)

# --- Language selection ---
language = st.selectbox("Select language:", ["English", "Telugu", "Hindi", "Other"])

# --- Story input method ---
input_method = st.radio("Choose input method:", ["Write Story", "Speak Story"])

story_text = ""

if input_method == "Write Story":
    story_text = st.text_area("📝 Write your story or memory here:", height=200)

else:
    st.info("🎤 Upload a voice recording (WAV or MP3) and we will transcribe it for you.")
    uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])
    if uploaded_file:
        st.audio(uploaded_file)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(uploaded_file.read())
            temp_audio_path = temp_audio_file.name

        if uploaded_file.name.endswith(".mp3"):
            sound = AudioSegment.from_mp3(temp_audio_path)
            wav_path = temp_audio_path.replace(".wav", "_converted.wav")
            sound.export(wav_path, format="wav")
            temp_audio_path = wav_path

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                story_text = recognizer.recognize_google(audio_data)
                st.success("✅ Transcription successful!")
                st.write("📝 Transcribed story:")
                st.write(story_text)
            except Exception as e:
                st.error(f"Could not transcribe audio: {e}")

# --- Submit button and saving ---
if st.button("Submit Story"):
    if story_text.strip() == "":
        st.warning("⚠️ Please provide a story either by typing or voice before submitting.")
    else:
        save_path = "user_stories.txt"
        with open(save_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] - {selected_image} - Language: {language}\n{story_text}\n\n")
        st.success("✅ Your story has been saved!")
        st.info(f"Saved at: {os.path.abspath(save_path)}")

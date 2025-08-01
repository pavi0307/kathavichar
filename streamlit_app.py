import streamlit as st
from datetime import datetime
import os
import speech_recognition as sr
from pydub import AudioSegment
import io
from streamlit_audiorec import st_audiorec

st.set_page_config(page_title="KathaVichar - Image to Story", layout="centered")
st.title("📸 KathaVichar - Image to Story")
st.markdown("Let your voice or words tell the story of our culture!")

# Step 1: Choose image
st.markdown("### 🪜 Step 1: Choose an image")
image_options = {
    "Charminar": "prompts/charminar.jpg",
    "Fort": "prompts/fort.jpg",
    "Market": "prompts/market.jpg"
}
selected_image = st.selectbox("Select an image:", list(image_options.keys()))
st.image(image_options[selected_image], caption=f"Prompt: {selected_image}", use_container_width=True)

# Step 2: Select language
st.markdown("### 🪜 Step 2: Choose your language")
language = st.radio("Language:", ["English", "Telugu", "Hindi", "Other"], horizontal=True)

# Step 3: Story input
st.markdown("### 🪜 Step 3: Share your story")

story = st.text_area("✍️ Type your story (or use voice below):", height=200)

st.markdown("🎤 Or record your voice below (English only for now):")
wav_audio_data = st_audiorec()

if wav_audio_data:
    audio = AudioSegment.from_file(io.BytesIO(wav_audio_data), format="wav")
    audio.export("temp.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            voice_text = recognizer.recognize_google(audio_data)
            st.success("✅ Transcription successful!")
            st.markdown(f"🗣️ **You said:** {voice_text}")
            story += "\n" + voice_text  # Append voice to story box
        except sr.UnknownValueError:
            st.error("😕 Sorry, could not understand your voice.")
        except sr.RequestError:
            st.error("⚠️ Could not reach the speech service.")

# Step 4: Submit
if st.button("📤 Submit Story"):
    if story.strip():
        file_path = os.path.abspath("user_stories.txt")
        with open("user_stories.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] - {selected_image} - Language: {language}\n{story}\n\n")
        st.success("✅ Thank you! Your story has been saved.")
        st.balloons()
        st.info(f"📁 Story saved at: {file_path}")
    else:
        st.warning("⚠️ Please type or speak your story before submitting.")

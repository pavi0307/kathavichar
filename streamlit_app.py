# streamlit_app.py

import streamlit as st
import csv
import datetime
import speech_recognition as sr
import tempfile
import os

# Title
st.set_page_config(page_title="KathaVichar", layout="centered")
st.title("📚 KathaVichar – Your Multilingual Story Assistant")

# Step-by-step UI
st.markdown("### Step 1: Enter your name")
user_name = st.text_input("Your name")

st.markdown("### Step 2: Pick a language")
language = st.selectbox("Choose a language", ["English", "Telugu", "Hindi", "Tamil"])

st.markdown("### Step 3: Choose how to share your story idea")
mode = st.radio("Input type", ["🧠 Type your idea", "🎙️ Use voice input"])

# Get user input (text or voice)
story_prompt = ""
if mode == "🧠 Type your idea":
    story_prompt = st.text_area("Enter your story idea")
else:
    st.markdown("Upload a short voice clip (WAV or MP3 format)")
    audio_file = st.file_uploader("Upload audio", type=["wav", "mp3"])
    if audio_file is not None:
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)
            try:
                story_prompt = recognizer.recognize_google(audio_data)
                st.success(f"Transcribed text: {story_prompt}")
            except sr.UnknownValueError:
                st.error("Sorry, could not understand the audio.")
            except sr.RequestError:
                st.error("API unavailable. Please try again later.")
        os.remove(tmp_path)

# Sample story generator (replace with real LLM output later)
def generate_story(prompt, lang):
    return f"Here’s a short folk story in {lang} based on your prompt:\n\nOnce upon a time... (story continues from: '{prompt}')"

# Submit button
if st.button("Generate Story"):
    if not user_name or not story_prompt:
        st.warning("Please enter your name and a story prompt.")
    else:
        story_output = generate_story(story_prompt, language)
        st.success("✅ Story generated!")
        st.text_area("Your story", story_output, height=250)

        # Save to CSV
        with open("user_stories.txt", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.datetime.now(), user_name, language, story_prompt, story_output])

        st.markdown("🎉 **Thank you! Your story has been saved.**")


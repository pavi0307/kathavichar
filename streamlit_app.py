import streamlit as st
from datetime import datetime
import os

# ✅ Page setup for mobile-friendly layout
st.set_page_config(page_title="KathaVichar - Image to Story", layout="centered")

# ✅ App Title and Intro
st.title("📸 KathaVichar - Image to Story")
st.markdown("Welcome to **KathaVichar!**\n\nTurn your memories into stories by choosing an image and writing what it reminds you of.")

# ✅ Step 1: Select language
st.markdown("### 🪜 Step 1: Choose Your Language")
language = st.selectbox("Pick a language to write your story in:", ["English", "Telugu", "Hindi", "Other"])

# ✅ Step 2: Select image
st.markdown("### 🖼️ Step 2: Pick an Image Prompt")
image_options = {
    "Charminar": "prompts/charminar.jpg",
    "Fort": "prompts/fort.jpg",
    "Market": "prompts/market.jpg"
}
selected_image = st.selectbox("Choose an image that brings a memory to mind:", list(image_options.keys()))
image_path = image_options[selected_image]
st.image(image_path, caption=f"Prompt: {selected_image}", use_column_width=True)

# ✅ Step 3: Write your story
st.markdown("### ✍️ Step 3: Share Your Story")
story = st.text_area("Write your memory or story here:", height=200)

# ✅ Step 4: Submit and save story
st.markdown("### ✅ Step 4: Submit")
if st.button("Submit My Story"):
    if story.strip():
        file_path = os.path.abspath("user_stories.txt")
        with open("user_stories.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] - {selected_image} - Language: {language}\n{story}\n\n")

        st.success("🎉 Your story has been saved successfully!")
        st.balloons()
        st.markdown("💖 **Thank you for contributing to KathaVichar!** Your memory is now part of our story archive.")
        st.info(f"📁 File location: `{file_path}`")
    else:
        st.warning("⚠️ Please write something before submitting.")

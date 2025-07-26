import streamlit as st
from datetime import datetime
import os

# Set Streamlit page configuration
st.set_page_config(page_title="KathaVichar - Image to Story", layout="centered")

# ✅ Optional: Show a banner image at the top
st.image("data/kathavichar_image.jpg", use_column_width=True)

# Title and intro
st.title("📸 KathaVichar - Image to Story")
st.markdown("Choose an image and share a memory or story it brings to your mind!")

# Dropdown image options
image_options = {
    "Charminar": "prompts/charminar.jpg",
    "Fort": "prompts/fort.jpg",
    "Market": "prompts/market.jpg"
}

# Image selection dropdown
selected_image = st.selectbox("Select an image:", list(image_options.keys()))
image_path = image_options[selected_image]

# Display image
st.image(image_path, caption=f"Story prompt: {selected_image}", use_container_width=True)

# Story input box
story = st.text_area("📝 Your story or memory:", height=200)

# Submit and save
if st.button("Submit"):
    if story.strip():
        file_path = os.path.abspath("user_stories.txt")
        with open("user_stories.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] - {selected_image}\n{story}\n\n")
        st.success("✅ Your story has been saved!")
        st.info(f"📁 Saved at: `{file_path}`")
    else:
        st.warning("⚠️ Please write something before submitting.")

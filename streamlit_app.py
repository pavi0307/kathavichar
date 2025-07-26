
import os
print("📁 Current working directory:", os.getcwd())
import streamlit as st

st.set_page_config(page_title="KathaVichar", layout="centered")

st.title("🧠 KathaVichar: Local Story Collector")

st.image("prompts/charminar.jpg", caption="What story or memory does this image bring to mind?")

user_input = st.text_area("✍️ Write your story or description below (in any language):")

if st.button("Submit"):
    if user_input.strip():
        with open("data/user_stories.txt", "a", encoding="utf-8") as f:
            f.write(user_input + "\n---\n")
        st.success("✅ Thank you! Your story has been recorded.")
    else:
        st.warning("⚠️ Please enter a story before submitting.")

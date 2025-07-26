import streamlit as st
from datetime import datetime

st.title("KathaVichar - Image to Story")

st.image("prompts/charminar.jpg", caption="What story or memory does this image bring to mind?")

story = st.text_area("Share your story:", height=200)

if st.button("Submit"):
    with open("user_stories.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {story}\n\n")
    st.success("✅ Your story has been saved! Thank you.")

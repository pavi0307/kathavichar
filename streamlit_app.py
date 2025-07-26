import streamlit as st

# Set page title
st.set_page_config(page_title="KathaVichar", layout="centered")

# Title of the app
st.title("🖼️ KathaVichar - Tell Your Story")

# Show the image with caption
st.image("prompts/charminar.jpg", caption="What story or memory does this image bring to mind?")

# Prompt the user to enter their story or thoughts
user_input = st.text_area("Share your thoughts here:")

# Submit button
if st.button("Submit"):
    if user_input.strip() != "":
        st.success("Thank you for sharing your story! 🎉")
    else:
        st.warning("Please enter some text before submitting.")

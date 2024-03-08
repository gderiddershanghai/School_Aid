import streamlit as st
import openai
from io import BytesIO
import os
from dotenv import load_dotenv, find_dotenv
from module.helpers import extract_audio
from module.openai_helpers import get_transcription, get_video_feedback

# # Set up your OpenAI API key here
# _ = load_dotenv(find_dotenv()) # read local .env file
# openai.api_key  = os.getenv('OPENAI_API_KEY')

def page_1_video_feedback():
    # st.title('Video to Audio Converter')

    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""
    if 'comments' not in st.session_state:
        st.session_state.comments = ""

    # File uploader
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"], key="file_uploader")

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        audio_path = extract_audio(uploaded_file)
        st.success('Audio has been successfully extracted.')
        st.audio(audio_path)


        st.session_state.transcript = get_transcription(audio_path)
        # st.session_state.transcript = """
        # My grandma goes to school My grandma is taking me to school today
        # Good morning, miss said grandma This is our playground
        # Let's play together This is our classroom Together
        # It's story time Let's Let's listen together It's crying time Said Lisa
        # Let's say it together said grandma This is our music room said Lisa Let's sing together
        # said grandma Let's play together said grandma It's time to go home said Lisa
        # Goodbye miss said grandma It's lunchtime said grandma Let's eat together said Lisa
        # """
        st.text_area("Transcript", value=st.session_state.transcript, height=150, disabled=True)

    # Always show the form
    with st.form(key='comments_form'):
        st.session_state.comments = st.text_area("Comments", value=st.session_state.comments, height=150)
        submitted = st.form_submit_button("Generate Feedback")

    if submitted:
        # Assuming xyz takes the transcript and comments, and returns a string response
        feedback = get_video_feedback(st.session_state.transcript, st.session_state.comments)
        st.write(feedback)

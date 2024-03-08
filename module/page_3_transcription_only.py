import streamlit as st
from module.helpers import extract_audio
from module.openai_helpers import get_transcription, get_video_feedback
from module.metrics import get_readability_features

def page_3_transcription_only():
    # st.title('Video to Audio Converter')
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""


    # File uploader
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"], key="file_uploader")

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        audio_path = extract_audio(uploaded_file)
        st.success('Audio has been successfully extracted.')
        st.audio(audio_path)
        st.session_state.transcript = get_transcription(audio_path)
        readability = get_readability_features(st.session_state.transcript)

        st.text_area("Transcript", value=st.session_state.transcript + '\n\n' + readability, height=150, disabled=True)

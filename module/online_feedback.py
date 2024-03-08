import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO
from module.helpers import extract_english_text_from_pdf
from module.openai_helpers import get_online_class_feedback
import re

def page_2_online_feedback():
    # st.title('Online Class Feedback')

    # Initialize session state
    if 'uploaded_pdf' not in st.session_state:
        st.session_state.uploaded_pdf = None
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""
    if 'comments' not in st.session_state:
        st.session_state.comments = ""

    # PDF uploader
    uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"], key="pdf_uploader")

    if uploaded_pdf is not None:
        st.session_state.uploaded_pdf = uploaded_pdf
        st.session_state.transcript = extract_english_text_from_pdf(uploaded_pdf)
        st.success('Text has been successfully extracted from the PDF.')
        st.text_area("Extracted Text", value=st.session_state.transcript, height=150, disabled=True)
        if len(st.session_state.transcript) > 1500:
                st.warning('The extracted text is too long to display here.')
                st.session_state.transcript = st.session_state.transcript[:1500]


    # Comment form
    with st.form(key='comments_form'):
        comments_input = st.text_area("Comments", value=st.session_state.comments, height=150)
        submitted = st.form_submit_button("Generate Feedback")

    if submitted:
        # Update session state with the latest comments
        st.session_state.comments = comments_input
        # Generate feedback based on the extracted text and comments
        feedback = get_online_class_feedback(st.session_state.transcript, st.session_state.comments)
        st.write(feedback)  # Display the generated feedback

from moviepy.editor import VideoFileClip
from tempfile import NamedTemporaryFile
import streamlit as st
import ffmpeg
import tempfile
import fitz  # PyMuPDF
from io import BytesIO
import re

def extract_audio(video_file):
    """
    Extracts the audio from the uploaded video file using ffmpeg and returns the path to the audio file.

    :param video_file: The uploaded video file.
    :return: The path to the extracted audio file.
    """
    # Create temporary files for video and audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as video_temp, \
         tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as audio_temp:
        # Write the uploaded video to the temporary file
        video_temp.write(video_file.read())
        video_temp_path = video_temp.name
        audio_temp_path = audio_temp.name

    # Use ffmpeg to extract audio
    (
        ffmpeg
        .input(video_temp_path)
        .output(audio_temp_path, format='mp3')
        .run(overwrite_output=True, quiet=True)
    )
    print(audio_temp, '<<<<<<<<<<<<<<<<<<')
    return audio_temp_path

# Helper function to extract English text from PDF
def extract_english_text_from_pdf(uploaded_file):
    with fitz.open(stream=BytesIO(uploaded_file.getvalue())) as pdf_file:
        all_text = ""
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            all_text += page.get_text()
        # Filter English text and common punctuation
        english_text = re.sub(r'[^a-zA-Z0-9\s.,;!?\'"-]+', '', all_text)
    return english_text

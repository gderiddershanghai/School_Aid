import streamlit as st
from module.video_feedback import page_1_video_feedback
from module.online_feedback import page_2_online_feedback
from module.page_3_transcription_only import page_3_transcription_only

def intro():
    import streamlit as st

    st.write("# Welcome to the Teacher Aid App! 👋")
    st.sidebar.success("Choose how I can help you today.")

    st.markdown("""
    Streamlit powers this interactive teaching aid designed to support teachers with writing feedback. Functions include:

    1. **Video Feedback**: Upload the video, add some comments and let me take care of the rest.
    2. **Online Feedback**: Upload today's content along with some sentences on the student's performance and I'll turn it into a simple paragraph.
    3. **Video Transcription**: Let me help you type up what your students wrote.
    4. **OCR**: Take a picture of your student's esssay and I'll type it up for you. - in progress

    Get started by selecting from the dropdown on the left.
        """)


def page1_video():
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    # st.write('Video Homework Help')
    page_1_video_feedback()


def page2_online():
    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    # st.write('Online Class Feedback Help')
    page_2_online_feedback()

def page3_re2_transcription():
    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    # st.write('RE Video Transcription')
    page_3_transcription_only()

page_names_to_funcs = {
    "—": intro,
    "Video Feedback": page1_video,
    "Online Feedback": page2_online,
    "Essay Transcription": page3_re2_transcription
}

if 'current_demo' not in st.session_state:
    st.session_state['current_demo'] = None

# Sidebar selection box
demo_name = st.sidebar.selectbox("Choose Practice Type", list(page_names_to_funcs.keys()))

# # Check if the demo has changed
# if st.session_state['current_demo'] != demo_name:
#     st.session_state['current_demo'] = demo_name  # Update the current demo
#     reset_or_initialize_state()  # Reset or initialize state based on new demo

# Dynamically call the selected demo function
if demo_name in page_names_to_funcs:
    page_names_to_funcs[demo_name]()

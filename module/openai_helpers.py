from dotenv import load_dotenv
import os
from openai import OpenAI
import numpy as np

load_dotenv()

def get_transcription(audio_temp_path):
    # Retrieve the API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI(api_key=api_key)

    with open(audio_temp_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            language='en',
            # prompt="Do not correct mistakes",
            model="whisper-1",
            file=audio_file,
            response_format="text",
            temperature=0.2
        )
    print(transcription)
    return transcription


def get_video_feedback(transcript, teacher_comments):

    if len(teacher_comments)<10:
        return "Please add some comments"
    random_number = np.random.randint(1,10)
    temperature=random_number/10
    model="gpt-3.5-turbo"
    # model='gpt-4'
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI(api_key=api_key)

    if len(transcript)>5:

        system_message = """
        As an assistant to an ESL teacher, your role is to help craft feedback for video assignments submitted by students aged 4 to 8.
        Use the video transcript and the teacher's comments to generate simple, constructive feedback. Aim to encourage the student,
        suggest specific areas for improvement, and offer pronunciation tips. The feedback should be easy for young learners to understand.
        Below are examples of feedback that balance positive reinforcement with actionable advice.
        Make sure to include some of the vocabulary and sentence patterns from the transcript below in your feedback.
        Video Transcript:
        {transcript}
        """

        user_message = f"""
        Let's create feedback for a student's video.

        Teacher's Comments:
        {teacher_comments}

        Example Feedbacks:
        1. "Riding a bicycle" was perfectly said, and your explanation of activities was clear. Remember, using pronouns can make sentences shorter and conversations smoother. Great job, Jasper!
        2. Elsa, work on the "r" sound in "fork" to avoid confusion with other words. Your reading skills are impressive. Keep practicing!
        3. Great work, Lian! If possible, try reading the story a little bit more quickly and like the other kids in the class, focus on the past tense of both regular and irregular verbs. For the regular past tense, the -ed is pronounced as a /t/ after all voiceless consonant sounds: p, f, k, s, sh, ch, th (e.g. looked actually sounds like lookt). -ed sounds like /d/ if it's after voiced consonant sounds like b, v, g, z, j, th, l, m, n, r, and all vowel sounds (e.g. moved & played), but as a /Id/ after t and d sounds (painted & sounded). For irregular there aren't that many clear-cut rules, but focus on verbs that recur in each story like ran, said, gave, took (most of which you're pronouncing correctly already). Keep up the hard work and see you this weekend!

        Based on the transcript and comments, please generate similar feedback that is encouraging, specifies areas for improvement, and includes pronunciation tips.
        Your feedback should be between 50 and 100 words.
        """
    else:

        system_message = """
        As an assistant to an ESL teacher, your role is to help craft feedback for video assignments submitted by students aged 4 to 8.
        Use the video transcript and the teacher's comments to generate simple, constructive feedback. Aim to encourage the student,
        suggest specific areas for improvement, and offer pronunciation tips. The feedback should be easy for young learners to understand.
        Below are examples of feedback that balance positive reinforcement with actionable advice.
        """

        user_message = f"""
        Let's create feedback for a student's video.

        Teacher's Comments:
        {teacher_comments}

        Example Feedbacks:
        1. "Riding a bicycle" was perfectly said, and your explanation of activities was clear. Remember, using pronouns can make sentences shorter and conversations smoother. Great job, Jasper!
        2. Elsa, work on the "r" sound in "fork" to avoid confusion with other words. Your reading skills are impressive. Keep practicing!
        3. Great work, Lian! If possible, try reading the story a little bit more quickly and like the other kids in the class, focus on the past tense of both regular and irregular verbs. For the regular past tense, the -ed is pronounced as a /t/ after all voiceless consonant sounds: p, f, k, s, sh, ch, th (e.g. looked actually sounds like lookt). -ed sounds like /d/ if it's after voiced consonant sounds like b, v, g, z, j, th, l, m, n, r, and all vowel sounds (e.g. moved & played), but as a /Id/ after t and d sounds (painted & sounded). For irregular there aren't that many clear-cut rules, but focus on verbs that recur in each story like ran, said, gave, took (most of which you're pronouncing correctly already). Keep up the hard work and see you this weekend!

        Based on the teacher's comments, please generate similar feedback that is encouraging, specifies areas for improvement, and includes pronunciation tips.
        Don't copy anything from the example feedback.
        Your feedback should be between 50 and 100 words.
        """


    response = client.chat.completions.create(

    model=model,

    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ],
    max_tokens=145,
    temperature=temperature
    )
    return response.choices[0].message.content


def get_online_class_feedback(lesson_content, teacher_comments):

    if len(teacher_comments) < 35:
        return "Please add some more comments."

    random_number = np.random.randint(1, 10)
    temperature = random_number / 10
    model = "gpt-3.5-turbo"  # or model='gpt-4' based on preference
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI(api_key=api_key)

    system_message = f"""
    As an assistant to an ESL teacher, your role is to analyze the teacher's comments on a student's performance in an online class.
    Background Lesson Content:
    {lesson_content}
    Note: The feedback should not directly quote or rely heavily on the above lesson content but should focus on observations made by the teacher during the class.
    Remember, the students are primary ESL learners in China. Your language should be simple, clear, and tailored to encourage and guide the student based on the teacher's comments.
    Your feedback should include a summary of the student's performance, key areas for improvement, and specific pronunciation or grammar tips that could help the student.
    The goal is to provide constructive and personalized feedback that supports the student's learning journey, focusing on the teacher's observations rather than the predetermined lesson content.
    """

    user_message = f"""
    Teacher's Comments on the Student's Performance:
    {teacher_comments}

    Given these observations, generate feedback that focuses on encouraging the student, identifying areas for improvement, and offering specific advice to aid their learning. The feedback should be tailored to the student's needs as highlighted by the teacher, avoiding generic phrases or direct references to the lesson content.

    Aim for feedback that is engaging, supportive, and provides clear guidance for the student's progress. Your feedback should be concise, between 100-150 words.
    Remember to start with a brief summary of the content that was covered in the lesson in 2-3 sentences. E.g. Today we covered xyz.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        max_tokens=250,
        temperature=temperature
    )
    return response.choices[0].message.content

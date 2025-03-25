import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a Youtube Video Summarizer. You will be taking the transcript text and summarizing the entire video and provide important summary in points within 250 words. Please provide the summary of the text given here: """

## Fetch the transcript data from youtube videos

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text =YouTubeTranscriptApi.get_transcript(video_id)
        print(transcript_text)
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e

### getting the summary based on Prompt from Google Gemini AI Model

def get_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

### Setup the streamlit app

st.title("Acciojob YouTube Transcript Summarizer")
youtube_link = st.text_input("Enter the youtube video link: ")

if youtube_link:
    video_id = youtube_link.split("=")[1].split("&")[0]
    print(f"Exact video id=========={video_id}")
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    
if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary = get_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes: ")
        st.write(summary)
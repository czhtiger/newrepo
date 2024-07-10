import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import time
# from PyPDF2 import PdfReader
import openai
from openai import OpenAI, OpenAIError
from pathlib import Path
# from gtts import gTTS

try:
    os.mkdir("C:\\temp1")
except:
    pass


'# Multilingual Translate '

st.markdown(''' Please enter your text in English then I will translate to your selected language

 ''')

st.header('AI Translation')

text_need_be_translated = ""
language = st.selectbox(label='Language Selection',
                        options=("Chinese", "French", "Hindi", "Italian", "Korean", "Spanish"))


def extract_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text1 = ""
    for page in pdf_reader.pages:
        text1 += page.extract_text()
    return text1


def save_audio_stream(model: str, voice: str, input_text: str, file_path: str):
    """ Saves streamed audio data to a file, handling different OS path conventions. """
    # Construct the path object and validate the file extension
    path = Path(file_path)
    valid_formats = ['mp3', 'opus', 'aac', 'flac', 'wav', 'pcm']
    file_extension = path.suffix.lstrip('.').lower()

    if file_extension not in valid_formats:
        raise ValueError(f"Unsupported file format: {file_extension}. Please use one of {valid_formats}.")

   

    try:
        with client.audio.speech.with_streaming_response.create(
                model=model,
                voice=voice,
                input=input_text,
                response_format=file_extension
        ) as response:
            with open(path, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
    except OpenAIError as e:
        print(f"An error occurred while trying to fetch the audio stream: {e}")


st.write("You selected:", language)
input_option = st.selectbox("Please choose an input option", ["Enter text", "Upload a file"])

if input_option == "Enter text":
    text_need_be_translated = st.text_input("Please enter your text that need be translate, good luck")
    time.sleep(3)
    st.write("You want to translate ", text_need_be_translated)
else:
    uploaded_file = st.file_uploader("Choose a text or pdf file")
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text_need_be_translated = extract_pdf_text(uploaded_file)
        elif uploaded_file.type == "text/plain":
            text_need_be_translated = uploaded_file.read().decode()
        else:
            st.write("Unsupported file type")


def translate_text(text, dest_language):
    prompt = f"Translate the following English text to {dest_language} {text} "
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)
    translated_text1 = completion.choices[0].message.content
    print('Hello ', prompt, translated_text1)
    st.write(prompt, ' ', translated_text1)

    return translated_text1


def text_to_speech(text, language):
    tts = gTTS(text=text, lang=language)
    tts.save("audio.mp3")


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">{file_label}</a>'
    return href


submitButton = st.button('I want to Translate and Convert to Speech')

if len(text_need_be_translated) > 0 and submitButton:
    translated_text = translate_text(text_need_be_translated, language)

    file_path = "C:\\temp1\\audio.mp3"
    save_audio_stream(
        model="tts-1",
        voice="alloy",
        input_text=translated_text,
        file_path=file_path
    )
    print(file_path)
    audio_file = open(f"C:\\temp1\\audio.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Your audio:")
    st.audio(audio_bytes, format="C:\\temp1\\audio/mp3", start_time=0)

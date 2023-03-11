import gradio as gr
import speech_recognition as sr
import openai
import pyttsx3
from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key =  os.getenv("OPENAI_API_KEY")

messages=[
        {"role": "system", "content": "You are a teacher"}
    ]
def transcribe(audio):
    global messages
    file = open(audio, "rb")
    transcription = openai.Audio.transcribe("whisper-1", file)
    print(transcription)
    messages.append({"role": "user", "content": transcription["text"]})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    AImessage = response["choices"][0]["message"]["content"]
    engine = pyttsx3.init()
    engine.say(AImessage)
    engine.runAndWait()
    messages.append({"role": "assistant", "content": AImessage})
    chat = ''
    for message in messages:
        if message["role"] != 'system':
            chat += message["role"] + ':' + message["content"] + "\n\n"
    return chat


ui = gr.Interface(fn=transcribe ,inputs=gr.Audio(source='microphone',type='filepath'), outputs='text')

ui.launch()

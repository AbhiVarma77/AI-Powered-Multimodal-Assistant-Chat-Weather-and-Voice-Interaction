import os
import requests
import google.generativeai as genai
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import gradio as gr
import speech_recognition as sr
from gtts import gTTS
import tempfile

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = "821c7ee11e5e73e78c6e402e8911d392"  # Replace with actual API Key

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# AI Chatbot System Message
system_message = "You act like ChatGPT but powered by AI."

def stream_response(message, history):
    history_langchain_format = [SystemMessage(content=system_message)]
    
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    
    if message:
        history_langchain_format.append(HumanMessage(content=message))
        response = model.generate_content(message)
        return response.text

# Speech-to-Text Function
def speech_to_text(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Error connecting to speech recognition service."

# Convert AI's text response to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name  # Return file path

# Speech-to-Speech Processing
def speech_to_speech(audio):
    user_text = speech_to_text(audio)
    if "Sorry" in user_text or "Error" in user_text:
        return user_text, None  # Return error message, no audio

    ai_response = stream_response(user_text, [])  # Get AI's response
    audio_path = text_to_speech(ai_response)  # Convert to speech
    return ai_response, audio_path

# Gradio UI
def gradio_ui():
    with gr.Blocks(theme=gr.themes.Soft(), css="body { background-color: #1e1e1e; color: white; }") as demo:
        gr.Markdown("""<h1 style='text-align: center; color: #FFD700;'>AI Chatbot</h1>
                    <p style='text-align: center;'>Ask me anything, get weather updates, or use voice interaction!</p>""")
        
        choice = gr.Radio(["Chatbot", "Weather", "Speech-to-Speech"], label="Select Mode")
        weather_section = gr.Column(visible=False)
        chatbot_section = gr.Column(visible=False)
        speech_section = gr.Column(visible=False)

        with weather_section:
            city_input = gr.Textbox(placeholder="Enter city name for weather", label="City Name")
            weather_output = gr.Textbox(label="Weather Report")
            
            def fetch_weather(city):
                return generate_weather_report(city) if city else "Please enter a valid city."
            
            weather_button = gr.Button("Get Weather")
            weather_button.click(fetch_weather, inputs=city_input, outputs=weather_output)

        with chatbot_section:
            chatbot = gr.ChatInterface(fn=stream_response, type="messages")

        with speech_section:
            gr.Markdown("🎙️ **Ask your question by speaking, and AI will reply in voice!**")
            speech_input = gr.Audio(type="filepath", label="🎤 Speak here")
            text_output = gr.Textbox(label="AI Response (Text)")
            audio_output = gr.Audio(label="AI Response (Speech)")

            speech_button = gr.Button("Get AI Response")
            speech_button.click(speech_to_speech, inputs=speech_input, outputs=[text_output, audio_output])

        def update_visibility(selected):
            return (
                gr.update(visible=(selected == "Weather")),
                gr.update(visible=(selected == "Chatbot")),
                gr.update(visible=(selected == "Speech-to-Speech"))
            )

        choice.change(update_visibility, inputs=choice, outputs=[weather_section, chatbot_section, speech_section])

    demo.launch(share=True)

# Run Gradio UI
if __name__ == "__main__":
    gradio_ui()

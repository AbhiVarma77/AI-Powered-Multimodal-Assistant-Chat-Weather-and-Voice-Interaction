import os
import re
import requests
import urllib.parse  # To encode URLs
import google.generativeai as genai
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import gradio as gr

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = "821c7ee11e5e73e78c6e402e8911d392"  # Replace with actual API Key

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# Function to fetch weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    else:
        return {"error": "City not found!"}

# Function to generate weather insights using Gemini AI
def generate_weather_report(city):
    weather_data = get_weather(city)
    
    if "error" in weather_data:
        return weather_data["error"]
    
    prompt = f"""Generate a detailed weather forecast for {city} based on the following data:
    - Temperature: {weather_data['temperature']}°C
    - Weather Condition: {weather_data['weather']}
    - Humidity: {weather_data['humidity']}%
    - Wind Speed: {weather_data['wind_speed']} km/h
    Provide recommendations based on the forecast (e.g., safety precautions)."""
    
    response = model.generate_content(prompt)
    return response.text

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

# Gradio UI with Sidebar
def gradio_ui():
    with gr.Blocks(theme=gr.themes.Soft(), css="body { background-color: #1e1e1e; color: white; }") as demo:
        gr.Markdown("""<h1 style='text-align: center; color: #FFD700;'>AI Chatbot</h1>
                    <p style='text-align: center;'>Ask me anything or get weather updates!</p>""")
        
        choice = gr.Radio(["Chatbot", "Weather"], label="Select Mode")
        weather_section = gr.Column(visible=False)
        chatbot_section = gr.Column(visible=False)
        
        with weather_section:
            city_input = gr.Textbox(placeholder="Enter city name for weather", label="City Name")
            weather_output = gr.Textbox(label="Weather Report")
            
            def fetch_weather(city):
                if city:
                    return generate_weather_report(city)
                return "Please enter a valid city."
            
            weather_button = gr.Button("Get Weather")
            weather_button.click(fetch_weather, inputs=city_input, outputs=weather_output)
        
        with chatbot_section:
            chatbot = gr.ChatInterface(fn=stream_response,
                                       textbox=gr.Textbox(placeholder="Type your message...",
                                                          show_label=False,
                                                          autofocus=True,
                                                          container=False))
        
        def update_visibility(selected):
            if selected == "Weather":
                return gr.update(visible=True), gr.update(visible=False)
            elif selected == "Chatbot":
                return gr.update(visible=False), gr.update(visible=True)
            else:
                return gr.update(visible=False), gr.update(visible=False)
        
        choice.change(update_visibility, inputs=choice, outputs=[weather_section, chatbot_section])
    
    demo.launch(share=True)

# Run Gradio UI
if __name__ == "__main__":
    gradio_ui()

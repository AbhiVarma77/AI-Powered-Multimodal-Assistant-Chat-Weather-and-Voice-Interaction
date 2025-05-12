import gradio as gr
import requests
import json
import google.generativeai as genai


# API setup
OPENWEATHER_API_KEY = "821c7ee11e5e73e78c6e402e8911d392"
GEMINI_API_KEY = "AIzaSyDsQxl5G9u5N8YPxJsopJbTM_a71aCRDgU"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")


def detect_weather_intent(message):
    """Detects if a message is asking about weather."""
    weather_keywords = [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "sunny",
        "cloudy",
        "humidity",
        "precipitation",
        "weather in",
        "what's the weather",
    ]

    message_lower = message.lower()
    for keyword in weather_keywords:
        if keyword in message_lower:
            # Extract city name - this is a simplified approach
            # In a production system, use NER or similar techniques
            if "in" in message_lower:
                parts = message_lower.split("in")
                if len(parts) > 1:
                    city = parts[1].strip().split()[0]
                    return True, city
            return True, None
    return False, None


def get_weather(city):
    """Get weather data for a city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    else:
        return None, f"Error retrieving weather data: {response.status_code}"


def format_weather_response(weather_data):
    """Format weather data into a readable response."""
    location = weather_data["location"]
    temp = weather_data["temperature"]
    condition = weather_data["condition"]
    humidity = weather_data["humidity"]
    wind = weather_data["wind"]

    response = f"Weather in {location}: {condition} with a temperature of {temp}. "
    response += f"Humidity is {humidity} and wind speed is {wind}."

    # Add forecast summary
    response += "\n\nForecast for the next 3 days:"
    for day in weather_data["forecast"][:3]:
        date = day["date"]
        min_temp = day["day"]["mintemp_c"]
        max_temp = day["day"]["maxtemp_c"]
        condition = day["day"]["condition"]["text"]
        response += f"\n- {date}: {condition}, {min_temp}°C to {max_temp}°C"

    return response


def process_message(message, history):
    """Process user message and decide whether to use weather API or chatbot."""
    is_weather_query, city = detect_weather_intent(message)

    if is_weather_query:
        weather_data = get_weather(city)

        if "error" in weather_data:
            return weather_data["error"]

        prompt = f"""Generate a detailed weather forecast for {city} based on the following data:
        - Temperature: {weather_data["temperature"]}°C
        - Weather Condition: {weather_data["weather"]}
        - Humidity: {weather_data["humidity"]}%
        - Wind Speed: {weather_data["wind_speed"]} km/h
        Provide recommendations based on the forecast (e.g., safety precautions)."""

        response = model.generate_content(prompt)
        return response.text

    # For non-weather queries, use Gemini
    chat_response = model.generate_content(message).text
    return chat_response


# Gradio Interface
with gr.Blocks() as app:
    chatbot = gr.Chatbot(height=500)
    msg = gr.Textbox(label="Message")
    clear = gr.Button("Clear")

    def user(message, history):
        return "", history + [[message, None]]

    def bot(history):
        bot_message = process_message(history[-1][0], history[:-1])
        history[-1][1] = bot_message
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    app.launch()

# AI Chatbot & Weather Forecasting App

## Overview
This project is a **multi-functional AI-powered application** that provides:
- **AI Chatbot**: Interact with an AI chatbot powered by Google's Gemini API.
- **Weather Forecasting**: Get real-time weather updates and AI-generated insights based on OpenWeather API data.

The application is built using **Python, Gradio, and Google Gemini AI**, providing a user-friendly interface for chatting and checking weather reports.

## Features
✅ **Chatbot Mode**: Engage in natural conversations with the AI-powered chatbot.
✅ **Weather Mode**: Get live weather data and AI-generated insights for any city.
✅ **Interactive UI**: Built with Gradio, offering a sleek and responsive experience.
✅ **Real-time API Calls**: Fetches data from OpenWeather API for accurate weather updates.
✅ **AI-Powered Insights**: Uses Gemini AI to generate weather reports with recommendations.

## Technologies Used
- **Python**
- **Gradio** (UI Framework)
- **Google Gemini AI** (for chatbot & insights)
- **OpenWeather API** (for weather data)
- **Requests** (for making API calls)
- **LangChain** (for chatbot memory handling)

## Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/ai-chatbot-weather.git
cd ai-chatbot-weather
```

### 2️⃣ Install Dependencies
Ensure you have Python installed, then run:
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up API Keys
- Create a `.env` file and add your **Gemini API Key**:
  ```env
  GEMINI_API_KEY=your_google_gemini_api_key
  ```
- Replace the **OpenWeather API Key** in the code with your own key.

### 4️⃣ Run the Application
```sh
python app.py
```

The application will launch, and you can access it in your browser.

## Usage
- **Select a mode**: Chatbot or Weather.
- **Chatbot Mode**: Type messages and interact with the AI.
- **Weather Mode**: Enter a city name to get weather details and AI insights.

## Example Outputs
**Chatbot Mode:**
```
User: What is the capital of France?
AI: The capital of France is Paris.
```

**Weather Mode:**
```
City: New York
Temperature: 20°C
Weather: Cloudy
Humidity: 65%
Wind Speed: 10 km/h

AI Insight: It’s cloudy today in New York. Carry an umbrella just in case!
```

## Deployment
To deploy the application online, use **Gradio's share feature**:
- Run the script and find the **public Gradio URL**.
- Share it with others to access the chatbot and weather app online.

## Future Enhancements
- ✅ Improve chatbot's memory & conversation flow.
- ✅ Add more AI-driven weather predictions.
- ✅ Enhance UI with custom themes and animations.





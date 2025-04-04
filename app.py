from dotenv import load_dotenv
import os
import gradio as gr
import google.generativeai as genai
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("The GEMINI_API_KEY environment variable is not set")

# Configure Gemini AI (Google Generative AI)
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")


# System message
system_message = "You act like ChatGPT but powered by Gemini AI."

def stream_response(message, history):
    history_langchain_format = [SystemMessage(content=system_message)]
    
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    
    if message:
        history_langchain_format.append(HumanMessage(content=message))
        partial_message = ""
        response = model.generate_content(message)
        partial_message += response.text
        return partial_message

# Define the UI
with gr.Blocks(theme=gr.themes.Soft(), css="body { background-color: #1e1e1e; color: white; }") as demo:
    gr.Markdown("""<h1 style='text-align: center; color: #FFD700;'>Gemini AI Chat Assistant</h1>
                <p style='text-align: center;'>Ask me anything you want?</p>""")
    
    chatbot = gr.ChatInterface(fn=stream_response,
                               textbox=gr.Textbox(placeholder="Type your message...",
                                                  show_label=False,
                                                  autofocus=True,
                                                  container=False))

# Launch the Gradio app
demo.launch(share=True)

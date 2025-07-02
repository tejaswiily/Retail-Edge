from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()  # Load environment variables

# API Key Check
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found! Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)

# Streamlit Config
st.set_page_config(page_title="Retail Q&A Bot", page_icon=":robot_face:", layout="wide")

# Add custom CSS styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
    }
    .stTextInput>div>input {
        font-size: 16px;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.header("Welcome to the **Retail Edge Bot**!")

# Function to get Gemini response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize session state for chat history if not already done
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User Input Section
input = st.text_input("Enter your question:", key="input", placeholder="Type here...")
submit = st.button("Ask the Retail Bot")

# Sidebar: Chat History Display
with st.sidebar:
    st.subheader("Conversation History:")
    for role, text in st.session_state['chat_history']:
        st.write(f"**{role}:** {text}")

# Main Conversation
if submit and input:
    with st.spinner('Bot is thinking...'):
        response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    for chunk in response:
        st.session_state['chat_history'].append(("Bot", chunk.text))
    st.subheader("Bot's Response")
    for chunk in response:
        st.write(chunk.text)

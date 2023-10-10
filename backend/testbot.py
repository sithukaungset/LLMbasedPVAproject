import streamlit as st
import requests
from typing import Dict, List
import pandas as pd
import requests 
import streamlit as st
# ... [Other necessary imports]

API_URL = "http://localhost:8000/chat_response"

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "sender": "bot",
                "message": "Hello! I'm your Meeting Room Booking Bot. How can I assist you today? (e.g., 'Book a room', 'Cancel a booking', etc.)"
            }
        ]

def get_bot_response(user_message: str) -> str:
    data = {"user_message": user_message}
    response = requests.post(API_URL, json=data)
    return response.json()["bot_response"]

def main():
    st.title("Meeting Room Booking Chatbot")

    init_session_state()  

    # Display previous chat messages
    for message in st.session_state.messages:
        st.write(f"**{message['sender']}**: {message['message']}")

    st.markdown("---")

    user_input = st.text_input("You:")

    if user_input:
        st.session_state.messages.append({"sender": "user", "message": user_input})
        
        # Get bot's response from the API
        bot_response = get_bot_response(user_input)
        
        st.session_state.messages.append({"sender": "bot", "message": bot_response})
        st.text_input("You:", value="", key="reset")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()

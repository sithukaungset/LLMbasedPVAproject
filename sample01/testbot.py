import streamlit as st
import requests
from typing import Dict, List
import pandas as pd
import requests 
import streamlit as st
# ... [Other necessary imports]

API_URL = "http://localhost:8000/writer"

# These constants are not relevant for a meeting room bot, so we can remove them:
# DEFAULT_BOT, DEFAULT_CHARACTERS, DEFAULT_NEWS_TEXT

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "sender": "bot",
                "message": "Hello! I'm your Meeting Room Booking Bot. How can I assist you today? (e.g., 'Book a room', 'Cancel a booking', etc.)"
            }
        ]


def main():
    st.title("Meeting Room Booking Chatbot")

    init_session_state()  # Ensure this is called at the beginning of main

    # Display previous chat messages
    for message in st.session_state.messages:
        st.write(f"**{message['sender']}**: {message['message']}")

    st.markdown("---")

    user_input = st.text_input("You:")

    if user_input:
        st.session_state.messages.append({
            "sender": "user",
            "message": user_input
        })

        # Here, you should add logic or API calls to generate the bot's response based on the user_input
        # For simplicity, I'm just going to echo back the user's message:
        bot_response = f"You said '{user_input}'. Let me process that."

        st.session_state.messages.append({
            "sender": "bot",
            "message": bot_response
        })

        st.text_input("You:", value="", key="reset")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()

from typing import Dict, List
import pandas as pd
import requests
import streamlit as st

API_URL = "http://localhost:8000/chat_response"

DEFAULT_BOT = "Meeting Bot"

def generate_bot_prompt(user_input: str, meeting_date: str, meeting_time: str, duration: str, participants: str, meeting_info: str) -> str:
    prompt = f"""[User Request]
{user_input}

[Meeting Information]
Date: {meeting_date}
Time: {meeting_time}
Duration: {duration} hours
Participants: {participants}

[Room Data]
{meeting_info}

Based on the information provided, please assist the user with booking, modifying, or canceling meeting rooms.
"""
    return prompt

def request_writer_api(
    user_query: str, 
    meeting_date: str, 
    meeting_time: str, 
    duration: str, 
    participants: str, 
    meeting_info: str) -> str:
    structured_prompt = generate_bot_prompt(user_query, meeting_date, meeting_time, duration, participants, meeting_info)
    try:
        resp = requests.post(
            API_URL,
            json={
                "user_input": structured_prompt,
   
             }

        )
        resp.raise_for_status()
        return resp.json().get("results", "Sorry, I couldn't process that request.")
    except requests.RequestException as e:
        return f"There was an error: {str(e)}"



def init_session_state():
    st.session_state.setdefault("result", "")
    st.session_state.setdefault("user_query", "")

def input_step1_ui():
    st.subheader("Select Bot")
    bots = {
        "Meeting room bot": {"purpose": "booking, modifying, or canceling meeting rooms"},
        "Parking booking bot": {"purpose": "reserving parking slots"},
        "Cafe bot": {"purpose": "ordering coffee or snacks"},
        "IT Helpdesk bot": {"purpose": "resolving IT-related issues"},
        "Smart toilet bot": {"purpose": "checking toilet availability and cleanliness status"}
    }
    st.session_state.bot = st.selectbox("Select a bot:", bots)


def input_user_query_ui():
    st.subheader("Enter Your Query")
    user_query = st.text_input("Please type your query regarding meeting rooms:")
    meeting_date = st.date_input("Meeting Date:")
    meeting_time = st.time_input("Meeting Time:")
    duration = st.text_input("Duration (in hours):")
    participants = st.text_input("Participants (comma-separated):")
    meeting_info = st.text_area("Room Data:")

    if user_query:  # Check if the user has entered a query
        response = request_writer_api(user_query, meeting_date, meeting_time, duration, participants, meeting_info)
        st.write(response)  # Displaying the response on Streamlit
    
    return user_query, meeting_date, meeting_time, duration, participants, meeting_info



def upload_meeting_data():
    uploaded_file = st.file_uploader("Upload Meeting Room Data (Excel format)", type=["xlsx"])
    if uploaded_file:
        meeting_data_df = pd.read_excel(uploaded_file)
        st.write(meeting_data_df.columns)
        return meeting_data_df
    return None


def input_step3_ui():
    st.subheader("Provide data via excel sheet")

    meeting_data_df = upload_meeting_data()

    if meeting_data_df is not None:
        st.session_state.meeting_data_df = meeting_data_df


def result_ui():
    st.subheader("Chat Session")

    chat_container_style = """
    background-color: #2f2f2f;
    border: 1px solid #3e3e3e;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    """

    user_message_style = """
    display: inline-block;
    background-color: #4a4a4a;
    color: #e1ffc7;
    border-radius: 8px;
    padding: 8px 10px;
    margin: 2px 0;
    max-width: 80%;
    """

    bot_message_style = """
    display: inline-block;
    background-color: #1a1a1a;
    color: #e2e2e2;
    border-radius: 8px;
    padding: 8px 10px;
    margin: 2px 0;
    max-width: 80%;
    """

    st.markdown(f"<div style='{chat_container_style}'>", unsafe_allow_html=True)

    if st.session_state.user_query:
        st.markdown(f"<div style='{user_message_style}'>You: {st.session_state.user_query}</div>", unsafe_allow_html=True)

    if st.session_state.result:
        st.markdown(f"<div style='{bot_message_style}'>Meeting Bot: {st.session_state.result}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    st.title("Megazone Meeting Room GPT")

    init_session_state()

    col1, col3 = st.columns([1, 1])

    with col1:
        input_step1_ui()
    with col3:
        input_step3_ui()

    st.markdown("---")
    result_ui()

    user_query, meeting_date, meeting_time, duration, participants, meeting_info = input_user_query_ui()

    if user_query:
        structured_prompt = generate_bot_prompt(
            user_input=user_query,
            meeting_date=str(meeting_date),
            meeting_time=str(meeting_time),
            duration=duration,
            participants=participants,
            meeting_info=meeting_info
        )

        # if not st.session_state.user_query or structured_prompt != st.session_state.user_query:
        #     st.session_state.user_query = structured_prompt
        #     st.session_state.result = request_writer_api(prompt=st.session_state.user_query)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()

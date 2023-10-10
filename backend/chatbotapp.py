from typing import Dict, List
import pandas as pd
import requests
import streamlit as st

API_URL = "http://localhost:8000/chat_response"

DEFAULT_BOT = "Meeting Bot"


def request_writer_api(user_input: str) -> str:
    try:
        resp = requests.post(
            API_URL,
            json={"user_input": user_input},
            timeout=10
        )
        resp.raise_for_status()
        return resp.json().get("results", "Sorry, I couldn't process that request.")
    except requests.RequestException:
        return "There was an error communicating with the server."


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
    return user_query


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

    user_query = input_user_query_ui()

    if user_query and (not st.session_state.user_query or user_query != st.session_state.user_query):
        st.session_state.user_query = user_query

        st.session_state.result = request_writer_api(user_input=st.session_state.user_query)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()

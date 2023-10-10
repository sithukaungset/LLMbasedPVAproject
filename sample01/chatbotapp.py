from typing import Dict, List
import pandas as pd
import requests 
import streamlit as st

API_URL = "http://localhost:8000/meeting"

DEFAULT_BOT = "Meeting Bot"
DEFAULT_CHARACTERS = [
    {"name": "James", "characteristics": "An ambitious businessman"},
    {"name": "Kong", "characteristics": "A renowned doctor working at a biological research institute; in a romantic relationship with James"},
    {"name": "Bab", "characteristics": "A jealous competitor company's CEO"},
]
DEFAULT_NEWS_TEXT = """Oil prices continue to drop... Gasoline down by 6.6 won·Diesel by 5.9 won↓. This week, local gas stations also saw a simultaneous decrease in gasoline and diesel selling prices.
According to the Korea Petroleum Corporation's price information system, Opinet, the average selling price of gasoline at national gas stations in the third week of June was recorded at 1,575.8 won per liter, a decrease of 6.6 won from the previous week.
The selling price of diesel was also tallied at 1,387.6 won, down by 8.7 won.
Gasoline prices have been dropping for 8 consecutive weeks, while diesel prices have been on a decline for 9 weeks in a row.
An official from the Korea Petroleum Association predicted, "Next week, gasoline and diesel prices will show a downward stabilization, but especially from the week after, there's a possibility that diesel prices might rebound."""

def request_writer_api(
    genre: str,
    characters: List[Dict[str, str]],
    news_text: str,
) -> str:
    resp = requests.post(
        API_URL,
        json={
            "genre": genre,
            "characters": characters,
            "news_text": news_text,
        },
    )
    resp = resp.json()
    return resp["results"]


def init_session_state():
    if "genre" not in st.session_state:
        st.session_state.genre = DEFAULT_BOT
    if "characters" not in st.session_state:
        st.session_state.characters = DEFAULT_CHARACTERS
    if "news_text" not in st.session_state:
        st.session_state.news_text = DEFAULT_NEWS_TEXT
    if "result" not in st.session_state:
        st.session_state.result = ""


def input_step1_ui():
    # Step 1: Select bot type
    st.subheader("Step 1: Select Bot")
    bots = [
        "Meeting room bot",
        "Fantasy",
        "Sci-Fi",
        "Mystery",
        "Romance",
    ]
    st.session_state.genre = st.selectbox("Select a bot:", bots)


def input_step2_ui():
    # Step 2: Add Characters
    st.subheader("Step 2: Add Characters")

    character_name = st.text_input("Name")
    character_characteristics = st.text_input("Characteristics")

    if st.button("Add Character"):
        st.session_state.characters.append(
            {
                "name": character_name,
                "characteristics": character_characteristics,
            }
        )

# This new function allows uploading of Excel files and returns them as DataFrames

def upload_meeting_data():
    uploaded_file = st.file_uploader("Upload Meeting Room Data (Excel format)", type=["xlsx"])
    if uploaded_file:
        meeting_data_df = pd.read_excel(uploaded_file)
        st.write(meeting_data_df) # Display the uploaded data (optional)
        return meeting_data_df
    return None

# Adjust this function to pass meeting room data to the chatbot
def input_step3_ui():
    # Step 3: Add News Article
    st.subheader("Step 3: Add News Article") 
    news_text = st.text_area(
        "Paste the news article here", value=st.session_state.news_text
    )
    st.session_state.news_text = news_text

    # Upload and process the Excel file
    meeting_data_df = upload_meeting_data()
    
    # Convert the uploaded meeting data to a string format (or any other format your chatbot can use)
    if meeting_data_df is not None:
        meeting_info_str = "\n".join([f"{row['Room Name']}: {row['Status']}" for _, row in meeting_data_df.iterrows()])
    else:
        meeting_info_str = ""

    if st.button("Begin!"):
        # You'll have to adjust request_writer_api to accept and process meeting_info_str
        st.session_state.result = request_writer_api(
            genre=st.session_state.genre,
            characters=st.session_state.characters,
            news_text=st.session_state.news_text,
            # Add the meeting_info here 
            meeting_info=meeting_info_str
        )

def characters_ui():
    st.subheader("Added Characters")

    placeholder = st.empty()
    character_list = []
    for character in st.session_state.characters:
        name, characteristics = character.values()
        character_list.append(f"[{name}]\n{characteristics}")
    placeholder.text("\n".join(character_list))

    # Add a 'Reset' button to reset the characters
    if st.button("Reset"):
        placeholder.empty()
        st.session_state.characters = []
        st.success("Characters have been reset.")


def result_ui():
    st.subheader("Result")
    st.text_area("Your Meeting Room info", st.session_state.result, height=600)


def main():
    st.title("[Part 06] Writer GPT")

    init_session_state()

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        input_step1_ui()
    with col2:
        input_step2_ui()
    with col3:
        input_step3_ui()

    st.markdown("---")
    characters_ui()

    st.markdown("---")
    result_ui()

def main():
    st.title("Megazone Meeting Room GPT")

    init_session_state()

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        input_step1_ui()
    with col2:
        input_step2_ui()
    with col3:
        input_step3_ui()

    st.markdown("---")
    characters_ui()

    st.markdown("---")
    result_ui()

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
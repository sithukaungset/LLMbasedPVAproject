from pprint import pprint
from typing import Dict, List
from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from pydantic import BaseModel
import openai
from langchain.chat_models import AzureChatOpenAI
import re  # You'll use regular expressions to parse the data
from typing import Dict

load_dotenv()

# Load environment variables
OPENAI_API_KEY = "824fe43e851f4862af326fa83c3d3cfe"
OPENAI_API_BASE = "https://mtcaichat01.openai.azure.com"
OPENAI_DEPLOYMENT_VERSION = "2023-03-15-preview"
OPENAI_DEPLOYMENT_NAME = "gpt432k"
OPENAI_MODEL_NAME = "gpt4"
OPENAI_EMBEDDING_DEPLOYMENT_NAME = "embeddingada002"
OPENAI_EMBEDDING_MODEL_NAME = "text-embedding-ada-002"

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str

def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r", encoding='utf-8') as f:
        prompt_template = f.read()

    return prompt_template

def extract_data_from_prompt(prompt: str) -> Dict[str, str]:
    # Extract meeting_date
    date_match = re.search(r"Date: (\d{4}-\d{2}-\d{2})", prompt)
    meeting_date = date_match.group(1) if date_match else None

    # Extract meeting_time
    time_match = re.search(r"Time: ([\d:]+ [APMapm]{2})", prompt)
    meeting_time = time_match.group(1) if time_match else None

    # Extract duration
    duration_match = re.search(r"Duration: (\d+) hours", prompt)
    duration = duration_match.group(1) if duration_match else None

    # Extract participants
    participants_match = re.search(r"Participants: ([\w\s,]+)", prompt)
    participants = participants_match.group(1) if participants_match else None

    # Extract Room Data
    # This is a bit tricky because we don't know the exact format. I'll assume it's the last line for now.
    room_data_match = re.search(r"\[Room Data\]\n(.+)", prompt)
    room_data = room_data_match.group(1) if room_data_match else None

    return {
        "meeting_date": meeting_date,
        "meeting_time": meeting_time,
        "duration": duration,
        "participants": participants,
        "meeting_info": room_data  # As it's a string, you might need to process it further to convert it to a dictionary
    }

@app.post("/chat_response")
def get_bot_response(req: ChatRequest):

    data = extract_data_from_prompt(req.user_input)

    llm = AzureChatOpenAI(
        deployment_name=OPENAI_DEPLOYMENT_NAME,
        model_name=OPENAI_MODEL_NAME,
        openai_api_base=OPENAI_API_BASE,
        openai_api_version=OPENAI_DEPLOYMENT_VERSION,
        openai_api_key=OPENAI_API_KEY
    )

    prompt_template = ChatPromptTemplate.from_template(
        template=read_prompt_template("bot_template.txt")

    )

    chain = LLMChain( llm =llm, prompt=prompt_template,output_key="output" )
    # Send the prompt to the chat model
    
    # response = chain(req.dict())

    # Pass the extracted data to the chain
    response = chain({
        "user_input": req.user_input,
        "meeting_date": data["meeting_date"],
        "meeting_time": data["meeting_time"],
        "duration": data["duration"],
        "participants": data["participants"],
        "meeting_info": data["meeting_info"]
    })
    print("Response from OpenAI:", response)

    return {"bot_response": response["output"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

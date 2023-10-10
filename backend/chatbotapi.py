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
    meeting_info: Dict[str, str]

def generate_prompt(user_input: str, meeting_info: Dict[str, str]) -> str:
    """Generate a structured prompt for the chat model."""
    meeting_info_str = "\n".join([f"{room_name}: {status}" for room_name, status in meeting_info.items()])

    prompt = (
        f"<USER_QUERY>\n{user_input}\n</USER_QUERY>\n"
        f"Meeting Room Info:\n{meeting_info_str}\n"
        "Based on the <USER_QUERY>, help the user with booking, modifying, or canceling meeting rooms."
    )

    return prompt

@app.post("/chat_response")
def get_bot_response(req: ChatRequest, request: Request):

    llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
        model_name=OPENAI_MODEL_NAME,
        openai_api_base=OPENAI_API_BASE,
        openai_api_version=OPENAI_DEPLOYMENT_VERSION,
        openai_api_key=OPENAI_API_KEY)

    # Generate the prompt
    prompt = generate_prompt(
        user_input=req.user_input,
        meeting_info=req.meeting_info
    )

    # Send the prompt to the chat model
    response = llm(prompt)

    # Extract the chatbot's response from the result.
    bot_response = response.get("output", "Sorry, I couldn't process that.")

    return {"bot_response": bot_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

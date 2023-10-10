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
    meeting_date: str
    meeting_time: str
    duration: str
    participants: str
    meeting_info: Dict[str, str]

def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r", encoding='utf-8') as f:
        prompt_template = f.read()

    return prompt_template


@app.post("/chat_response")
def get_bot_response(req: ChatRequest):

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
    
    response = chain(req.dict())

    return {"bot_response": response["output"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

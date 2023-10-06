from pprint import pprint
from typing import Dict, List

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
 
class UserRequest(BaseModel):
    genre: str
    characters: List[Dict[str, str]]
    news_text: str


def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r", encoding='utf-8') as f:
        prompt_template = f.read()

    return prompt_template


@app.post("/writer")
def generate_novel(req: UserRequest) -> Dict[str, str]:

    # Initialize Azure OpenAI
    openai.api_type = "azure"
    openai.api_version = OPENAI_DEPLOYMENT_VERSION
    openai.api_base = OPENAI_API_BASE
    openai.api_key = OPENAI_API_KEY

    # Initialize AzureChatOpenAI and OpenAIEmbeddings

    # writer_llm = AzureChatOpenAI(temperature=0.1, max_tokens=500, model="gpt-3.5-turbo")
    writer_llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
        model_name=OPENAI_MODEL_NAME,
        openai_api_base=OPENAI_API_BASE,
        openai_api_version=OPENAI_DEPLOYMENT_VERSION,
        openai_api_key=OPENAI_API_KEY)

    writer_prompt_template = ChatPromptTemplate.from_template(
        template=read_prompt_template("prompt_template.txt")
    )
    writer_chain = LLMChain(
        llm=writer_llm, prompt=writer_prompt_template, output_key="output"
    )

    result = writer_chain(req.dict())

    return {"results": result["output"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

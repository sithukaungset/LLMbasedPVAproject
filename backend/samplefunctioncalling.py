from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os
from langchain import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains.openai_functions import create_structured_output_chain
import logging

# Load environment variables
OPENAI_API_KEY = "824fe43e851f4862af326fa83c3d3cfe"
OPENAI_API_BASE = "https://mtcaichat01.openai.azure.com"
OPENAI_DEPLOYMENT_VERSION = "2023-03-15-preview"
OPENAI_DEPLOYMENT_NAME = "gpt432k"
OPENAI_MODEL_NAME = "gpt4"  
OPENAI_EMBEDDING_DEPLOYMENT_NAME = "embeddingada002"
OPENAI_EMBEDDING_MODEL_NAME = "text-embedding-ada-002" 


# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str

class Person(BaseModel):
    """Identifying information about a person."""
    name: str = Field(..., description="The person's name")
    age: int = Field(..., description="The person's age")
    fav_food: Optional[str] = Field(None, description="The person's favorite food")

def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r", encoding='utf-8') as f:
        return f.read()

@app.post("/chat_response")
def get_bot_response(req: ChatRequest):
    try:
        # Load environment variables
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
        OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")
        OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
        OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
        
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

        # Create a chain that uses the Person Pydantic class to extract structured information
        chain = create_structured_output_chain(Person, llm, prompt_template, verbose=True)
        response = chain(req.user_input)
        return {"bot_response": response}
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

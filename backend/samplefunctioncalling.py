from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os
from langchain import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts
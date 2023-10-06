import os

from dotenv import load_dotenv
from langchain.chains import LLMChain
#from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import openai 
from langchain.chat_models import AzureChatOpenAI

load_dotenv()
# Load environment variables
# OPENAI_API_KEY = "824fe43e851f4862af326fa83c3d3cfe"
# OPENAI_API_BASE = "https://mtcaichat01.openai.azure.com"
# OPENAI_DEPLOYMENT_VERSION = "2023-03-15-preview"
# OPENAI_DEPLOYMENT_NAME = "gpt432k"
# OPENAI_MODEL_NAME = "gpt4"  
# OPENAI_EMBEDDING_DEPLOYMENT_NAME = "embeddingada002"
# OPENAI_EMBEDDING_MODEL_NAME = "text-embedding-ada-002" 


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
BUG_STEP1_PROMPT_TEMPLATE = os.path.join(CUR_DIR, "prompt_templates", "bug_analyze.txt")
BUG_STEP2_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "bug_solution.txt"
)
ENHANCE_STEP1_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "enhancement_say_thanks.txt"
)
DEFAULT_RESPONSE_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "default_response.txt"
)
INTENT_PROMPT_TEMPLATE = os.path.join(CUR_DIR, "prompt_templates", "parse_intent.txt")

SEARCH_VALUE_CHECK_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "search_value_check.txt"
)
SEARCH_COMPRESSION_PROMPT_TEMPLATE = os.path.join(
    CUR_DIR, "prompt_templates", "search_compress.txt"
)


def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()

    return prompt_template


chat_file = os.path.join(CUR_DIR, "hist.json")


def create_chain(llm, template_path, output_key):


    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            template=read_prompt_template(template_path)
        ),
        output_key=output_key,
        verbose=True,
    )

# Initialize Azure OpenAI
openai.api_type = "azure"
openai.api_version = OPENAI_DEPLOYMENT_VERSION
openai.api_base = OPENAI_API_BASE
openai.api_key = OPENAI_API_KEY

llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
        model_name=OPENAI_MODEL_NAME,
        openai_api_base=OPENAI_API_BASE,
        openai_api_version=OPENAI_DEPLOYMENT_VERSION,
        openai_api_key=OPENAI_API_KEY)

bug_step1_chain = create_chain(
    llm=llm,
    template_path=BUG_STEP1_PROMPT_TEMPLATE,
    output_key="bug_analysis",
)
bug_step2_chain = create_chain(
    llm=llm,
    template_path=BUG_STEP2_PROMPT_TEMPLATE,
    output_key="output",
)
enhance_step1_chain = create_chain(
    llm=llm,
    template_path=ENHANCE_STEP1_PROMPT_TEMPLATE,
    output_key="output",
)
parse_intent_chain = create_chain(
    llm=llm,
    template_path=INTENT_PROMPT_TEMPLATE,
    output_key="intent",
)
default_chain = create_chain(
    llm=llm, template_path=DEFAULT_RESPONSE_PROMPT_TEMPLATE, output_key="output"
)

search_value_check_chain = create_chain(
    llm=llm,
    template_path=SEARCH_VALUE_CHECK_PROMPT_TEMPLATE,
    output_key="output",
)
search_compression_chain = create_chain(
    llm=llm,
    template_path=SEARCH_COMPRESSION_PROMPT_TEMPLATE,
    output_key="output",
)

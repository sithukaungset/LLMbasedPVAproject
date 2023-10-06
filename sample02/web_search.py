import os

from chains import search_compression_chain, search_value_check_chain
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

load_dotenv()

search = GoogleSearchAPIWrapper(
    google_api_key="AIzaSyA9fzqzVNNfCwnCI8mfjTkv1N3MQiruby0",
    google_cse_id="96b33e57d360c48c5"
)

search_tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=search.run,
)


def query_web_search(user_message: str) -> str:
    context = {"user_message": user_message}
    context["related_web_search_results"] = search_tool.run(user_message)

    has_value = search_value_check_chain.run(context)

    print(has_value)
    if has_value == "Y":
        return search_compression_chain.run(context)
    else:
        return ""

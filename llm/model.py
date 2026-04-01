from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from config.hawkeye import set_openai_token, get_openai_base_url

# Fetch token and set OPENAI_API_KEY / OPENAI_API_BASE env vars
set_openai_token()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    openai_api_base=get_openai_base_url(),
)


def call_llm(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content
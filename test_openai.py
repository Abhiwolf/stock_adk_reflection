"""
Quick standalone script to test OpenAI model connectivity via Hawkeye.
Usage:  python test_openai.py
"""

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from config.hawkeye import set_openai_token, get_openai_base_url

# 1. Fetch OAuth token and configure env vars
print("=" * 60)
print("Setting up OpenAI token via Hawkeye...")
set_openai_token()

# 2. Initialise the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    openai_api_base=get_openai_base_url(),
)

# 3. Send a test prompt
prompt = "Explain in 2-3 sentences what a stock P/E ratio is."
print("=" * 60)
print(f"Prompt : {prompt}")
print("=" * 60)

response = llm.invoke(prompt)
print(f"Response:\n{response.content}")
print("=" * 60)
print("OpenAI model test completed successfully.")

import json
import os
import requests

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# OpenAI-specific Hawkeye config (matches agent_backend/app/adk/config/openai.py)
OPENAI_BASE_URL = os.getenv("HAWKEYE_OPENAI_BASE_URL", "")
OPENAI_OAUTH_URL = f"{OPENAI_BASE_URL}/oauthprovider/oauth2/token"
OPENAI_CLIENT_ID = os.getenv("HAWKEYE_OPENAI_CLIENT_ID", "")
OPENAI_CLIENT_SECRET = os.getenv("HAWKEYE_OPENAI_CLIENT_SECRET", "")

SSL_VERIFY = os.getenv("SSL_VERIFY", "False").lower() in ("true", "1", "yes")


def set_openai_token() -> str:
    """
    Fetch an OAuth token for OpenAI via Hawkeye and set OPENAI_API_KEY env var.
    Mirrors agent_backend/app/adk/services/llm/models.py::_set_openai_token().
    Returns the access_token string.
    """
    token_req_payload = {
        "grant_type": "client_credentials",
        "client_id": OPENAI_CLIENT_ID,
        "client_secret": OPENAI_CLIENT_SECRET,
    }

    logger.info(f"Getting OpenAI token from {OPENAI_OAUTH_URL}")
    token_response = requests.post(
        url=OPENAI_OAUTH_URL,
        data=token_req_payload,
        verify=SSL_VERIFY,
        allow_redirects=False,
    )

    if token_response.status_code != 200:
        msg = f"Failed to obtain OpenAI token from Hawkeye (status {token_response.status_code}): {token_response.text}"
        logger.error(msg)
        raise Exception(msg)

    tokens = json.loads(token_response.text)
    api_key = tokens["access_token"]

    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = OPENAI_BASE_URL
    logger.info("Successfully set OPENAI_API_KEY and OPENAI_API_BASE")
    return api_key


def get_openai_base_url() -> str:
    """Return the Hawkeye OpenAI base URL."""
    return OPENAI_BASE_URL

import os

import openai
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_openai_client():
    return openai.OpenAI()

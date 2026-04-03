import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

BASE_URL = "https://integrate.api.nvidia.com/v1"

MODEL_NAME = "deepseek-ai/deepseek-v3.2"
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_NOTIFY_TARGET = os.getenv("EMAIL_NOTIFY_TARGET")

BASE_URL = "https://integrate.api.nvidia.com/v1"

MODEL_NAME = "deepseek-ai/deepseek-v3.2"
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    API_KEY: str = os.getenv("API_KEY")
    AZURE_ENDPOINT: str = "https://20242-m9bfmsab-eastus2.cognitiveservices.azure.com/"
    MODEL_NAME: str = "gpt-4o-mini"

@lru_cache
def get_settings():
    return Settings()
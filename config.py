# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

ASI_API_KEY = os.getenv("ASI_API_KEY")
ASI_MODEL = os.getenv("ASI_MODEL", "asi1-mini")
BASE_URL_ASI = "https://api.asi1.ai/v1/chat/completions"
DB_PATH = "inft_meta.db"

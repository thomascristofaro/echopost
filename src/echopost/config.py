import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Carica .env
load_dotenv()

# Percorsi
BASE_DIR = Path(__file__).resolve().parent
APPSETTINGS_PATH = BASE_DIR / "appsettings.json"

# Carica appsettings.json
with open(APPSETTINGS_PATH, "r", encoding="utf-8") as f:
    appsettings = json.load(f)

# Config accessibile ovunque
FEED_URLS = appsettings["feeds"]
DOWNLOAD_FOLDER = appsettings["download_folder"]
LLM_CONFIG = appsettings["llm"]

# Variabili segrete da .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

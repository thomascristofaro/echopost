from dotenv import load_dotenv
import os
import json

load_dotenv()

with open("appsettings.json") as f:
    config = json.load(f)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_TOKEN = os.getenv("LINKEDIN_TOKEN")
FEED_URLS = config["feeds"]
DB_PATH = config["database"]
FILTER_INSTRUCTIONS = config["filter_instructions"]
CHECK_INTERVAL = config["check_interval"]

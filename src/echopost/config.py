import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

class AppConfig(BaseModel):
    feed_urls: List[str]
    relevance_prompt: str

class Settings(BaseModel):
    environment: str
    openai_api_key: str
    db_path: str
    app: AppConfig

def load_settings() -> Settings:
    load_dotenv()
    with open("appsettings.json") as f:
        data = json.load(f)
    return Settings(
        environment=data["environment"],
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        db_path=data["db_path"],
        app=AppConfig(**data["app"])
    )
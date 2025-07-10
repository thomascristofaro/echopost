import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    openai_api_key: str
    db_path: str
    feed_urls: List[str]
    relevance_prompt: str = ""
    deployment_name: str = ""
    ranking_keywords: List[str] = []
    ranking_min_score: float = 0.0
    linkedin_template: str = ""
    scheduler_min: int = 60

def load_settings() -> Settings:
    load_dotenv()
    with open("appsettings.json") as f:
        data = json.load(f)
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        feed_urls=data.get("feed_urls", []),
        db_path=data.get("db_path"),
        relevance_prompt=data.get("relevance_prompt", ""),
        deployment_name=data.get("deployment_name", ""),
        ranking_keywords=data.get("ranking_keywords", []),
        ranking_min_score=data.get("ranking_min_score", 0.0),
        linkedin_template=data.get("linkedin_template", ""),
        scheduler_min=data.get("scheduler_min", 60)
    )
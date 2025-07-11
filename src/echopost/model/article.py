from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    id: Optional[int] = None
    title: str
    url: str
    summary: str
    content: str
    relevance_score: float = 0.0
    checked: int = 0
    relevant: int = 0
    posted: int = 0
    score: float = 0.0
    published: Optional[str] = None
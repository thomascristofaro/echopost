from pydantic import BaseModel

class Article(BaseModel):
    title: str
    url: str
    summary: str
    content: str
    relevance_score: float = 0.0
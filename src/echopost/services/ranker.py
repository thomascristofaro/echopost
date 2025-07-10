from .database import Database
from typing import List
from ..model.article import Article

def score_article(title: str, content: str, keywords=None) -> float:
    if keywords is None:
        keywords = ["AI", "automation", "innovazione", "startup"]
    score = sum(content.lower().count(k.lower()) for k in keywords)
    return score

def score_relevant_articles(db: Database, keywords=None):
    articles = db.get_relevant_unposted_articles()
    for article_id, title, content in articles:
        score = score_article(title, content, keywords)
        db.update_article_score(article_id, score)

def rank_articles(articles: List[Article]) -> List[Article]:
    # TODO: implement LLM or heuristic ranking
    return sorted(articles, key=lambda x: x.relevance_score, reverse=True)
from typing import List
from ..model.article import Article

def rank_articles(articles: List[Article]) -> List[Article]:
    # TODO: implement LLM or heuristic ranking
    return sorted(articles, key=lambda x: x.relevance_score, reverse=True)
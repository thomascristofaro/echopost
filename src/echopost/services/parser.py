from newspaper import Article as NPArticle
from typing import List
from ..model.article import Article

def parse_and_filter(entries: List[dict], prompt: str, openai_key: str) -> List[Article]:
    articles = []
    for entry in entries:
        try:
            a = NPArticle(entry.link)
            a.download()
            a.parse()
            # TODO: call LLM to filter based on prompt
            articles.append(Article(
                title=a.title,
                url=entry.link,
                summary=entry.get("summary", ""),
                content=a.text,
            ))
        except Exception:
            continue
    return articles

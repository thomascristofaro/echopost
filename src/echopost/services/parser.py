from .database import Database
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

def filter_and_download_articles(db: Database, kernel, filter_instructions: str):
    articles = db.get_articles_without_content()
    for article_id, url, title, summary in articles:
        a = NPArticle(url)
        try:
            a.download()
            a.parse()
            full_text = a.text
            # Call LLM or kernel to check relevance
            is_relevant = kernel.invoke("IsThisRelevant", input=f"{filter_instructions}\nTitolo: {title}\nTesto: {full_text[:2000]}")
            relevant_flag = 1 if "sì" in is_relevant.lower() or "yes" in is_relevant.lower() else 0
            db.update_article_content_and_relevance(article_id, full_text, relevant_flag)
        except Exception as e:
            print(f"Errore su {url}: {e}")

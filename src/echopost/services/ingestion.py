import feedparser
from typing import List
from .database import Database
from newspaper import Article as NPArticle
from ..model.article import Article

def fetch_and_store_feeds(urls: List[str], db: Database):
    for url in urls:
        feed = feedparser.parse(url)
        entries = feed.values()
        for entry in entries:
            if not db.article_exists(entry["link"]):
                article = Article(
                    url=entry["link"],
                    title=entry["title"],
                    summary=entry.get("description", ""),
                    content="",
                    relevance_score=0.0,
                    checked=0,
                    relevant=0,
                    posted=0,
                    score=0.0,
                    published=entry.get("pubDate", "")
                )
                db.insert_article(article)

def filter_and_download_articles(db: Database, kernel, filter_instructions: str):
    articles = db.get_articles_without_content()
    for article in articles:
        a = NPArticle(article.url)
        try:
            a.download()
            a.parse()
            full_text = a.text
            # Call LLM or kernel to check relevance
            is_relevant = kernel.invoke("IsThisRelevant", input=f"{filter_instructions}\nTitolo: {article.title}\nTesto: {full_text[:2000]}")
            relevant_flag = 1 if "sì" in is_relevant.lower() or "yes" in is_relevant.lower() else 0
            if article.id is not None:
                db.update_article_content_and_relevance(article.id, full_text, relevant_flag)
        except Exception as e:
            print(f"Errore su {article.url}: {e}")

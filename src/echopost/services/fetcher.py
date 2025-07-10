import feedparser
from typing import List
from .database import Database

def fetch_feeds(urls: List[str]) -> List[dict]:
    entries = []
    for url in urls:
        feed = feedparser.parse(url)
        entries.extend(feed.entries)
    return entries

def fetch_and_store_feeds(urls: list, db: Database):
    for url in urls:
        entries = fetch_feeds([url])
        for entry in entries:
            if not db.article_exists(entry.link):
                db.insert_article(
                    url=entry.link,
                    title=entry.title,
                    published=entry.get("published", ""),
                    summary=entry.get("summary", "")
                )
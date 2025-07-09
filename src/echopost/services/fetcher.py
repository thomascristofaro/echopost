import feedparser
from typing import List

def fetch_feeds(urls: List[str]) -> List[dict]:
    entries = []
    for url in urls:
        feed = feedparser.parse(url)
        entries.extend(feed.entries)
    return entries
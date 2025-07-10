from .config import Settings
from .services.fetcher import fetch_feeds, fetch_and_store_feeds
from .services.parser import parse_and_filter, filter_and_download_articles
from .services.ranker import rank_articles, score_relevant_articles
from .services.publisher import publish_to_linkedin, post_best_article_to_linkedin
from .services.database import Database

# Placeholder for your LLM kernel or similar object
class DummyKernel:
    def invoke(self, *args, **kwargs):
        return "yes"  # Always returns relevant for demo

def main(settings: Settings):
    print("Starting EchoPost...")
    db = Database(settings.db_path)
    kernel = DummyKernel()  # Replace with your actual kernel/LLM

    # Step 1: Fetch and store new articles from feeds
    fetch_and_store_feeds(settings.feed_urls, db)

    # Step 2: Filter and download articles, update DB with content and relevance
    filter_and_download_articles(db, kernel, settings.relevance_prompt)

    # Step 3: Score relevant articles
    score_relevant_articles(db, settings.ranking_keywords)

    # Step 4: Post the best article to LinkedIn
    post_best_article_to_linkedin(db, kernel)
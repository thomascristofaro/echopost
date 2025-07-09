from .config import Settings
from .services.fetcher import fetch_feeds
from .services.parser import parse_and_filter
from .services.ranker import rank_articles
from .services.publisher import publish_to_linkedin

def main(settings: Settings):
    print("Starting EchoPost...")
    articles = fetch_feeds(settings.app.feed_urls)
    parsed = parse_and_filter(articles, settings.app.relevance_prompt, settings.openai_api_key)
    ranked = rank_articles(parsed)
    if ranked:
        publish_to_linkedin(ranked[0])
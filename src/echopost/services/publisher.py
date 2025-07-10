from ..model.article import Article
from .database import Database
from typing import List

def publish_to_linkedin(article: Article):
    # TODO: call LinkedIn API to post
    print(f"Publishing: {article.title}")

def post_best_article_to_linkedin(db: Database, kernel):
    row = db.get_best_article_to_post()
    if not row:
        return
    article_id, title, url, content = row
    # Generate post text using LLM/kernel
    post_text = kernel.invoke("GenerateLinkedInPost", input=f"Titolo: {title}\nTesto: {content[:3000]}\nURL: {url}")
    # Placeholder for LinkedIn API
    success = post_to_linkedin(post_text)
    if success:
        db.mark_article_posted(article_id)

def post_to_linkedin(text):
    print("Pubblicazione su LinkedIn:", text)
    return True  # Replace with LinkedIn API logic

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
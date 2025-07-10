from ..model.article import Article
from .database import Database

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
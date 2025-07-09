from ..model.article import Article

def publish_to_linkedin(article: Article):
    # TODO: call LinkedIn API to post
    print(f"Publishing: {article.title}")
from .config import Settings
from .services.ingestion import fetch_and_store_feeds, filter_and_download_articles
# from .services.publisher import post_best_article_to_linkedin
from .services.database import Database
from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

async def main(settings: Settings):
    print("Starting EchoPost...")

    db = Database(settings.db_path)
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(
        api_key=settings.azure_api_key,
        endpoint=settings.azure_endpoint,
        deployment_name=settings.deployment_name
    ))

    # example using a simple prompt
    # # es: kernel.import_plugin("IsThisRelevant", path_to_prompt_file)
    # # es: kernel.import_plugin("GenerateLinkedInPost", path_to_prompt_file)
    # test = await kernel.invoke_prompt("tell me a joke about engineers")
    # print(test)

    # Step 1: Fetch and store new articles from feeds
    fetch_and_store_feeds(settings.feed_urls, db)

    # Step 2: Filter and download articles, update DB with content and relevance
    filter_and_download_articles(db, kernel, settings.relevance_prompt)

    # # Step 3: Score relevant articles
    # score_relevant_articles(db, settings.ranking_keywords)

    # # Step 4: Post the best article to LinkedIn
    # post_best_article_to_linkedin(db, kernel)
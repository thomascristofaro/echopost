import feedparser
import sqlite3
import newspaper
from semantic_kernel import Kernel
import openai
import datetime
import time

# --- Settings ---
FEED_URLS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    # Aggiungi altri feed RSS
]

DB_PATH = "echopost.db"
CHECK_INTERVAL = 3600  # ogni ora

# Prompt di filtraggio pertinenza (modificabile a piacere)
FILTER_INSTRUCTIONS = "Seleziona solo articoli che parlano di innovazione tecnologica, AI o automazione aziendale."

# --- Init DB ---
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            published TEXT,
            content TEXT,
            summary TEXT,
            relevant INTEGER DEFAULT 0,
            posted INTEGER DEFAULT 0,
            score REAL DEFAULT 0
        )
        """)
        conn.commit()

# --- Download Feed & Save Articles ---
def fetch_and_store_feeds():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for url in FEED_URLS:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                c.execute("SELECT 1 FROM articles WHERE url=?", (entry.link,))
                if c.fetchone():
                    continue  # già presente
                c.execute("INSERT INTO articles (url, title, published, summary) VALUES (?, ?, ?, ?)",
                          (entry.link, entry.title, entry.get("published", ""), entry.get("summary", "")))
        conn.commit()

# --- Filtra e Scarica Contenuto con newspaper3k ---
def filter_and_download_articles(kernel: Kernel):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, url, title, summary FROM articles WHERE content IS NULL")
        articles = c.fetchall()

        for article_id, url, title, summary in articles:
            article = newspaper.article(url)
            try:
                article.download()
                article.parse()
                full_text = article.text

                # Chiedi al modello se l'articolo è rilevante
                is_relevant = kernel.invoke("IsThisRelevant", input=f"{FILTER_INSTRUCTIONS}\nTitolo: {title}\nTesto: {full_text[:2000]}")
                relevant_flag = 1 if "sì" in is_relevant.lower() or "yes" in is_relevant.lower() else 0

                c.execute("""
                UPDATE articles SET content = ?, relevant = ? WHERE id = ?
                """, (full_text, relevant_flag, article_id))

            except Exception as e:
                print(f"Errore su {url}: {e}")
        conn.commit()

# --- Ranking ---
def score_relevant_articles():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, content FROM articles WHERE relevant = 1 AND posted = 0")
        articles = c.fetchall()

        for article_id, title, content in articles:
            score = score_article(title, content)
            c.execute("UPDATE articles SET score = ? WHERE id = ?", (score, article_id))
        conn.commit()

def score_article(title, content):
    # Placeholder: implementa logica personalizzata di scoring
    keywords = ["AI", "automation", "innovazione", "startup"]
    score = sum(content.lower().count(k.lower()) for k in keywords)
    return score

# --- Pubblicazione su LinkedIn ---
def post_best_article_to_linkedin(kernel: Kernel):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, url, content FROM articles WHERE relevant = 1 AND posted = 0 ORDER BY score DESC LIMIT 1")
        row = c.fetchone()
        if not row:
            return
        article_id, title, url, content = row

        # Genera testo del post
        post_text = kernel.invoke("GenerateLinkedInPost", input=f"Titolo: {title}\nTesto: {content[:3000]}\nURL: {url}")

        # Pubblica su LinkedIn (placeholder)
        success = post_to_linkedin(post_text)

        if success:
            c.execute("UPDATE articles SET posted = 1 WHERE id = ?", (article_id,))
            conn.commit()

# --- Placeholder per LinkedIn API ---
def post_to_linkedin(text):
    print("Pubblicazione su LinkedIn:", text)
    return True  # In futuro, implementa le LinkedIn Marketing API

# --- MAIN LOOP ---
# def run():
    # kernel = Kernel()
    # # Carica i tuoi plugin Semantic Kernel personalizzati qui
    # # es: kernel.import_plugin("IsThisRelevant", path_to_prompt_file)
    # # es: kernel.import_plugin("GenerateLinkedInPost", path_to_prompt_file)

    # init_db()
    # fetch_and_store_feeds()
    # filter_and_download_articles(kernel)
    # score_relevant_articles()
    # post_best_article_to_linkedin(kernel)

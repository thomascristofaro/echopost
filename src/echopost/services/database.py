import sqlite3
from typing import List, Tuple, Optional, Any

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    def init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
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

    def article_exists(self, url: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT 1 FROM articles WHERE url=?", (url,))
            return c.fetchone() is not None

    def insert_article(self, url: str, title: str, published: str, summary: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO articles (url, title, published, summary) VALUES (?, ?, ?, ?)",
                (url, title, published, summary)
            )
            conn.commit()

    def get_articles_without_content(self) -> List[Tuple[int, str, str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT id, url, title, summary FROM articles WHERE content IS NULL")
            return c.fetchall()

    def update_article_content_and_relevance(self, article_id: int, content: str, relevant: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE articles SET content = ?, relevant = ? WHERE id = ?",
                (content, relevant, article_id)
            )
            conn.commit()

    def get_relevant_unposted_articles(self) -> List[Tuple[int, str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT id, title, content FROM articles WHERE relevant = 1 AND posted = 0")
            return c.fetchall()

    def update_article_score(self, article_id: int, score: float) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE articles SET score = ? WHERE id = ?", (score, article_id))
            conn.commit()

    def get_best_article_to_post(self) -> Optional[Tuple[int, str, str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, title, url, content FROM articles WHERE relevant = 1 AND posted = 0 ORDER BY score DESC LIMIT 1"
            )
            return c.fetchone()

    def mark_article_posted(self, article_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE articles SET posted = 1 WHERE id = ?", (article_id,))
            conn.commit()
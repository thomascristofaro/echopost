from typing import List, Tuple, Optional, Any
from ..model.article import Article
import sqlite3

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
                checked INTEGER DEFAULT 0,
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

    def insert_article(self, article: Article) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO articles (url, title, published, summary, content, checked, relevant, posted, score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    article.url,
                    article.title,
                    article.published,
                    article.summary,
                    article.content,
                    article.checked,
                    article.relevant,
                    article.posted,
                    article.score
                )
            )
            conn.commit()

    def get_articles_without_content(self) -> List[Article]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT id, url, title, summary, content, checked, relevant, posted, score, published FROM articles WHERE content IS NULL")
            rows = c.fetchall()
            return [Article(
                id=row[0], url=row[1], title=row[2], summary=row[3], content=row[4], checked=row[5], relevant=row[6], posted=row[7], score=row[8], published=row[9]
            ) for row in rows]

    def update_article_content_and_relevance(self, article_id: int, content: str, relevant: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE articles SET content = ?, relevant = ? WHERE id = ?",
                (content, relevant, article_id)
            )
            conn.commit()

    def get_relevant_unposted_articles(self) -> List[Article]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT id, title, content, url, summary, score, checked, relevant, posted, published FROM articles WHERE relevant = 1 AND posted = 0")
            rows = c.fetchall()
            return [Article(
                id=row[0], title=row[1], content=row[2], url=row[3], summary=row[4], score=row[5], checked=row[6], relevant=row[7], posted=row[8], published=row[9]
            ) for row in rows]

    def update_article_score(self, article_id: int, score: float) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE articles SET score = ? WHERE id = ?", (score, article_id))
            conn.commit()

    def get_best_article_to_post(self) -> Optional[Article]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, title, url, content, summary, score, checked, relevant, posted, published FROM articles WHERE relevant = 1 AND posted = 0 ORDER BY score DESC LIMIT 1"
            )
            row = c.fetchone()
            if row:
                return Article(
                    id=row[0], title=row[1], url=row[2], content=row[3], summary=row[4], score=row[5], checked=row[6], relevant=row[7], posted=row[8], published=row[9]
                )
            return None

    def mark_article_posted(self, article_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE articles SET posted = 1 WHERE id = ?", (article_id,))
            conn.commit()
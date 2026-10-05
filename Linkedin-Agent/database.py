import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database operations for LinkedIn Agent"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db_exists()
        self._create_tables()

    def _ensure_db_exists(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def _create_tables(self):
        """Create necessary database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Table for gathered content (news, interview questions, etc.)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS gathered_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT UNIQUE,
                    content TEXT,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Table for generated posts
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS generated_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    post_type TEXT,
                    tags TEXT,
                    hashtags TEXT,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    posted BOOLEAN DEFAULT 0,
                    posted_at TIMESTAMP,
                    posted_url TEXT,
                    variation_index INTEGER
                )
            """
            )

            # Table for post engagement tracking
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS post_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    post_url TEXT,
                    post_content TEXT,
                    post_date DATE,
                    topic TEXT,
                    content_type TEXT,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES generated_posts(id)
                )
            """
            )

            # Table for content cache
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS content_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    cache_key TEXT UNIQUE NOT NULL,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            """
            )

            # Table for analytics recommendations
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS analytics_recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_date DATE,
                    topic TEXT,
                    content_type TEXT,
                    avg_views REAL,
                    avg_engagement_rate REAL,
                    recommendation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()

    def insert_gathered_content(
        self, source: str, title: str, url: str, content: str, category: str
    ) -> bool:
        """Insert gathered content into database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO gathered_content (source, title, url, content, category)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (source, title, url, content, category),
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error inserting gathered content: {e}")
            return False

    def get_recent_content(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent gathered content"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM gathered_content 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """,
                    (limit,),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting recent content: {e}")
            return []

    def insert_generated_post(
        self,
        title: str,
        content: str,
        post_type: str,
        tags: str,
        hashtags: str,
        variation_index: int = 0,
    ) -> int:
        """Insert generated post into database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO generated_posts (title, content, post_type, tags, hashtags, variation_index)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (title, content, post_type, tags, hashtags, variation_index),
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error inserting generated post: {e}")
            return -1

    def get_today_posts(self) -> List[Dict[str, Any]]:
        """Get today's generated posts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM generated_posts 
                    WHERE DATE(generated_at) = DATE('now')
                    ORDER BY generated_at DESC
                """,
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting today's posts: {e}")
            return []

    def mark_post_as_posted(
        self, post_id: int, post_url: str, posted_at: datetime = None
    ) -> bool:
        """Mark a post as posted on LinkedIn"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE generated_posts 
                    SET posted = 1, posted_at = ?, posted_url = ?
                    WHERE id = ?
                """,
                    (posted_at or datetime.now(), post_url, post_id),
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error marking post as posted: {e}")
            return False

    def insert_post_engagement(
        self,
        post_id: int,
        post_url: str,
        post_content: str,
        topic: str,
        content_type: str,
        views: int = 0,
        likes: int = 0,
        comments: int = 0,
        shares: int = 0,
    ) -> bool:
        """Insert post engagement metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO post_analytics 
                    (post_id, post_url, post_content, post_date, topic, content_type, views, likes, comments, shares)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        post_id,
                        post_url,
                        post_content,
                        datetime.now().date(),
                        topic,
                        content_type,
                        views,
                        likes,
                        comments,
                        shares,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error inserting engagement metrics: {e}")
            return False

    def get_engagement_analytics(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get engagement analytics for past N days"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM post_analytics 
                    WHERE post_date >= DATE('now', '-' || ? || ' days')
                    ORDER BY post_date DESC
                """,
                    (days,),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting engagement analytics: {e}")
            return []

    def cache_content(
        self, source: str, cache_key: str, data: str, expires_in_hours: int = 24
    ) -> bool:
        """Cache content to avoid duplicate requests"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                from datetime import timedelta

                expires_at = datetime.now() + timedelta(hours=expires_in_hours)
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO content_cache (source, cache_key, data, expires_at)
                    VALUES (?, ?, ?, ?)
                """,
                    (source, cache_key, data, expires_at),
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error caching content: {e}")
            return False

    def get_cached_content(self, source: str, cache_key: str) -> str:
        """Get cached content if available and not expired"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT data FROM content_cache 
                    WHERE source = ? AND cache_key = ? AND expires_at > datetime('now')
                """,
                    (source, cache_key),
                )
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting cached content: {e}")
            return None

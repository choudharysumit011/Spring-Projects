import requests
import logging
import time
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET
import config
from database import DatabaseManager

logger = logging.getLogger(__name__)


class ContentGatherer:
    """Gathers content from multiple sources"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.session = requests.Session()
        self.session.headers.update(config.DEFAULT_HEADERS)

    def gather_all_content(self) -> Dict[str, List[Dict[str, Any]]]:
        """Gather content from all sources"""
        content = {
            "news": [],
            "interview_questions": [],
            "reddit_discussions": [],
            "trending_dev_posts": [],
        }

        logger.info("Starting content gathering from all sources...")

        # Gather news
        content["news"] = self.fetch_news()
        time.sleep(config.REQUEST_DELAY)

        # Gather interview questions
        content["interview_questions"] = self.fetch_interview_questions()
        time.sleep(config.REQUEST_DELAY)

        # Gather Reddit discussions
        try:
            content["reddit_discussions"] = self.fetch_reddit_discussions()
        except Exception as e:
            logger.warning(f"Failed to fetch Reddit discussions: {e}")

        time.sleep(config.REQUEST_DELAY)

        # Gather trending dev posts
        content["trending_dev_posts"] = self.fetch_trending_dev_posts()

        logger.info(f"Content gathering completed. Total items: {sum(len(v) for v in content.values())}")
        return content

    def fetch_news(self) -> List[Dict[str, Any]]:
        """Fetch latest news from NewsAPI"""
        try:
            if not config.NEWSAPI_KEY:
                logger.warning("NewsAPI key not configured, skipping news fetch")
                return []

            urls = [
                f"{config.NEWSAPI_BASE_URL}/everything?q=AI+OR+machine+learning+OR+software+development&language=en&sortBy=publishedAt&pageSize=10",
                f"{config.NEWSAPI_BASE_URL}/everything?q=SDE+OR+software+engineer+interview&language=en&sortBy=publishedAt&pageSize=5",
            ]

            all_news = []
            for url in urls:
                params = {"apiKey": config.NEWSAPI_KEY}
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                if data.get("articles"):
                    for article in data["articles"]:
                        news_item = {
                            "source": "NewsAPI",
                            "title": article.get("title", ""),
                            "url": article.get("url", ""),
                            "content": article.get("description", ""),
                            "category": "technology_news",
                        }
                        all_news.append(news_item)
                        self.db.insert_gathered_content(**news_item)

                time.sleep(1)

            logger.info(f"Fetched {len(all_news)} news items from NewsAPI")
            return all_news[:config.MAX_NEWS_ITEMS]

        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []

    def fetch_interview_questions(self) -> List[Dict[str, Any]]:
        """Fetch interview questions from HackerNews and other sources"""
        try:
            questions = []

            # Fetch from HackerNews API - filter for interview-related posts
            try:
                questions.extend(self._fetch_hackernews_items())
            except Exception as e:
                logger.warning(f"Failed to fetch from HackerNews: {e}")

            # Fetch SDE interview questions from NewsAPI
            try:
                questions.extend(self._fetch_sde_interview_news())
            except Exception as e:
                logger.warning(f"Failed to fetch SDE interview news: {e}")

            logger.info(f"Fetched {len(questions)} interview questions")
            return questions[:config.MAX_INTERVIEW_QUESTIONS]

        except Exception as e:
            logger.error(f"Error fetching interview questions: {e}")
            return []

    def _fetch_sde_interview_news(self) -> List[Dict[str, Any]]:
        """Fetch SDE interview questions from NewsAPI"""
        try:
            if not config.NEWSAPI_KEY:
                logger.warning("NewsAPI key not configured, skipping SDE interview news")
                return []

            interview_keywords = [
                "SDE interview questions",
                "software engineer interview",
                "interview preparation",
                "coding interview",
                "system design interview",
            ]

            all_questions = []
            for keyword in interview_keywords:
                try:
                    url = f"{config.NEWSAPI_BASE_URL}/everything"
                    params = {
                        "q": keyword,
                        "language": "en",
                        "sortBy": "publishedAt",
                        "pageSize": 5,
                        "apiKey": config.NEWSAPI_KEY,
                    }
                    response = self.session.get(url, params=params, timeout=10)
                    response.raise_for_status()

                    data = response.json()
                    if data.get("articles"):
                        for article in data["articles"]:
                            question = {
                                "source": "NewsAPI-Interviews",
                                "title": article.get("title", ""),
                                "url": article.get("url", ""),
                                "content": article.get("description", ""),
                                "category": "interview_questions",
                            }
                            all_questions.append(question)
                            self.db.insert_gathered_content(**question)

                    time.sleep(1)

                except Exception as e:
                    logger.debug(f"Error fetching interviews for keyword '{keyword}': {e}")
                    continue

            logger.info(f"Fetched {len(all_questions)} SDE interview questions from NewsAPI")
            return all_questions

        except Exception as e:
            logger.error(f"Error fetching SDE interview news: {e}")
            return []

    def _fetch_hackernews_items(self) -> List[Dict[str, Any]]:
        """Fetch latest items from HackerNews"""
        try:
            # Fetch top stories
            response = self.session.get(
                f"{config.HACKERNEWS_BASE_URL}/topstories.json", timeout=10
            )
            response.raise_for_status()
            story_ids = response.json()[:20]

            questions = []
            for story_id in story_ids:
                try:
                    item_response = self.session.get(
                        f"{config.HACKERNEWS_BASE_URL}/item/{story_id}.json", timeout=10
                    )
                    item_response.raise_for_status()
                    item = item_response.json()

                    if item.get("type") == "story" and item.get("title"):
                        question = {
                            "source": "HackerNews",
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "content": f"Score: {item.get('score', 0)}, Comments: {item.get('descendants', 0)}",
                            "category": "industry_insights",
                        }
                        questions.append(question)
                        self.db.insert_gathered_content(**question)

                    time.sleep(0.1)

                except Exception as e:
                    logger.debug(f"Error fetching HackerNews item {story_id}: {e}")
                    continue

            return questions

        except Exception as e:
            logger.error(f"Error fetching HackerNews items: {e}")
            return []

    def fetch_reddit_discussions(self) -> List[Dict[str, Any]]:
        """Fetch discussions from Reddit using PRAW"""
        try:
            # Skip Reddit if no credentials
            if not config.REDDIT_CLIENT_ID or not config.REDDIT_CLIENT_SECRET:
                logger.info("Reddit credentials not configured, skipping Reddit fetch")
                return []

            import praw

            reddit = praw.Reddit(
                client_id=config.REDDIT_CLIENT_ID,
                client_secret=config.REDDIT_CLIENT_SECRET,
                user_agent=config.REDDIT_USER_AGENT,
            )

            discussions = []
            for subreddit_name in config.REDDIT_SUBREDDITS:
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    for submission in subreddit.hot(limit=5):
                        discussion = {
                            "source": f"Reddit/{subreddit_name}",
                            "title": submission.title,
                            "url": f"https://reddit.com{submission.permalink}",
                            "content": submission.selftext[:200] if submission.selftext else submission.title,
                            "category": "community_discussions",
                        }
                        discussions.append(discussion)
                        self.db.insert_gathered_content(**discussion)

                except Exception as e:
                    logger.warning(f"Error fetching from r/{subreddit_name}: {e}")
                    continue

                time.sleep(config.REQUEST_DELAY)

            logger.info(f"Fetched {len(discussions)} Reddit discussions")
            return discussions

        except ImportError:
            logger.warning("PRAW not installed, skipping Reddit fetch")
            return []
        except Exception as e:
            logger.warning(f"Error fetching Reddit discussions: {e}")
            return []

    def fetch_trending_dev_posts(self) -> List[Dict[str, Any]]:
        """Fetch trending posts from Dev.to and other sources"""
        try:
            posts = []

            # Fetch from Dev.to API
            try:
                posts.extend(self._fetch_devto_posts())
            except Exception as e:
                logger.warning(f"Failed to fetch from Dev.to: {e}")

            # Fetch from Medium RSS
            try:
                posts.extend(self._fetch_medium_posts())
            except Exception as e:
                logger.warning(f"Failed to fetch from Medium: {e}")

            logger.info(f"Fetched {len(posts)} trending dev posts")
            return posts

        except Exception as e:
            logger.error(f"Error fetching trending dev posts: {e}")
            return []

    def _fetch_devto_posts(self) -> List[Dict[str, Any]]:
        """Fetch trending posts from Dev.to"""
        try:
            response = self.session.get(
                "https://dev.to/api/articles?tag=webdev,ai,javascript,career&sort_by=trending",
                timeout=10,
            )
            response.raise_for_status()

            posts = []
            for article in response.json()[:10]:
                post = {
                    "source": "Dev.to",
                    "title": article.get("title", ""),
                    "url": article.get("url", ""),
                    "content": article.get("description", ""),
                    "category": "technical_insights",
                }
                posts.append(post)
                self.db.insert_gathered_content(**post)

            return posts

        except Exception as e:
            logger.error(f"Error fetching Dev.to posts: {e}")
            return []

    def _fetch_medium_posts(self) -> List[Dict[str, Any]]:
        """Fetch trending posts from Medium via RSS"""
        try:
            response = self.session.get(
                "https://medium.com/feed/tag/software-engineering",
                timeout=10
            )
            response.raise_for_status()

            posts = []
            root = ET.fromstring(response.content)

            # Parse RSS feed items
            for item in root.findall('.//item')[:10]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                description_elem = item.find('description')

                title = title_elem.text if title_elem is not None else ""
                link = link_elem.text if link_elem is not None else ""
                description = description_elem.text if description_elem is not None else ""

                # Clean HTML from description if present
                if description:
                    description = BeautifulSoup(description, 'html.parser').get_text()[:200]

                post = {
                    "source": "Medium",
                    "title": title,
                    "url": link,
                    "content": description,
                    "category": "technical_insights",
                }
                posts.append(post)
                self.db.insert_gathered_content(**post)

            return posts

        except Exception as e:
            logger.error(f"Error fetching Medium posts: {e}")
            return []

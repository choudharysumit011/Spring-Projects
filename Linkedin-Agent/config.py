import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistral/mistral-small")  # Cost-effective, reliable model

# News API Configuration
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
NEWSAPI_BASE_URL = "https://newsapi.org/v2"

# HackerNews API Configuration
HACKERNEWS_BASE_URL = "https://hacker-news.firebaseio.com/v0"

# Reddit Configuration (PRAW)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "LinkedInAgent/1.0")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/linkedin_agent.db")

# Scheduler Configuration
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "09:00")  # Default: 9 AM daily
SCHEDULE_TIMEZONE = os.getenv("SCHEDULE_TIMEZONE", "UTC")

# LeetCode & HackerRank Scraping
LEETCODE_BASE_URL = "https://leetcode.com"
HACKERRANK_BASE_URL = "https://www.hackerrank.com"

# Reddit Subreddits to monitor
REDDIT_SUBREDDITS = [
    "webdev",
    "devops",
    "MachineLearning",
    "programming",
    "learnprogramming",
    "golang",
    "Kubernetes",
]

# Content Generation Config
MAX_INTERVIEW_QUESTIONS = 5
MAX_NEWS_ITEMS = 10
GENERATE_POST_VARIATIONS = 3

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = "./logs"

# LinkedIn Posting Config (manual workflow)
POSTS_OUTPUT_DIR = "./generated_posts"

# Content Cache Duration (hours)
CACHE_DURATION = 24

# Request Headers for Web Scraping
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Rate Limiting
REQUEST_DELAY = 2  # seconds between requests to avoid rate limiting

# Plan: Build Multi-Function LinkedIn Growth & Content Agent

Build a Python automation agent with three core capabilities: (1) gather SDE interview questions and tech/AI/industry news daily, (2) schedule and post to LinkedIn, (3) analyze post performance and adapt content strategy based on engagement metrics.

## Steps

1. **Set up project structure and dependencies**
   - Create `requirements.txt` with OpenRouter LLM API, web scraping libraries (`BeautifulSoup`, `requests`, `selenium`), scheduling (`APScheduler`), RSS parsing (`feedparser`)
   - Initialize main modules: `config.py`, `content_gatherer.py`, `content_generator.py`, `manual_linkedin_handler.py`, `analytics_tracker.py`, `scheduler.py`, `main.py`, `database.py`

2. **Implement multi-source content gathering module** (`content_gatherer.py`)
   - Fetch from **NewsAPI** (free tier) — latest tech/AI/industry news
   - Fetch from **HackerNews API** (free) — trending discussions
   - Scrape **LeetCode** — latest SDE interview problems (web crawler)
   - Scrape **HackerRank** — coding challenges and interviews
   - Scrape **Reddit** — tech communities (r/webdev, r/devops, r/MachineLearning, r/programming)
   - Scrape **LinkedIn posts** — analyze trending posts in your network (web crawler)
   - Scrape **Dev.to**, **Medium**, **CSS-Tricks** — latest technical blogs
   - Store raw data in SQLite for deduplication and tracking

3. **Implement content generation module** (`content_generator.py`)
   - Use **OpenRouter** to call various LLM models (access to Claude, GPT-4, Mistral, etc.)
   - Pass gathered interview questions + news items to LLM
   - Generate unique, engaging LinkedIn post copy daily
   - Create variations: short posts, threads, carousel-style posts
   - Add relevant hashtags and CTAs based on content type

4. **Implement manual LinkedIn posting handler** (`manual_linkedin_handler.py`)
   - Since no LinkedIn API available: generate formatted post content ready for copy-paste
   - Create daily briefing that user can manually post or schedule via LinkedIn's native scheduler
   - Option 1: Generate plain text formatted for LinkedIn
   - Option 2: Store posts in database with timestamps for user to post manually
   - Option 3: Generate HTML/JSON export for LinkedIn's "Scheduled Posts" feature

5. **Implement analytics tracking module** (`analytics_tracker.py`)
   - Store posted content in SQLite with metadata (date, topic, format, length)
   - Provide manual entry point for users to log engagement metrics (views, likes, comments, shares)
   - Use LLM to analyze patterns: which topics/formats get best engagement
   - Generate weekly/monthly analytics reports
   - Recommend content adjustments based on historical performance

6. **Set up scheduling & automation** (`scheduler.py`)
   - Use `APScheduler` to run gathering → generating → preparing cycle daily (configurable time)
   - Daily: Fetch news/interview questions → Generate post → Save to database
   - Weekly: Analyze engagement trends → Recommend content strategy
   - Add logging for monitoring agent actions

7. **Create main entry point** (`main.py`)
   - Initialize all modules and start scheduler
   - Provide CLI interface for:
     - Manual content generation trigger
     - View today's prepared post
     - Log engagement metrics
     - View analytics/recommendations
     - Configure post timing and sources

## Further Considerations

1. **OpenRouter LLM Selection** — OpenRouter provides unified API access to multiple models (Claude, GPT-4, Mistral, LLaMA, etc.). Recommendation: Start with a cost-effective model like Mistral or Claude-Instant for daily content generation; benchmark quality vs cost.

2. **Manual LinkedIn Posting Workflow** — Since no API access, the agent prepares content that user manually posts. Recommendation: Generate content daily and store in database. User can either:
   - Copy-paste to LinkedIn manually (takes 30 seconds)
   - Use LinkedIn's native "Schedule post" feature (can bulk schedule)
   - Generate weekly digest for planning purposes

3. **Web Crawling Rate Limiting** — Scraping LeetCode, Reddit, LinkedIn, Medium can hit rate limits. Recommendation: 
   - Add delays between requests (2-5 seconds)
   - Rotate user agents
   - Cache responses for 24 hours to avoid duplicate scrapes
   - Respect robots.txt and terms of service

4. **Reddit/Twitter Scraping** — Reddit allows basic scraping; Twitter/X blocks most scrapers. Recommendation:
   - Use `praw` library for Reddit (free, no authentication needed for public posts)
   - For Twitter insights, use HackerNews which aggregates tech discussions instead
   - Consider paid APIs later if needed

5. **LeetCode/HackerRank Scraping** — These sites may block automated scraping. Recommendation:
   - Use browser automation (`selenium`) as fallback for JavaScript-heavy sites
   - Cache interview questions daily (they don't change frequently)
   - Fall back to RSS feeds or public APIs if available

6. **Content Quality & LLM Prompting** — LLM output quality depends on input data. Recommendation:
   - Provide LLM with 3-5 recent interview questions + 5-10 news items as context
   - Use prompt engineering to specify tone (professional, conversational, educational)
   - Include hashtag suggestions and industry keywords in the prompt
   - Generate multiple variations and let user pick the best

7. **Analytics Tracking Without LinkedIn API** — Cannot auto-fetch metrics. Recommendation:
   - Maintain spreadsheet or database table for manual logging
   - Track: date, post ID/link, content topic, format, views, likes, comments, shares
   - Use LLM to analyze patterns from historical data
   - Weekly recommendations based on engagement trends

8. **Content Variety & Scheduling** — To avoid monotony and maximize reach. Recommendation:
   - Mix content types: tips, questions, news summaries, interview breakdowns, opinion pieces
   - Vary posting time based on analytics (morning vs evening engagement)
   - Create threads (multiple posts on same topic) for deeper reach
   - Tag relevant communities/people when possible

## Implementation Dependencies

### Core Libraries
- `openrouter` or `httpx`/`requests` — OpenRouter LLM API integration
- `beautifulsoup4` — Web scraping for LeetCode, HackerRank, Dev.to, Medium, LinkedIn
- `selenium` — Browser automation for JavaScript-heavy sites (LeetCode, Reddit if needed)
- `praw` — Python Reddit API Wrapper (free, no auth for public posts)
- `feedparser` — RSS/Atom feed parsing for news aggregation
- `requests` — HTTP requests for API calls (NewsAPI, HackerNews)
- `apscheduler` — Job scheduling for daily content generation
- `python-dotenv` — Environment variable management
- `sqlite3` — Built-in; for storing gathered content and analytics
- `lxml` — Fast XML parsing (optional, for feedparser)

### Free APIs Required
- **NewsAPI** — Free tier (100 requests/day) — https://newsapi.org/
- **HackerNews API** — Completely free, no key needed — https://hackernews.algolia.com/api
- **Reddit (PRAW)** — Free, no authentication for public posts — https://www.reddit.com/dev/api
- **LeetCode** — No official API; web scraping required
- **HackerRank** — No official API; web scraping required
- **Dev.to** — Free API available — https://docs.dev.to/api/
- **Medium** — No official API; RSS feeds available
- **OpenRouter** — Paid API access but supports free models; set budget limits

### API Keys Required
- **OpenRouter API key** — https://openrouter.ai/ (set spending limits to avoid surprise charges)
- **NewsAPI key** — Free tier (100 requests/day)
- Optional: **LinkedIn** credentials for web scraping if using Selenium browser automation

### Project Structure
```
linkedin-agent/
├── config.py                      # Configuration & environment variables
├── content_gatherer.py            # Multi-source content fetching
├── content_generator.py           # LLM content generation using OpenRouter
├── manual_linkedin_handler.py     # Prepare content for manual posting
├── analytics_tracker.py           # Track engagement & analyze patterns
├── scheduler.py                   # APScheduler setup
├── database.py                    # SQLite schema & operations
├── main.py                        # CLI entry point & scheduler starter
├── requirements.txt               # Dependencies
├── .env.example                   # Environment variables template
├── logs/                          # Agent logs (created at runtime)
├── data/                          # SQLite database file
└── generated_posts/               # Daily generated posts (optional)
```

# LinkedIn Agent - API Integration Guide

## 🔑 Getting Required API Keys

### 1. OpenRouter API (REQUIRED) ⭐

**What it does**: Access to multiple LLM models (Claude, GPT-4, Mistral, etc.)

**Cost**: 
- Free tier: Test with free models
- Paid: $0.001-0.01 per 1000 tokens (~0.5¢ per post)

**Steps**:
1. Go to https://openrouter.ai/
2. Click "Sign Up" (top right)
3. Create account with email/GitHub
4. Go to Settings → API Keys
5. Create new API key
6. Copy the key to `.env`:
   ```
   OPENROUTER_API_KEY=sk-or-...
   ```

**Model Selection** (in `.env`):
```env
# Recommended for cost (fastest, cheapest)
OPENROUTER_MODEL=mistral/mistral-7b-instruct

# Better quality (mid-cost)
OPENROUTER_MODEL=meta-llama/llama-2-13b-chat

# Best quality (expensive)
OPENROUTER_MODEL=anthropic/claude-2

# Visit https://openrouter.ai/models for full list
```

**Set Spending Limits**:
1. OpenRouter Dashboard → Settings
2. Set daily/monthly budget limit
3. Recommended: $2-5/month for daily posting

---

### 2. NewsAPI (OPTIONAL but Recommended) 📰

**What it does**: Latest tech and AI news with categories

**Cost**: Completely FREE (100 requests/day)

**Steps**:
1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Enter email and click "Subscribe"
4. Copy the free API key
5. Add to `.env`:
   ```
   NEWSAPI_KEY=abc123def456
   ```

**Without NewsAPI**:
- Agent will skip news gathering
- Use HackerNews and Reddit instead (both free)
- Still generates good posts from other sources

---

### 3. Reddit/PRAW (FREE, Optional) 👥

**What it does**: Discussions from tech subreddits

**Cost**: Completely FREE

**Setup Option A: Public Posts (No Auth)**
```env
# No API key needed for public subreddits
# Just leave REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET empty
# Agent will still fetch discussions
```

**Setup Option B: With Authentication** (Better):
1. Go to https://www.reddit.com/prefs/apps
2. Scroll to bottom → Create another app
3. Fill form:
   - name: "LinkedInAgent"
   - type: Select "script"
   - description: "LinkedIn content generation"
   - About URL: https://your-site.com
   - Redirect URI: http://localhost:8080
4. Click Create
5. Copy the values:
   ```env
   REDDIT_CLIENT_ID=abc123...
   REDDIT_CLIENT_SECRET=xyz789...
   REDDIT_USER_AGENT=LinkedInAgent/1.0 (by YourUsername)
   ```

---

### 4. Dev.to API (FREE) 👨‍💻

**What it does**: Developer blog posts and tutorials

**Cost**: Completely FREE (no API key needed)

**Setup**: No action needed
- Agent automatically fetches from Dev.to
- Already configured in `content_gatherer.py`

---

### 5. Medium RSS (FREE) 📚

**What it does**: Technical blog posts

**Cost**: Completely FREE (no API key needed)

**Setup**: No action needed
- Agent automatically fetches via RSS
- Already configured in `content_gatherer.py`

---

### 6. HackerNews API (FREE) 🔗

**What it does**: Trending tech discussions

**Cost**: Completely FREE (no API key needed)

**Setup**: No action needed
- Completely open API
- Already configured in `content_gatherer.py`

---

## ✅ Minimal Setup (Fastest)

If you want to get started immediately:

1. Get OpenRouter API key (required)
   - https://openrouter.ai/ (takes 2 minutes)
   
2. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env`, add only this:
   ```env
   OPENROUTER_API_KEY=your_key_here
   ```

4. Done! Run:
   ```bash
   python main.py --generate
   ```

---

## 🚀 Full Setup (Recommended)

For best results with all content sources:

1. **OpenRouter** (2 min)
   - https://openrouter.ai/
   
2. **NewsAPI** (2 min)
   - https://newsapi.org/
   
3. **Reddit** (Optional, 3 min)
   - https://www.reddit.com/prefs/apps

4. Update `.env`:
   ```env
   OPENROUTER_API_KEY=sk-or-...
   OPENROUTER_MODEL=mistral/mistral-7b-instruct
   NEWSAPI_KEY=abc123...
   REDDIT_CLIENT_ID=xyz...
   REDDIT_CLIENT_SECRET=abc...
   REDDIT_USER_AGENT=LinkedInAgent/1.0 (by YourUsername)
   SCHEDULE_TIME=09:00
   SCHEDULE_TIMEZONE=UTC
   ```

5. Run:
   ```bash
   python main.py --schedule
   ```

---

## 💰 Cost Estimate

### Monthly Cost
```
Without paid APIs:
- OpenRouter: ~$1-3/month (5 posts × $0.002-0.006)
- NewsAPI: FREE
- Others: FREE
Total: ~$2-4/month
```

### Daily Cost
```
Per post generation:
- OpenRouter: ~0.5¢ - 1¢
- NewsAPI: FREE (100 req/day included)
Total: ~0.5¢ per day
```

### Annual Cost
```
~$6-48/year (minimal)
```

---

## 🔒 API Key Safety

### DO ✅
- Store in `.env` file (never commit to git)
- Use environment variables only
- Set spending limits on OpenRouter dashboard
- Keep `.env` in `.gitignore`

### DON'T ❌
- Share API keys publicly
- Hardcode keys in Python files
- Push `.env` to GitHub
- Use the same key for multiple apps

### Protection Steps
1. Add to `.gitignore`:
   ```
   .env
   data/
   logs/
   generated_posts/
   ```

2. If key leaked:
   - Regenerate on OpenRouter
   - Update `.env` file
   - No code changes needed

---

## 🧪 Testing API Keys

### Test OpenRouter
```bash
python -c "
import requests
import config
response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={'Authorization': f'Bearer {config.OPENROUTER_API_KEY}'},
    json={
        'model': config.OPENROUTER_MODEL,
        'messages': [{'role': 'user', 'content': 'Say hello'}],
        'max_tokens': 10,
    }
)
print(response.json())
"
```

### Test NewsAPI
```bash
python -c "
import requests
import config
response = requests.get(
    'https://newsapi.org/v2/top-headlines',
    params={'q': 'technology', 'apiKey': config.NEWSAPI_KEY}
)
print('Status:', response.status_code)
print('Articles:', len(response.json().get('articles', [])))
"
```

### Test Reddit
```bash
python -c "
import praw
import config
reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT
)
subreddit = reddit.subreddit('programming')
print('Hot posts:', len(list(subreddit.hot(limit=5))))
"
```

---

## 🆘 Troubleshooting API Issues

### "OPENROUTER_API_KEY not set"
```
Solution:
1. Check .env file exists
2. Check OPENROUTER_API_KEY is set
3. Restart Python (cache may be stale)
4. Use: python main.py (verify status)
```

### "Invalid API key"
```
Solution:
1. Regenerate key on OpenRouter dashboard
2. Copy exact key (no extra spaces)
3. Test with provided script above
```

### "Rate limit exceeded"
```
Solution (for NewsAPI):
1. Free tier: 100 requests/day
2. Upgrade to paid plan for more
3. Or: Remove NewsAPI key, use only free sources
```

### "429 Too Many Requests"
```
Solution:
1. Increase REQUEST_DELAY in .env
2. Example: REQUEST_DELAY=3 (instead of 2)
3. Reduce MAX_NEWS_ITEMS and MAX_INTERVIEW_QUESTIONS
4. Increase CACHE_DURATION to 48 hours
```

### HackerNews not working
```
Reason: Might be down or slow
Solution: Agent handles gracefully, uses fallback sources
Check: logs/linkedin_agent.log for details
```

### Reddit not working
```
Solution 1 (if no auth):
- Leave REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET empty
- Agent will try unauthenticated (slower, limited)

Solution 2 (if auth fails):
- Regenerate credentials at: https://www.reddit.com/prefs/apps
- Delete old app and create new one
- Copy credentials exactly
```

---

## 📊 API Quotas Reference

| Service | Free Tier | Cost | Reset |
|---------|-----------|------|-------|
| OpenRouter | Free models | Pay-per-token | N/A |
| NewsAPI | 100 req/day | $45/mo for more | Daily |
| HackerNews | Unlimited | Free | N/A |
| Reddit | Unlimited | Free | N/A |
| Dev.to | Unlimited | Free | N/A |
| Medium | Unlimited (RSS) | Free | N/A |

---

## 🔄 Recommended Configuration

For best experience with minimal cost:

```env
# REQUIRED
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=mistral/mistral-7b-instruct

# Recommended (free)
NEWSAPI_KEY=your_free_key

# Nice to have (optional)
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=LinkedInAgent/1.0

# Schedule (default is fine)
SCHEDULE_TIME=09:00
SCHEDULE_TIMEZONE=UTC

# Optional tweaks
REQUEST_DELAY=2
CACHE_DURATION=24
MAX_INTERVIEW_QUESTIONS=5
MAX_NEWS_ITEMS=10
GENERATE_POST_VARIATIONS=3
```

---

## 🎯 What You Get

With this setup:

✅ Content from 6+ sources daily
✅ AI-generated posts 3 different ways
✅ Cost: ~$2-5/month
✅ Time to setup: ~10 minutes
✅ Automatic daily posting
✅ Analytics and recommendations

Ready? Follow QUICKSTART.md next!

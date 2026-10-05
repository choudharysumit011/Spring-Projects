# LinkedIn Agent - Quick Start Guide

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
# Activate virtual environment (if not already done)
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux

# Install required packages
pip install -r requirements.txt
```

### Step 2: Create Configuration File

```bash
# Copy the example configuration
cp .env.example .env
```

### Step 3: Add API Keys to `.env`

Open `.env` file and update with your API keys:

```env
# REQUIRED: OpenRouter API key
# Get free key from: https://openrouter.ai/
OPENROUTER_API_KEY=your_key_here

# OPTIONAL: NewsAPI key for better news coverage
# Get from: https://newsapi.org/ (free tier: 100 requests/day)
NEWSAPI_KEY=your_key_here
```

### Step 4: Test the Agent

```bash
# Test 1: Check if agent initializes correctly
python main.py

# Test 2: Generate posts manually
python main.py --generate

# Test 3: View today's posts
python main.py --today
```

## 📅 Starting the Scheduler

Once you've confirmed the agent works:

```bash
# Start the scheduler (runs daily at 9 AM by default)
python main.py --schedule
```

The agent will:
1. Run daily at configured time (default: 9 AM UTC)
2. Gather content from all sources
3. Generate 3 post variations using AI
4. Save posts as HTML and TXT files in `./generated_posts/`
5. You can then manually post to LinkedIn

## 📊 Daily Workflow

### Option A: Scheduled (Recommended)
```bash
# Terminal 1: Start scheduler
python main.py --schedule
# Runs automatically daily at 9 AM
```

Then daily:
1. Check `./generated_posts/` for today's posts
2. Copy your preferred post to LinkedIn
3. Log engagement when post gets views

### Option B: Manual
```bash
# Whenever you want to generate
python main.py --generate
python main.py --today
# Copy and post manually
```

## 📈 Logging Engagement (Important!)

To get AI recommendations, you need to log post metrics:

```bash
python main.py --log-post
```

Then enter:
- LinkedIn post URL
- Views, Likes, Comments, Shares
- Content type (tips, question, news, thread)
- Topic (optional)

After 5-10 posts with metrics, you can get recommendations:

```bash
python main.py --analytics
```

## 🔄 Workflow Diagram

```
DAY 1:
┌─────────────────────────────────────────┐
│ Agent Gathers Content                   │
│ (9 AM or manual --generate)             │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ Generates 3 Post Variations             │
│ (HTML + TXT formats)                    │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ You Copy Best Post to LinkedIn          │
│ (Use LinkedIn's scheduler if available) │
└─────────────┬───────────────────────────┘
              ↓

DAY 2:
┌─────────────────────────────────────────┐
│ Post Gets Views/Likes/Comments          │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ You Log Metrics                         │
│ (python main.py --log-post)             │
└─────────────┬───────────────────────────┘
              ↓

AFTER 5-10 POSTS:
┌─────────────────────────────────────────┐
│ View Analytics & Get Recommendations    │
│ (python main.py --analytics)            │
│ - Best performing topics                │
│ - Optimal posting times                 │
│ - Content type recommendations          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ Adjust Strategy Based on AI Insights    │
│ - Generate more of high-performing type │
│ - Post at optimal times                 │
│ - Focus on winning topics               │
└─────────────────────────────────────────┘
```

## 📁 Important Directories

- **`./generated_posts/`** - Daily generated posts (HTML + TXT)
- **`./data/`** - SQLite database (auto-created)
- **`./logs/`** - Agent logs for debugging

## 🐛 Common Issues

**Issue**: Agent says API key not configured
```
Solution: Check that OPENROUTER_API_KEY is set in .env file
```

**Issue**: No content being gathered
```
Solution: Check internet connection and API keys
Run: python main.py --generate (for manual test)
Check: logs/linkedin_agent.log for detailed errors
```

**Issue**: Generated posts look generic
```
Solution: This is normal initially. As you log more metrics,
the AI learns your audience and generates better content.
Ensure you're logging at least 10+ posts with metrics.
```

**Issue**: Want to change posting time
```
Solution: Edit .env file
SCHEDULE_TIME=14:00  # For 2 PM
SCHEDULE_TIMEZONE=America/New_York  # Your timezone
Restart scheduler
```

## 💡 Pro Tips

1. **Post Regularly**: Daily posts get more traction than weekly
2. **Log Metrics Early**: Start logging after first 2-3 posts
3. **Review Variations**: Agent generates 3 options - pick the best
4. **Use Hashtags**: Don't remove auto-generated hashtags
5. **Engage Back**: Comment on similar posts to increase visibility
6. **Time Posts**: Use analytics to find your peak times
7. **Mix Content**: Vary between tips, questions, news, threads

## 📞 Support

For troubleshooting:
1. Check `logs/linkedin_agent.log`
2. Review README.md for detailed documentation
3. Verify `.env` configuration
4. Test with `python main.py --generate`

---

**Ready? Start with:**
```bash
python main.py --schedule
```

**Questions? Check:**
```bash
python main.py --help
```

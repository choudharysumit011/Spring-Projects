# 🤖 LinkedIn Growth Agent

An intelligent automation agent that gathers tech insights, generates engaging LinkedIn content, and provides analytics-driven recommendations to grow your professional presence.

## ✨ Features

### 1. 📥 Multi-Source Content Gathering
- **NewsAPI**: Latest technology and AI news
- **HackerNews**: Trending tech discussions and insights
- **Reddit**: Tech communities (r/webdev, r/devops, r/MachineLearning, r/programming)
- **Dev.to**: Developer articles and tutorials
- **Medium**: Technical blogs and essays
- **Web Crawlers**: Scrape latest SDE interview questions from LeetCode and HackerRank

### 2. ✍️ AI-Powered Content Generation
- Uses **OpenRouter LLM API** to generate unique LinkedIn posts
- Access to multiple models: Claude, GPT-4, Mistral, LLaMA
- Generates multiple post variations (tips, questions, insights, threads)
- Auto-adds relevant hashtags and CTAs
- Professional yet conversational tone suitable for software engineers

### 3. 📱 Manual LinkedIn Posting
- Since LinkedIn doesn't provide direct API access to profiles, the agent:
  - Generates formatted posts ready for copy-paste
  - Creates HTML and text versions for easy viewing
  - Allows scheduled posting via LinkedIn's native scheduler
  - Tracks post URLs and engagement

### 4. 📊 Analytics & Recommendations
- Track post engagement (views, likes, comments, shares)
- Analyze performance by content type and topic
- AI-powered weekly recommendations for content strategy
- Identify best-performing topics and posting times

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenRouter API key (free models available): https://openrouter.ai/
- Optional: NewsAPI key for better news coverage: https://newsapi.org/

### Installation

1. **Clone or setup the project**
```bash
cd Linkedin-Agent
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
# IMPORTANT: Set OPENROUTER_API_KEY
```

### Configuration

Edit `.env` file with your settings:

```env
# Required
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=mistral/mistral-7b-instruct  # Cost-effective option

# Optional but recommended
NEWSAPI_KEY=your_newsapi_key_here

# Customize schedule
SCHEDULE_TIME=09:00              # When to generate posts (24-hour format)
SCHEDULE_TIMEZONE=UTC           # Your timezone

# Content preferences
MAX_INTERVIEW_QUESTIONS=5
MAX_NEWS_ITEMS=10
GENERATE_POST_VARIATIONS=3
```

## 📖 Usage

### 1. **Start the Scheduler** (Automated Daily)
```bash
python main.py --schedule
```
- Generates posts automatically at configured time (default: 9 AM)
- Runs weekly analytics analysis every Monday
- Keeps running in background (press Ctrl+C to stop)

### 2. **Manually Generate Posts**
```bash
python main.py --generate
```
- Instantly gather content and generate posts
- Useful for testing or generating on-demand

### 3. **View Today's Posts**
```bash
python main.py --today
```
- Display all posts generated today
- Shows post type, content, and hashtags

### 4. **Log Engagement Metrics**
```bash
python main.py --log-post
```
- Log views, likes, comments, shares for a posted content
- Helps the AI learn what works best
- Interactive prompt to enter metrics

Example:
```
Enter the LinkedIn post URL: https://linkedin.com/feed/update/...
Views: 250
Likes: 15
Comments: 3
Shares: 2
Content type: tips
Topic: career-development
```

### 5. **View Analytics & Recommendations**
```bash
python main.py --analytics
```
- Shows engagement statistics for last 30 days
- Performance breakdown by content type and topic
- AI-powered recommendations for content strategy

View analytics for specific period:
```bash
python main.py --analytics --days 7
```

### 6. **Get Help**
```bash
python main.py --help
```

## 📂 Project Structure

```
linkedin-agent/
├── main.py                      # CLI entry point and scheduler
├── config.py                    # Configuration and constants
├── database.py                  # SQLite database management
├── content_gatherer.py          # Multi-source content fetching
├── content_generator.py         # LLM-based post generation
├── manual_linkedin_handler.py   # LinkedIn posting workflow
├── analytics_tracker.py         # Analytics and recommendations
├── scheduler.py                 # APScheduler setup
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .env                         # Your configuration (create from .env.example)
├── data/                        # SQLite database (created at runtime)
├── logs/                        # Agent logs
└── generated_posts/             # Daily generated posts (HTML + TXT)
```

## 🔧 Architecture

### Content Flow

```
1. GATHERING (Daily at configured time)
   ├─ Fetch from NewsAPI
   ├─ Fetch from HackerNews
   ├─ Scrape Reddit threads
   ├─ Fetch Dev.to articles
   ├─ Scrape Medium posts
   └─ Store in SQLite for deduplication

2. GENERATION
   ├─ Prepare content summary
   ├─ Call OpenRouter LLM API
   ├─ Generate 3 post variations
   └─ Save to database

3. MANUAL POSTING
   ├─ Create HTML version for viewing
   ├─ Create TXT version for copy-paste
   └─ User manually posts to LinkedIn

4. ANALYTICS
   ├─ User logs engagement metrics
   ├─ Analyze patterns by type and topic
   └─ AI generates recommendations
```

## 💡 Tips for Success

### Content Strategy
1. **Mix Post Types**: Rotate between tips, questions, insights, and threads
2. **Optimal Timing**: Log metrics and use analytics to find when your audience is most active
3. **Engagement**: End posts with questions or CTAs to encourage comments
4. **Consistency**: Post daily for better algorithm favor

### Quality Posts
1. **Review Variations**: Agent generates 3 versions - pick the best one
2. **Customize if Needed**: You can edit posts before posting to LinkedIn
3. **Hashtags**: Use the auto-generated hashtags or add your own (5-10 optimal)
4. **Links**: Add relevant documentation or article links when appropriate

### Analytics Usage
1. **Log Regularly**: Log metrics from at least 5-10 posts for meaningful recommendations
2. **Review Weekly**: Check recommendations every Monday
3. **A/B Test**: Try different content types and compare performance
4. **Iterate**: Implement recommendations and track improvement

## 🔑 API Keys & Costs

### OpenRouter (REQUIRED)
- **Cost**: Pay-as-you-go, free tier available
- **Signup**: https://openrouter.ai/
- **Models**: Access to Mistral, Claude, GPT-4, LLaMA, etc.
- **Estimate**: ~$0.001-0.01 per post generation
- **Recommendation**: Set spending limit on OpenRouter dashboard

### NewsAPI (Optional)
- **Cost**: Free tier (100 requests/day)
- **Signup**: https://newsapi.org/
- **Benefit**: Better news coverage with categories and sources

### Reddit (Free)
- **Cost**: Completely free
- **Authentication**: Optional for public subreddits
- **Signup**: https://www.reddit.com/prefs/apps

## 🐛 Troubleshooting

### Agent won't start
```
❌ Error: OPENROUTER_API_KEY not set
```
- Set `OPENROUTER_API_KEY` in `.env` file
- Make sure `.env` is in the same directory as `main.py`

### API rate limits
- Add delay with `REQUEST_DELAY=3` in `.env`
- Cache duration: `CACHE_DURATION=24` (reuse content within 24 hours)

### No content gathered
- Check internet connection
- Verify API keys in `.env`
- Check logs: `logs/linkedin_agent.log`
- Run with `--generate` to test manually

### Posts not generating
- Verify `OPENROUTER_API_KEY` is valid
- Check `OPENROUTER_MODEL` is available
- Check logs for specific errors
- Try with `--generate` for immediate feedback

### Analytics not available
- Need at least 5+ posts with logged metrics
- Use `python main.py --log-post` to add engagement data
- Check database: `data/linkedin_agent.db`

## 📊 Example Output

### Generated Posts
```
================================================================================
Post #1
================================================================================
Type: tips
Title: 5 Java Performance Tips for SDE-2 Interviews

Content:
Just realized something while reviewing production issues today...

Most SDE-2 candidates stumble on Java performance questions because they skip 
one crucial step: understanding GC behavior.

Here's what I always ask myself:
1. What's the heap size? (Default: 1/4 system RAM)
2. Is it Full GC or Minor GC?
3. Can I tune -Xms and -Xmx?

Most people optimize code when the real issue is GC tuning. 

What's your biggest Java performance gotcha? 👇

Hashtags:
#Java #SoftwareEngineering #Interview #Performance #BackendDevelopment
```

### Analytics Report
```
================================================================================
LinkedIn Post Analytics Report (Last 30 Days)
================================================================================

📊 Overall Statistics:
   Total Posts: 12
   Avg Views: 245
   Avg Likes: 18
   Avg Comments: 2.5
   Avg Shares: 1.2

📝 Performance by Content Type:
   tips:
      Posts: 5
      Avg Views: 310
      Avg Likes: 24
      Avg Comments: 3.2
      Avg Engagement Rate: 8.71%

   question:
      Posts: 4
      Avg Views: 180
      Avg Likes: 12
      Avg Comments: 2.0
      Avg Engagement Rate: 7.78%
```

## 🤝 Contributing

Have ideas for improvements? Feel free to:
1. Add support for more content sources
2. Improve post generation prompts
3. Add more analytics features
4. Create better HTML templates

## 📝 License

MIT License - Feel free to use and modify

## 🙏 Acknowledgments

- OpenRouter for unified LLM access
- NewsAPI for technology news
- HackerNews for trending discussions
- Dev.to and Medium for developer content
- Reddit for community insights

## 📞 Support

For issues or questions:
1. Check logs: `logs/linkedin_agent.log`
2. Verify configuration in `.env`
3. Try `python main.py --help` for command reference
4. Run with `--generate` to test components

---

**Happy posting! 🚀 Monitor your growth with analytics and adapt your strategy daily.**

# ✅ LinkedIn Agent - Setup Checklist

Complete this checklist to get your agent running in 15 minutes.

## 🎯 Phase 1: Environment Setup (5 minutes)

- [ ] **Step 1.1**: Activate Python virtual environment
  ```bash
  # Windows
  venv\Scripts\activate
  # macOS/Linux
  source venv/bin/activate
  ```

- [ ] **Step 1.2**: Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
  Expected: All 8 packages install successfully

- [ ] **Step 1.3**: Create `.env` file
  ```bash
  cp .env.example .env
  ```
  Expected: `.env` file appears in project root

## 🔑 Phase 2: API Keys Setup (5 minutes)

### Required: OpenRouter

- [ ] **Step 2.1**: Get OpenRouter API key
  1. Go to https://openrouter.ai/
  2. Sign up (email/GitHub)
  3. Go to Settings → API Keys
  4. Create and copy API key

- [ ] **Step 2.2**: Add to `.env`
  ```
  OPENROUTER_API_KEY=sk-or-your-key-here
  ```

### Optional but Recommended: NewsAPI

- [ ] **Step 2.3**: Get NewsAPI key (optional)
  1. Go to https://newsapi.org/
  2. Click "Get API Key"
  3. Enter email → Subscribe (free)
  4. Copy API key

- [ ] **Step 2.4**: Add to `.env` (optional)
  ```
  NEWSAPI_KEY=abc123your-key-here
  ```

### Optional: Reddit API

- [ ] **Step 2.5**: Set up Reddit (optional for better discussions)
  1. Go to https://www.reddit.com/prefs/apps
  2. Create new app (type: script)
  3. Copy Client ID and Secret

- [ ] **Step 2.6**: Add to `.env` (optional)
  ```
  REDDIT_CLIENT_ID=your-id
  REDDIT_CLIENT_SECRET=your-secret
  REDDIT_USER_AGENT=LinkedInAgent/1.0 (by You)
  ```

## 🧪 Phase 3: Verification (3 minutes)

- [ ] **Step 3.1**: Check if agent initializes
  ```bash
  python main.py
  ```
  Expected: Shows agent status without errors

- [ ] **Step 3.2**: Test content generation
  ```bash
  python main.py --generate
  ```
  Expected: 
  - Gathers content from sources
  - Generates 3 post variations
  - Creates files in `generated_posts/`

- [ ] **Step 3.3**: View generated posts
  ```bash
  python main.py --today
  ```
  Expected: Displays today's generated posts

- [ ] **Step 3.4**: Check generated files
  - Navigate to `./generated_posts/` folder
  - Find `linkedin_posts_YYYY-MM-DD.html`
  - Open in browser (should be nicely formatted)
  - Open `linkedin_posts_YYYY-MM-DD.txt`
  - Both should have your generated posts

## 🚀 Phase 4: Start Automation (1 minute)

- [ ] **Step 4.1**: Start the scheduler
  ```bash
  python main.py --schedule
  ```
  Expected: 
  - Message: "✅ Scheduler started"
  - Runs in background
  - Press Ctrl+C to stop

- [ ] **Step 4.2**: Scheduler will run daily at 9 AM (UTC)
  - To change time: Edit `.env`, set `SCHEDULE_TIME=HH:MM`
  - Restart scheduler

## 📱 Phase 5: Daily Workflow (After Day 1)

- [ ] **Day 1**: Generated posts are ready
  1. Check `./generated_posts/` folder
  2. Open HTML file in browser
  3. Click "Copy Post & Hashtags"
  4. Go to LinkedIn.com
  5. Click "Start a post"
  6. Paste content
  7. Click "Post" or "Schedule post"

- [ ] **After posting**: Log engagement
  ```bash
  python main.py --log-post
  ```
  When prompted:
  - Enter LinkedIn post URL
  - Enter: Views, Likes, Comments, Shares
  - Content type: tips/question/news/thread
  - Topic: your description (optional)

- [ ] **After 5-10 posts**: View analytics
  ```bash
  python main.py --analytics
  ```
  See: Performance by type, topic, and AI recommendations

## 🎯 Verification Checklist

### Python & Packages
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] `requirements.txt` packages installed (no errors)
- [ ] `pip list` shows all 8 packages

### Configuration
- [ ] `.env` file created
- [ ] `OPENROUTER_API_KEY` set (required)
- [ ] `NEWSAPI_KEY` set (optional but recommended)
- [ ] Other optional keys set as needed

### Files
- [ ] All 8 Python modules exist
- [ ] `requirements.txt` present
- [ ] `.env.example` present
- [ ] Documentation files present

### Functionality
- [ ] `python main.py` runs without errors
- [ ] `python main.py --generate` creates posts
- [ ] `python main.py --today` shows posts
- [ ] `generated_posts/` folder has files

### Scheduler
- [ ] `python main.py --schedule` starts
- [ ] No errors in console
- [ ] Ready for daily automation

## 🐛 Troubleshooting

### Error: "OPENROUTER_API_KEY not set"
**Solution**: 
1. Check `.env` file exists
2. Check `OPENROUTER_API_KEY=...` is set
3. Run: `python main.py` (to verify)

### Error: "No content generated"
**Solution**:
1. Check internet connection
2. Check API keys are valid
3. Check logs: `logs/linkedin_agent.log`
4. Try again with `python main.py --generate`

### Error: "ModuleNotFoundError: No module named 'requests'"
**Solution**:
1. Confirm virtual environment is activated
2. Run: `pip install -r requirements.txt`
3. Verify: `pip list` (should show all packages)

### Error: "Database error"
**Solution**:
1. Delete `data/` folder (will recreate)
2. Delete `logs/` folder (will recreate)
3. Run: `python main.py --generate`

### Agent runs but no posts generated
**Solution**:
1. Check API keys are valid
2. Check internet connection
3. Check logs: `tail logs/linkedin_agent.log`
4. Verify each API separately
5. Increase verbosity: `LOG_LEVEL=DEBUG` in `.env`

## 📊 Success Indicators

### ✅ Setup Successful
- [ ] No errors when running `python main.py`
- [ ] `python main.py --generate` completes
- [ ] HTML/TXT files created in `generated_posts/`
- [ ] Files contain formatted posts with hashtags

### ✅ Ready for Daily Use
- [ ] Scheduler starts with `python main.py --schedule`
- [ ] Posts are generated daily at configured time
- [ ] Can view posts with `python main.py --today`
- [ ] Can log metrics with `python main.py --log-post`
- [ ] Can view analytics with `python main.py --analytics`

## 🎯 Next Steps (After Checklist)

1. **Now**: Review generated posts in `generated_posts/` folder
2. **Today**: Post your first generated content to LinkedIn
3. **Tomorrow**: Post the second day's content
4. **This Week**: Log metrics from 5+ posts
5. **Next Week**: Run analytics to see recommendations

## 📞 Quick Reference

| Command | Purpose |
|---------|---------|
| `python main.py` | Check status |
| `python main.py --schedule` | Start daily automation |
| `python main.py --generate` | Generate now |
| `python main.py --today` | View today's posts |
| `python main.py --log-post` | Log engagement |
| `python main.py --analytics` | View recommendations |
| `python main.py --help` | All commands |

## 📁 Important Directories

| Directory | Purpose |
|-----------|---------|
| `./venv/` | Python virtual environment |
| `./data/` | SQLite database (auto-created) |
| `./logs/` | Debug logs (auto-created) |
| `./generated_posts/` | Daily posts HTML+TXT (auto-created) |
| `./.env` | Your configuration (create from .env.example) |

## ⏰ Estimated Time

- **Total Setup**: 15 minutes
- **Daily Time**: 1-2 minutes (copy-paste post)
- **Weekly Time**: 5 minutes (review analytics)

## 🎉 You're Done When:

✅ Agent initialized successfully
✅ Posts generated without errors
✅ Posts visible in `generated_posts/`
✅ Scheduler running in background
✅ First post copied to LinkedIn

**Now go to QUICKSTART.md or start with:**
```bash
python main.py --schedule
```

---

**Need help? Check:**
- QUICKSTART.md - Quick start guide
- API_SETUP_GUIDE.md - API key instructions
- README.md - Full documentation
- INDEX.md - Navigation guide

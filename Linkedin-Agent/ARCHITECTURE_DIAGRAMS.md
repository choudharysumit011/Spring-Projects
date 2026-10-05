# LinkedIn Agent - Architecture & Flow Diagrams

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LINKEDIN GROWTH AGENT v1.0                       │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ INPUT SOURCES (Content Gathering)                                    │
├──────────────────────────────────────────────────────────────────────┤
│ ├─ 📰 NewsAPI (Tech News)                                            │
│ ├─ 🔗 HackerNews (Discussions)                                       │
│ ├─ 👥 Reddit/PRAW (Community)                                        │
│ ├─ 👨‍💻 Dev.to (Articles)                                            │
│ ├─ 📖 Medium RSS (Blogs)                                             │
│ └─ 🎓 LeetCode/HackerRank (Interview Q's)                           │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ content_gatherer.py - Multi-Source Content Fetcher                   │
├──────────────────────────────────────────────────────────────────────┤
│ • Fetch from APIs and web crawlers                                    │
│ • Deduplicate content                                                │
│ • Store in database                                                   │
│ • Handle rate limiting & caching                                      │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ database.py - Content Storage (SQLite)                               │
├──────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────┐                                   │
│ │ Table: gathered_content         │ (15+ items daily)                │
│ │ ├─ News items                   │                                   │
│ │ ├─ Interview questions          │                                   │
│ │ ├─ Reddit discussions           │                                   │
│ │ ├─ Dev blog posts               │                                   │
│ │ └─ Trending articles            │                                   │
│ └─────────────────────────────────┘                                   │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ content_generator.py - AI Post Generation (OpenRouter LLM)            │
├──────────────────────────────────────────────────────────────────────┤
│ 1. Summarize gathered content                                         │
│ 2. Call OpenRouter API (Multiple Models Available)                   │
│    ├─ Mistral (Cost-effective)                                       │
│    ├─ Claude                                                          │
│    ├─ GPT-4                                                           │
│    └─ LLaMA                                                           │
│ 3. Generate 3 variations:                                             │
│    ├─ Tips & Tricks                                                   │
│    ├─ Questions & Discussion                                          │
│    └─ News Insights                                                   │
│ 4. Add hashtags, CTAs, formatting                                    │
│ 5. Save to database                                                   │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ database.py - Generated Posts Storage                                 │
├──────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────┐                                   │
│ │ Table: generated_posts          │ (3 variations daily)             │
│ │ ├─ Post content                 │                                   │
│ │ ├─ Post type                    │                                   │
│ │ ├─ Hashtags                     │                                   │
│ │ ├─ Generated timestamp          │                                   │
│ │ └─ Posting status               │                                   │
│ └─────────────────────────────────┘                                   │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ manual_linkedin_handler.py - Posting Workflow (No API)                │
├──────────────────────────────────────────────────────────────────────┤
│ 1. Generate HTML file (browser-friendly)                             │
│ 2. Generate TXT file (copy-paste ready)                              │
│ 3. Save to generated_posts/ folder                                   │
│ 4. User opens and reviews                                             │
│ 5. User copies favorite variation                                     │
│ 6. User pastes to LinkedIn.com                                        │
│ 7. User posts or schedules                                            │
│ 8. User provides post URL to agent                                    │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
        📱 LINKEDIN.COM (Manual Posting)
        User copies post, pastes to LinkedIn, posts
               │
               ▼
        📊 ENGAGEMENT HAPPENS
        Views, Likes, Comments, Shares accumulate
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ analytics_tracker.py - Engagement Logging                             │
├──────────────────────────────────────────────────────────────────────┤
│ User runs: python main.py --log-post                                  │
│ ├─ Enter post URL                                                     │
│ ├─ Enter views, likes, comments, shares                              │
│ ├─ Enter content type & topic                                        │
│ └─ Store in database                                                  │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ database.py - Analytics Storage                                       │
├──────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────┐                                   │
│ │ Table: post_analytics           │ (Logged by user)                │
│ │ ├─ Post URL                     │                                   │
│ │ ├─ Views, Likes, Comments       │                                   │
│ │ ├─ Content type                 │                                   │
│ │ ├─ Topic/Tags                   │                                   │
│ │ └─ Engagement timestamp         │                                   │
│ └─────────────────────────────────┘                                   │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ content_generator.py - AI Analysis & Recommendations                  │
├──────────────────────────────────────────────────────────────────────┤
│ (Weekly, Automatic)                                                   │
│ 1. Fetch analytics from database                                      │
│ 2. Calculate performance metrics:                                     │
│    ├─ Avg views per post type                                        │
│    ├─ Engagement rate by topic                                       │
│    └─ Trend analysis                                                  │
│ 3. Call OpenRouter LLM for analysis                                  │
│ 4. Generate recommendations:                                          │
│    ├─ Best performing topics                                         │
│    ├─ Optimal posting times                                          │
│    ├─ Content format suggestions                                     │
│    └─ Strategy adjustments                                           │
│ 5. Display to user                                                    │
└──────────────┬───────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│ OUTPUT - User Recommendations                                         │
├──────────────────────────────────────────────────────────────────────┤
│ "Based on 10 posts analyzed:                                          │
│  • Tips posts get 20% more engagement                                │
│  • Best time to post: 9 AM - 11 AM                                   │
│  • Focus on: AI, Performance, Architecture topics                    │
│  • Try thread format for complex topics"                             │
└──────────────┴───────────────────────────────────────────────────────┘
```

## 📅 Daily Workflow Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        DAY 1                                     │
└─────────────────────────────────────────────────────────────────┘

9:00 AM (AUTOMATIC)
│
├─ 🔄 Gather content
│  ├─ NewsAPI: 10 news items
│  ├─ HackerNews: 5 trending
│  ├─ Reddit: 5 discussions
│  ├─ Dev.to: 5 articles
│  └─ Medium: 5 posts
│
├─ 🤖 Generate posts (OpenRouter LLM)
│  ├─ Summarize 25+ items
│  ├─ Create 3 variations
│  ├─ Add hashtags & CTAs
│  └─ Save to database
│
├─ 💾 Create output files
│  ├─ generated_posts/linkedin_posts_YYYY-MM-DD.html
│  └─ generated_posts/linkedin_posts_YYYY-MM-DD.txt
│
└─ ✅ Done (automated)

9:15 AM (USER ACTION)
│
├─ 📂 User opens generated_posts/ folder
├─ 🌐 Opens HTML file in browser
├─ 👀 Reviews 3 post variations
├─ ✍️  Picks favorite post
├─ 📋 Copies post & hashtags
├─ 🔗 Goes to LinkedIn.com
├─ ✏️  Clicks "Start a post"
├─ 📝 Pastes content
├─ 🚀 Clicks "Post" or "Schedule"
└─ 📌 Notes the post URL

DAY 2-6 (POSTS GET ENGAGEMENT)
│
├─ Views accumulate: 200, 300, 250...
├─ Likes: 15, 22, 18...
├─ Comments: 2, 3, 4...
└─ Shares: 1, 2, 1...

DAY 7 (USER ACTION - LOGGING)
│
├─ 📊 User runs: python main.py --log-post
├─ 📝 Enters post URL from day 1
├─ 🔢 Enters metrics:
│  ├─ Views: 250
│  ├─ Likes: 18
│  ├─ Comments: 3
│  ├─ Shares: 1
│  ├─ Type: "tips"
│  └─ Topic: "Java Performance"
└─ ✅ Logged to database

WEEK 2 (REPEATS)
│
├─ Days 8-14: Repeat above cycle
├─ More content generated
├─ More posts created
├─ More metrics logged
└─ Pattern building

WEEK 3 (ANALYTICS)
│
├─ 🤖 Monday 9 AM (AUTOMATIC)
├─ Analyze 10-15 posts
├─ Calculate averages by type
├─ Run LLM analysis
├─ Generate recommendations
└─ Display to user

USER SEES:
"Tips posts: 310 avg views (best!)
Question posts: 180 avg views
News posts: 200 avg views

Recommendation: Post more tips content!"

WEEK 4+ (OPTIMIZATION)
│
└─ User generates more tips posts
   (based on recommendations)
```

## 🔄 Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                    │
└──────────────────────────────────────────────────────────────────────┘

EXTERNAL APIs              AGENT PROCESSING              USER INTERACTION
─────────────              ──────────────                ────────────────

NewsAPI                                                       
    │                    content_gatherer.py
    ├─────────────────►  ├─ Fetch & parse
    │                    ├─ Deduplicate
HackerNews                ├─ Store in DB
    │                    │
    ├─────────────────►  database.py
    │                    ├─ gathered_content
Reddit                    │   (15+ items daily)
    │                    │
    ├─────────────────►  content_generator.py
    │                    ├─ Summarize
Dev.to                    ├─ Call OpenRouter
    │                    ├─ Generate 3 posts
    ├─────────────────►  │
    │                    database.py
Medium                    ├─ generated_posts
    │                    │   (3 items daily)
    └─────────────────►  │
                         manual_linkedin_handler.py
                         ├─ Create HTML file     ◄─── User opens
                         ├─ Create TXT file      ◄─── User copies
                         │
                         (User posts to LinkedIn)
                         │
                         User logs metrics       ◄─── python main.py --log-post
                         │
                         database.py
                         ├─ post_analytics
                         │   (views, likes, etc)
                         │
                         analytics_tracker.py
                         ├─ Analyze patterns
                         ├─ Call OpenRouter
                         │
                         User views report       ◄─── python main.py --analytics
```

## 🔧 Component Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│ main.py (CLI Entry Point)                                       │
│ ├─ scheduler.py ─────────────────────────────────────┐         │
│ │                                                    │          │
│ │  ┌─────────────────────────────────────────────┐  │          │
│ │  │ scheduler.daily_content_generation_job()    │  │          │
│ │  │ 1. calls content_gatherer.gather_all()      │  │          │
│ │  │ 2. calls content_generator.generate_posts() │  │          │
│ │  │ 3. calls manual_linkedin_handler.prepare()  │  │          │
│ │  └─────────────────────────────────────────────┘  │          │
│ │                                                    │          │
│ │  ┌─────────────────────────────────────────────┐  │          │
│ │  │ scheduler.weekly_analytics_job()             │  │          │
│ │  │ 1. calls analytics_tracker.display_report()  │  │          │
│ │  │ 2. calls analytics_tracker.display_recs()    │  │          │
│ │  └─────────────────────────────────────────────┘  │          │
│ │                                                    │          │
│ └─────────────────────────────────────────────────────┘         │
│                                                                  │
│ ├─ config.py (All settings)                                    │
│ ├─ database.py (SQLite operations)                             │
│ ├─ content_gatherer.py (Fetch content)                         │
│ ├─ content_generator.py (Generate posts + analysis)           │
│ ├─ manual_linkedin_handler.py (Posting workflow)               │
│ └─ analytics_tracker.py (Metrics & recommendations)            │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Database Schema

```
┌──────────────────────────────────────────────────────────────────┐
│                    linkedin_agent.db (SQLite)                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ TABLE: gathered_content                                          │
│ ├─ id (PK)                                                       │
│ ├─ source (NewsAPI, HackerNews, Reddit, Dev.to, Medium)         │
│ ├─ title                                                         │
│ ├─ url (UNIQUE)                                                  │
│ ├─ content                                                       │
│ ├─ category (tech_news, discussions, articles)                  │
│ ├─ created_at                                                    │
│ └─ updated_at                                                    │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ TABLE: generated_posts                                           │
│ ├─ id (PK)                                                       │
│ ├─ title                                                         │
│ ├─ content                                                       │
│ ├─ post_type (tips, question, news, thread)                    │
│ ├─ tags                                                          │
│ ├─ hashtags                                                      │
│ ├─ generated_at                                                  │
│ ├─ posted (boolean)                                              │
│ ├─ posted_at                                                     │
│ ├─ posted_url (LinkedIn post link)                              │
│ └─ variation_index                                               │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ TABLE: post_analytics                                            │
│ ├─ id (PK)                                                       │
│ ├─ post_id (FK)                                                  │
│ ├─ post_url                                                      │
│ ├─ post_content                                                  │
│ ├─ post_date                                                     │
│ ├─ topic                                                         │
│ ├─ content_type (tips, question, news, thread)                 │
│ ├─ views                                                         │
│ ├─ likes                                                         │
│ ├─ comments                                                      │
│ ├─ shares                                                        │
│ └─ updated_at                                                    │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ TABLE: content_cache                                             │
│ ├─ id (PK)                                                       │
│ ├─ source                                                        │
│ ├─ cache_key                                                     │
│ ├─ data                                                          │
│ ├─ created_at                                                    │
│ └─ expires_at (24 hours default)                                │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ TABLE: analytics_recommendations                                 │
│ ├─ id (PK)                                                       │
│ ├─ analysis_date                                                 │
│ ├─ topic                                                         │
│ ├─ content_type                                                  │
│ ├─ avg_views                                                     │
│ ├─ avg_engagement_rate                                           │
│ ├─ recommendation (AI-generated text)                           │
│ └─ created_at                                                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 🎯 State Machine: Post Lifecycle

```
┌──────────────┐
│   GATHERED   │ (In database)
└────────┬─────┘
         │ content_gatherer.py
         ▼
┌──────────────┐
│  GENERATED   │ (3 variations created)
└────────┬─────┘
         │ manual_linkedin_handler.py
         ▼
┌──────────────┐
│  FORMATTED   │ (HTML + TXT files ready)
└────────┬─────┘
         │ User action
         ▼
┌──────────────┐
│   COPIED     │ (User copies from HTML/TXT)
└────────┬─────┘
         │ User action
         ▼
┌──────────────┐
│   POSTED     │ (Manually posted to LinkedIn)
└────────┬─────┘
         │ User provides URL
         ▼
┌──────────────┐
│ ENGAGEMENT   │ (Views, Likes, Comments accumulate)
└────────┬─────┘
         │ User logs metrics
         ▼
┌──────────────┐
│  ANALYZED    │ (Analytics & recommendations)
└──────────────┘
```

---

**For more details, see:**
- README.md - Feature documentation
- IMPLEMENTATION_SUMMARY.md - Technical details
- QUICKSTART.md - Setup guide

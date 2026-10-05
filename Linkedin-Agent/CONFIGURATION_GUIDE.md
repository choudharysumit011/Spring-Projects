# Configuration Guide - Customize Content Sources

This guide shows you exactly WHERE to configure what content the agent gathers and generates.

---

## 🎯 Content Configuration Files

### File 1: `config.py` - Main Configuration
**Location**: `D:\Spring-small-projects\Linkedin-Agent\config.py`

This file controls:
- Interview question sources
- News sources
- Post generation settings
- Scheduling
- Reddit subreddits

**Key Settings to Change**:

```python
# Number of interview questions to gather daily
MAX_INTERVIEW_QUESTIONS = 5  # Change to get more/less

# Number of news items to gather daily
MAX_NEWS_ITEMS = 10  # Change to get more/less

# Number of post variations to generate
GENERATE_POST_VARIATIONS = 3  # Change to 2-5

# Reddit subreddits to monitor
REDDIT_SUBREDDITS = [
    "webdev",           # Change these
    "devops",           # Add/remove
    "MachineLearning",  # as needed
    "programming",
    "learnprogramming",
    "golang",
    "Kubernetes",
]

# When to generate posts daily (24-hour format)
SCHEDULE_TIME = "09:00"  # Change to your preferred time

# Posting language
MAX_NEWS_ITEMS = 10
```

---

### File 2: `content_gatherer.py` - Content Sources
**Location**: `D:\Spring-small-projects\Linkedin-Agent\content_gatherer.py`

This file controls WHERE content is gathered from.

**Current Sources**:
1. **NewsAPI** - General tech news + SDE interviews (lines 97-145)
2. **HackerNews** - Trending tech discussions (lines 147-181)
3. **Reddit** - Tech community posts (lines 183-220)
4. **Dev.to** - Developer articles (lines 238-258)
5. **Medium** - Technical blogs (lines 260-295)
6. **SDE Interview News** - Interview preparation content (lines 51-115)

**How to Add a New Content Source**:

Example - Add GitHub Trending:

```python
def fetch_github_trending(self) -> List[Dict[str, Any]]:
    """Fetch trending repositories from GitHub"""
    try:
        url = "https://api.github.com/repos/trending"
        # ... add your code here ...
        return trending_repos
    except Exception as e:
        logger.error(f"Error fetching GitHub trending: {e}")
        return []
```

Then add to `gather_all_content()` method (line 42):

```python
def gather_all_content(self) -> Dict[str, List[Dict[str, Any]]]:
    content = {
        "news": [],
        "interview_questions": [],
        "reddit_discussions": [],
        "trending_dev_posts": [],
        "github_trending": [],  # ADD THIS
    }
    
    # ... existing code ...
    
    content["github_trending"] = self.fetch_github_trending()
    
    return content
```

---

### File 3: `content_generator.py` - Post Generation
**Location**: `D:\Spring-small-projects\Linkedin-Agent\content_generator.py`

This file controls HOW posts are generated and what they focus on.

**Key Section: LLM Prompts (lines 155-213)**

The prompts control what the AI focuses on:

```python
# Prompt 1: Interview-focused (variation 1)
f"""You are a LinkedIn content strategist for Full Stack Java Software Engineers (SDE-1, SDE-2, SDE-3 levels).
PRIMARY FOCUS: SDE interview preparation, interview questions, career development.
...
"""

# Prompt 2: Career coaching angle (variation 2)
f"""You are a technical thought leader and career coach on LinkedIn...
"""

# Prompt 3: Expert breakdown angle (variation 3)
f"""You are a developer advocate and SDE interview expert...
"""
```

**How to Change Post Focus**:

Edit any of the three prompts. For example, to focus on AI/ML:

```python
f"""You are an AI/ML expert creating content for software engineers.
PRIMARY FOCUS: AI/ML interview preparation, machine learning trends, deep learning.
...
"""
```

---

## 📋 Complete Content Configuration Checklist

### Interview Question Settings
- **File**: `config.py`
- **Setting**: `MAX_INTERVIEW_QUESTIONS = 5`
- **Change to**: Higher number = more interview Q's (e.g., 10)

### News Coverage
- **File**: `config.py`
- **Setting**: `MAX_NEWS_ITEMS = 10`
- **Change to**: Higher number = more news items (e.g., 15)

### Reddit Communities to Monitor
- **File**: `config.py`
- **Setting**: `REDDIT_SUBREDDITS = [...]`
- **Change to**: Add/remove subreddits like:
  ```python
  REDDIT_SUBREDDITS = [
      "devops",
      "docker",           # NEW
      "kubernetes",
      "adobeaitools",     # NEW
      "MachineLearning",
      "learnprogramming",
  ]
  ```

### Content Sources to Enable/Disable
- **File**: `content_gatherer.py`, method `gather_all_content()`
- **Line**: 42-64
- **Example**: To disable Reddit:
  ```python
  # Comment out these lines:
  # try:
  #     content["reddit_discussions"] = self.fetch_reddit_discussions()
  # except Exception as e:
  #     logger.warning(f"Failed to fetch Reddit discussions: {e}")
  ```

### Post Generation Focus
- **File**: `content_generator.py`
- **Method**: `_build_prompt()`, lines 155-213
- **How to change**: Edit the prompts to change what the AI focuses on

### Posting Schedule
- **File**: `config.py`
- **Setting**: `SCHEDULE_TIME = "09:00"`
- **Change to**: Different time:
  ```python
  SCHEDULE_TIME = "14:00"  # 2 PM instead of 9 AM
  ```

---

## 🔧 Common Configuration Examples

### Example 1: Focus More on Interviews
**File**: `content_generator.py`, line 165

Change:
```python
PRIMARY FOCUS: SDE interview preparation, interview questions, career development.
SECONDARY FOCUS: Latest tech/AI news and software engineering trends.
```

To:
```python
EXCLUSIVE FOCUS: SDE-1, SDE-2, SDE-3 interview preparation and questions.
Include: System design problems, coding challenges, interview tips, career advice.
IGNORE: General tech news, company announcements, unrelated trends.
```

---

### Example 2: Add Focus on Specific Technology
**File**: `content_generator.py`, line 165

Add to prompt:
```python
TECHNOLOGY FOCUS: Java, Spring Boot, Microservices, System Design, AWS
- Prioritize posts about Java-specific interview questions
- Focus on full-stack development with Java backend
- Include cloud architecture and scalability topics
```

---

### Example 3: Monitor Specific Reddit Communities
**File**: `config.py`, line 42

Replace `REDDIT_SUBREDDITS`:
```python
REDDIT_SUBREDDITS = [
    "golang",           # If focusing on Go
    "rust",             # If focusing on Rust
    "Kubernetes",       # DevOps topics
    "docker",           # Containerization
    "aws",              # Cloud
    "MachineLearning",  # AI/ML
]
```

---

### Example 4: Add Custom News Keywords
**File**: `content_gatherer.py`, method `_fetch_sde_interview_news()`, line 78

Add more keywords:
```python
interview_keywords = [
    "SDE interview questions",
    "software engineer interview",
    "interview preparation",
    "coding interview",
    "system design interview",
    "FAANG interview",      # NEW
    "leetcode problems",    # NEW
    "behavioral interview",  # NEW
]
```

---

## 📊 Quick Reference: What Generates What

| Content Type | Source File | Method | Lines |
|--------------|------------|--------|-------|
| News | content_gatherer.py | fetch_news() | 97-145 |
| Interview Q's | content_gatherer.py | fetch_interview_questions() | 51-82 |
| SDE Interviews | content_gatherer.py | _fetch_sde_interview_news() | 84-143 |
| Reddit | content_gatherer.py | fetch_reddit_discussions() | 145-177 |
| Dev Posts | content_gatherer.py | fetch_trending_dev_posts() | 179-194 |
| Dev.to | content_gatherer.py | _fetch_devto_posts() | 196-218 |
| Medium | content_gatherer.py | _fetch_medium_posts() | 220-254 |

---

## 🎯 Focus Areas by File

### To Change WHAT content is gathered:
→ Edit `content_gatherer.py`

### To Change HOW posts are generated:
→ Edit `content_generator.py` (prompts)

### To Change WHEN posts are generated:
→ Edit `config.py` (SCHEDULE_TIME)

### To Change HOW MUCH content:
→ Edit `config.py` (MAX_INTERVIEW_QUESTIONS, MAX_NEWS_ITEMS, etc.)

### To Change WHICH communities:
→ Edit `config.py` (REDDIT_SUBREDDITS)

---

## ✅ Verification

After making changes:

1. **Save the file** (Ctrl+S)
2. **Restart the agent**:
   ```bash
   python main.py --generate
   ```
3. **Check the output** in `generated_posts/`
4. **View logs** for errors:
   ```bash
   tail logs/linkedin_agent.log
   ```

---

## 📚 Example: Create Custom Interview Focus

To make the agent focus ONLY on SDE interviews:

**Step 1**: Edit `config.py`
```python
MAX_INTERVIEW_QUESTIONS = 10  # More interview questions
MAX_NEWS_ITEMS = 5            # Less general news
```

**Step 2**: Edit `content_generator.py`, line 165
```python
PRIMARY FOCUS: SDE interview preparation, interview questions, career development.
EXCLUSIVE: Ignore general tech news not related to interviews.
Focus on: System design, algorithms, coding problems, interview tips, career advice.
```

**Step 3**: Edit `content_gatherer.py`, disable news in `gather_all_content()`
```python
# Comment out:
# content["news"] = self.fetch_news()
```

**Step 4**: Run:
```bash
python main.py --generate
```

Now all posts will focus on SDE interviews! 🎯

---

## 🚀 Next Steps

1. **Test your changes**:
   ```bash
   python main.py --generate
   ```

2. **Review the posts** in `generated_posts/`

3. **Adjust as needed** and repeat

4. **Once happy, start scheduler**:
   ```bash
   python main.py --schedule
   ```

---

**All configuration is done in these 2 files:**
- ✅ `config.py` - Settings (what, when, how much)
- ✅ `content_gatherer.py` - Sources (where)
- ✅ `content_generator.py` - Generation (how)

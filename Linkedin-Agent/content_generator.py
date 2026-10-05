import requests
import json
import logging
from typing import List, Dict, Any
import config
from database import DatabaseManager

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generates LinkedIn posts using OpenRouter LLM"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.api_key = config.OPENROUTER_API_KEY
        self.model = config.OPENROUTER_MODEL
        self.base_url = config.OPENROUTER_BASE_URL

    def generate_posts(self, gathered_content: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, str]]:
        """Generate LinkedIn posts from gathered content"""
        if not self.api_key:
            logger.error("OpenRouter API key not configured")
            return []

        try:
            posts = []

            # Prepare content summary for LLM
            content_summary = self._prepare_content_summary(gathered_content)

            # Generate multiple variations
            for i in range(config.GENERATE_POST_VARIATIONS):
                logger.info(f"Generating post variation {i + 1}/{config.GENERATE_POST_VARIATIONS}")

                post = self._generate_single_post(content_summary, variation_index=i)
                if post:
                    posts.append(post)
                    # Save to database
                    self.db.insert_generated_post(
                        title=post.get("title", f"Post {i + 1}"),
                        content=post.get("content", ""),
                        post_type=post.get("post_type", "standard"),
                        tags=post.get("tags", ""),
                        hashtags=post.get("hashtags", ""),
                        variation_index=i,
                    )

            logger.info(f"Generated {len(posts)} post variations")
            return posts

        except Exception as e:
            logger.error(f"Error generating posts: {e}")
            return []

    def _prepare_content_summary(self, gathered_content: Dict[str, List[Dict[str, Any]]]) -> str:
        """Prepare a summary of gathered content for the LLM"""
        summary = "# Today's Content Summary\n\n"

        # Add interview questions
        if gathered_content.get("interview_questions"):
            summary += "## Interview Questions:\n"
            for q in gathered_content["interview_questions"][:config.MAX_INTERVIEW_QUESTIONS]:
                summary += f"- {q.get('title', '')}\n"
            summary += "\n"

        # Add news
        if gathered_content.get("news"):
            summary += "## Latest Tech News:\n"
            for n in gathered_content["news"][:config.MAX_NEWS_ITEMS]:
                summary += f"- {n.get('title', '')}: {n.get('content', '')}\n"
            summary += "\n"

        # Add Reddit discussions
        if gathered_content.get("reddit_discussions"):
            summary += "## Hot Reddit Discussions:\n"
            for r in gathered_content["reddit_discussions"][:5]:
                summary += f"- {r.get('title', '')} (from {r.get('source', '')})\n"
            summary += "\n"

        # Add trending dev posts
        if gathered_content.get("trending_dev_posts"):
            summary += "## Trending Dev Posts:\n"
            for p in gathered_content["trending_dev_posts"][:5]:
                summary += f"- {p.get('title', '')}\n"
            summary += "\n"

        return summary

    def _generate_single_post(self, content_summary: str, variation_index: int = 0) -> Dict[str, str]:
        """Generate a single LinkedIn post using OpenRouter API"""
        try:
            # Build the prompt
            prompt = self._build_prompt(content_summary, variation_index)

            # Prepare request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "temperature": 0.7 + (variation_index * 0.1),
                "max_tokens": 500,
            }

            logger.debug(f"OpenRouter request - Model: {self.model}, Prompt length: {len(prompt)}")

            # Call OpenRouter API
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )

            # Check for errors
            if response.status_code != 200:
                error_msg = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get("error", {}).get("message", error_msg)
                except:
                    pass
                logger.error(f"OpenRouter API Error ({response.status_code}): {error_msg}")
                return {}

            result = response.json()

            if result.get("choices") and len(result["choices"]) > 0:
                generated_text = result["choices"][0]["message"]["content"]

                # Parse the generated content
                post = self._parse_generated_content(generated_text)
                return post
            else:
                logger.error("No content in OpenRouter response")
                return {}

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error with OpenRouter: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error generating post with OpenRouter: {e}")
            return {}

    def _build_prompt(self, content_summary: str, variation_index: int) -> str:
        """Build the prompt for LLM"""
        prompts = [
            f"""You are a LinkedIn content strategist for Full Stack Java Software Engineers (SDE-1, SDE-2, SDE-3 levels).
PRIMARY FOCUS: SDE interview preparation, interview questions, career development.
SECONDARY FOCUS: Latest tech/AI news and software engineering trends.

Generate an engaging LinkedIn post based on the following content summary.
If the content includes interview questions or interview preparation tips, prioritize those.

The post should:
- Focus on interview preparation, interview questions, or career growth when available
- Be professional yet conversational  
- Include actionable insights or tips
- Mention relevant technologies (Java, System Design, Algorithms, etc.)
- Include 3-5 relevant hashtags (#SDE #Interview #JavaDeveloper #CareerGrowth)
- Be suitable for LinkedIn (250-400 words)
- Provide value to software engineers at all levels
- Include call-to-action (CTA) for engagement

Content to base the post on:
{content_summary}

Format your response as JSON with keys: "title", "content", "post_type", "tags", "hashtags"
post_type can be: "interview_question", "interview_tips", "career_advice", "news_insight", "technical_breakdown"
""",
            f"""You are a technical thought leader and career coach on LinkedIn targeting software engineers.
Your expertise: SDE interviews, career progression, technical interview preparation.

Create a LinkedIn post from the given content that:
- Focuses on SDE interview preparation or career development when possible
- Sparks discussion and engagement
- Asks a thought-provoking question related to interviews or tech careers
- Makes insights about interview preparation, system design, algorithms
- Uses personal experience or real interview stories where relevant
- Ends with a strong call-to-action (CTA)
- Include relevant hashtags (#Interview #SDE #CareerDevelopment #SystemDesign)

Content:
{content_summary}

Return JSON with: "title", "content", "post_type", "tags", "hashtags"
""",
            f"""You are a developer advocate and SDE interview expert creating LinkedIn content.
Generate a post that:
- Educates on interview preparation, coding problems, or system design
- Breaks down complex interview topics into digestible insights
- References specific Java, algorithm, or system design concepts
- Provides actionable interview preparation tips
- Focuses on SDE-1, SDE-2, SDE-3 level interview questions
- Includes relevant hashtags (#InterviewPrep #SystemDesign #AlgorithmsExplained #SDE)
- Ends with engagement CTA like "What's YOUR biggest interview challenge?"

Based on:
{content_summary}

Output as JSON: "title", "content", "post_type", "tags", "hashtags"
""",
        ]

        return prompts[variation_index % len(prompts)]

    def _parse_generated_content(self, generated_text: str) -> Dict[str, str]:
        """Parse the generated content from LLM response"""
        try:
            # Try to parse as JSON
            if "```json" in generated_text:
                json_str = generated_text.split("```json")[1].split("```")[0].strip()
            elif "{" in generated_text:
                # Find JSON object in the text
                start = generated_text.find("{")
                end = generated_text.rfind("}") + 1
                json_str = generated_text[start:end]
            else:
                json_str = generated_text

            post_data = json.loads(json_str)

            # Ensure required fields and convert lists to strings
            tags = post_data.get("tags", "")
            hashtags = post_data.get("hashtags", "")

            # Convert lists to comma-separated strings if needed
            if isinstance(tags, list):
                tags = ",".join(tags)
            if isinstance(hashtags, list):
                hashtags = " ".join(hashtags)

            post = {
                "title": post_data.get("title", "LinkedIn Post"),
                "content": post_data.get("content", ""),
                "post_type": post_data.get("post_type", "standard"),
                "tags": str(tags),
                "hashtags": str(hashtags),
            }

            return post

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON from LLM response: {e}")
            # Fallback: treat entire response as content
            return {
                "title": "Generated Post",
                "content": generated_text[:400],
                "post_type": "standard",
                "tags": "tech,career,learning",
                "hashtags": "#SoftwareEngineering #Tech #Career",
            }
        except Exception as e:
            logger.error(f"Error parsing generated content: {e}")
            return {}

    def analyze_and_recommend(
        self, analytics_data: List[Dict[str, Any]]
    ) -> str:
        """Use LLM to analyze engagement patterns and recommend content strategy"""
        if not analytics_data:
            return "No engagement data available yet. Start posting and logging metrics to get recommendations."

        try:
            # Summarize analytics
            analytics_summary = self._summarize_analytics(analytics_data)

            prompt = f"""You are a LinkedIn growth strategist.
Analyze the following post engagement data and provide recommendations for improving content strategy:

{analytics_summary}

Provide specific, actionable recommendations for:
1. Best performing content types and topics
2. Optimal posting time/frequency
3. Content format recommendations (threads, single posts, carousels)
4. Suggested hashtags and keywords
5. Engagement strategies to increase views and interactions

Be concise and specific to the data provided."""

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 800,
                },
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            if result.get("choices") and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "Unable to generate recommendations at this time."

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return f"Error generating recommendations: {str(e)}"

    def _summarize_analytics(self, analytics_data: List[Dict[str, Any]]) -> str:
        """Summarize analytics data for the LLM"""
        summary = "Post Engagement Summary:\n"

        if not analytics_data:
            return summary + "No data available"

        # Group by content type
        by_type = {}
        for item in analytics_data:
            content_type = item.get("content_type", "unknown")
            if content_type not in by_type:
                by_type[content_type] = []
            by_type[content_type].append(item)

        for content_type, items in by_type.items():
            avg_views = sum(item.get("views", 0) for item in items) / len(items)
            avg_likes = sum(item.get("likes", 0) for item in items) / len(items)
            avg_comments = sum(item.get("comments", 0) for item in items) / len(items)

            summary += f"\n{content_type}:\n"
            summary += f"  Posts: {len(items)}\n"
            summary += f"  Avg Views: {avg_views:.0f}\n"
            summary += f"  Avg Likes: {avg_likes:.0f}\n"
            summary += f"  Avg Comments: {avg_comments:.0f}\n"

        return summary

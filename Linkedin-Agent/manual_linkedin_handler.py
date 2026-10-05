import os
from datetime import datetime
import logging
from typing import List, Dict, Any
import config
from database import DatabaseManager

logger = logging.getLogger(__name__)


class ManualLinkedInHandler:
    """Prepares content for manual LinkedIn posting"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Ensure output directory exists"""
        if not os.path.exists(config.POSTS_OUTPUT_DIR):
            os.makedirs(config.POSTS_OUTPUT_DIR)

    def prepare_posts_for_posting(self, posts: List[Dict[str, str]]) -> List[str]:
        """Prepare posts and return file paths for user to access"""
        file_paths = []

        try:
            # Create a daily briefing file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            briefing_file = os.path.join(
                config.POSTS_OUTPUT_DIR, f"linkedin_posts_{datetime.now().strftime('%Y-%m-%d')}.txt"
            )

            with open(briefing_file, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write(f"LinkedIn Posts - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                for idx, post in enumerate(posts, 1):
                    f.write(f"\n{'=' * 80}\n")
                    f.write(f"POST #{idx}\n")
                    f.write(f"{'=' * 80}\n")
                    f.write(f"Type: {post.get('post_type', 'Standard')}\n")
                    f.write(f"Title: {post.get('title', 'Untitled')}\n")
                    f.write(f"\n{post.get('content', '')}\n")
                    f.write(f"\nHashtags:\n{post.get('hashtags', '')}\n")
                    f.write(f"\n{'=' * 80}\n")
                    f.write("INSTRUCTIONS FOR POSTING:\n")
                    f.write("1. Copy the content above (excluding title and hashtags if posting as single item)\n")
                    f.write("2. Open LinkedIn.com and click 'Start a post'\n")
                    f.write("3. Paste the content\n")
                    f.write("4. Paste hashtags at the end\n")
                    f.write("5. Click 'Post' or 'Schedule post' for later\n")
                    f.write(f"{'=' * 80}\n\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("SUMMARY\n")
                f.write("=" * 80 + "\n")
                f.write(f"Total Posts Generated: {len(posts)}\n")
                f.write(f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(
                    f"\nNext Steps:\n"
                    f"1. Review posts above\n"
                    f"2. Choose your preferred variation\n"
                    f"3. Post to LinkedIn manually or use LinkedIn's schedule feature\n"
                    f"4. Log the post URL and engagement metrics using the analytics command\n"
                )

            file_paths.append(briefing_file)
            logger.info(f"Generated briefing file: {briefing_file}")

            # Also generate HTML version for better viewing
            html_file = briefing_file.replace(".txt", ".html")
            self._generate_html_posts(posts, html_file)
            file_paths.append(html_file)

            return file_paths

        except Exception as e:
            logger.error(f"Error preparing posts for posting: {e}")
            return []

    def _generate_html_posts(self, posts: List[Dict[str, str]], output_file: str):
        """Generate an HTML version of posts for better viewing"""
        try:
            html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn Posts</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }
        .header {
            background: #0a66c2;
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
        }
        .post-card {
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            border-left: 4px solid #0a66c2;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .post-card h2 {
            margin-top: 0;
            color: #0a66c2;
            font-size: 18px;
        }
        .post-meta {
            background: #f0f0f0;
            padding: 10px;
            border-radius: 4px;
            margin: 15px 0;
            font-size: 13px;
            color: #666;
        }
        .post-content {
            line-height: 1.6;
            margin: 15px 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .hashtags {
            color: #0a66c2;
            font-weight: 500;
            margin: 15px 0;
            padding: 10px;
            background: #f0f8ff;
            border-radius: 4px;
        }
        .copy-button {
            background: #0a66c2;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        .copy-button:hover {
            background: #084696;
        }
        .instructions {
            background: #fff3cd;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
            border-left: 4px solid #ffc107;
        }
        .footer {
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 LinkedIn Posts Generated</h1>
        <p>""" + datetime.now().strftime('%B %d, %Y at %H:%M') + """</p>
    </div>

    <div class="instructions">
        <h3>📋 How to Use</h3>
        <ol>
            <li>Review all post variations below</li>
            <li>Click "Copy to Clipboard" on your preferred post</li>
            <li>Open LinkedIn.com and click "Start a post"</li>
            <li>Paste the content and add hashtags</li>
            <li>Schedule or publish immediately</li>
        </ol>
    </div>
"""

            for idx, post in enumerate(posts, 1):
                html_content += f"""
    <div class="post-card">
        <h2>Post #{idx}</h2>
        <div class="post-meta">
            <strong>Type:</strong> {post.get('post_type', 'Standard')} | 
            <strong>Word Count:</strong> {len(post.get('content', '').split())}
        </div>
        <div class="post-content">{post.get('content', '')}</div>
        <div class="hashtags">
            <strong>Hashtags:</strong> {post.get('hashtags', '')}
        </div>
        <button class="copy-button" onclick="copyToClipboard('post{idx}')">
            📋 Copy Post & Hashtags
        </button>
        <textarea id="post{idx}" style="display:none;">{post.get('content', '')}

{post.get('hashtags', '')}</textarea>
    </div>
"""

            html_content += """
    <div class="footer">
        <p>✅ Generated by LinkedIn Agent</p>
        <p>🔄 Next posts will be generated tomorrow at """ + config.SCHEDULE_TIME + """</p>
    </div>

    <script>
        function copyToClipboard(elementId) {
            const textarea = document.getElementById(elementId);
            textarea.select();
            document.execCommand('copy');
            alert('Post copied to clipboard!');
        }
    </script>
</body>
</html>
"""

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            logger.info(f"Generated HTML file: {output_file}")

        except Exception as e:
            logger.error(f"Error generating HTML posts: {e}")

    def log_posted_content(
        self, post_id: int, post_url: str, post_data: Dict[str, Any]
    ) -> bool:
        """Log that a post has been posted to LinkedIn"""
        try:
            self.db.mark_post_as_posted(post_id, post_url)
            logger.info(f"Logged post {post_id} as posted: {post_url}")
            return True
        except Exception as e:
            logger.error(f"Error logging posted content: {e}")
            return False

    def log_engagement_metrics(
        self,
        post_url: str,
        views: int,
        likes: int,
        comments: int,
        shares: int,
        post_data: Dict[str, Any],
    ) -> bool:
        """Log engagement metrics for a posted content"""
        try:
            self.db.insert_post_engagement(
                post_id=None,
                post_url=post_url,
                post_content=post_data.get("content", ""),
                topic=post_data.get("tags", ""),
                content_type=post_data.get("post_type", ""),
                views=views,
                likes=likes,
                comments=comments,
                shares=shares,
            )
            logger.info(f"Logged engagement metrics for {post_url}")
            return True
        except Exception as e:
            logger.error(f"Error logging engagement metrics: {e}")
            return False

    def display_today_posts(self):
        """Display today's generated posts"""
        posts = self.db.get_today_posts()

        if not posts:
            print("No posts generated today yet.")
            return

        print("\n" + "=" * 80)
        print(f"Today's Generated Posts ({datetime.now().strftime('%Y-%m-%d')})")
        print("=" * 80 + "\n")

        for idx, post in enumerate(posts, 1):
            print(f"\nPost #{idx}")
            print("-" * 80)
            print(f"Type: {post.get('post_type', 'Standard')}")
            print(f"Generated: {post.get('generated_at', '')}")
            print(f"Status: {'Posted' if post.get('posted') else 'Not Posted'}")
            if post.get('posted_url'):
                print(f"Posted URL: {post.get('posted_url')}")
            print(f"\nContent:\n{post.get('content', '')}")
            print(f"\nHashtags: {post.get('hashtags', '')}")
            print("-" * 80)

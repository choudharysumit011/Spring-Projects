import logging
from typing import List, Dict, Any
from datetime import datetime
from database import DatabaseManager
from content_generator import ContentGenerator

logger = logging.getLogger(__name__)


class AnalyticsTracker:
    """Tracks and analyzes post engagement metrics"""

    def __init__(self, content_generator: ContentGenerator, db_manager: DatabaseManager):
        self.db = db_manager
        self.generator = content_generator

    def log_post_engagement(
        self,
        post_url: str,
        views: int,
        likes: int,
        comments: int,
        shares: int,
        post_content: str = "",
        topic: str = "",
        content_type: str = "",
    ) -> bool:
        """Log engagement metrics for a post"""
        try:
            success = self.db.insert_post_engagement(
                post_id=None,
                post_url=post_url,
                post_content=post_content,
                topic=topic,
                content_type=content_type,
                views=views,
                likes=likes,
                comments=comments,
                shares=shares,
            )
            if success:
                logger.info(f"Logged engagement for {post_url}: {views} views, {likes} likes")
            return success
        except Exception as e:
            logger.error(f"Error logging post engagement: {e}")
            return False

    def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics summary for the last N days"""
        try:
            analytics_data = self.db.get_engagement_analytics(days)

            if not analytics_data:
                return {
                    "total_posts": 0,
                    "avg_views": 0,
                    "avg_likes": 0,
                    "avg_comments": 0,
                    "avg_shares": 0,
                    "by_content_type": {},
                    "by_topic": {},
                }

            # Calculate overall stats
            total_posts = len(analytics_data)
            total_views = sum(item.get("views", 0) for item in analytics_data)
            total_likes = sum(item.get("likes", 0) for item in analytics_data)
            total_comments = sum(item.get("comments", 0) for item in analytics_data)
            total_shares = sum(item.get("shares", 0) for item in analytics_data)

            # Group by content type
            by_type = {}
            for item in analytics_data:
                content_type = item.get("content_type", "unknown")
                if content_type not in by_type:
                    by_type[content_type] = {
                        "count": 0,
                        "views": 0,
                        "likes": 0,
                        "comments": 0,
                        "shares": 0,
                    }
                by_type[content_type]["count"] += 1
                by_type[content_type]["views"] += item.get("views", 0)
                by_type[content_type]["likes"] += item.get("likes", 0)
                by_type[content_type]["comments"] += item.get("comments", 0)
                by_type[content_type]["shares"] += item.get("shares", 0)

            # Calculate averages for each type
            for content_type in by_type:
                count = by_type[content_type]["count"]
                by_type[content_type]["avg_views"] = by_type[content_type]["views"] / count
                by_type[content_type]["avg_likes"] = by_type[content_type]["likes"] / count
                by_type[content_type]["avg_comments"] = by_type[content_type]["comments"] / count
                by_type[content_type]["avg_shares"] = by_type[content_type]["shares"] / count

            # Group by topic
            by_topic = {}
            for item in analytics_data:
                topic = item.get("topic", "general")
                if topic not in by_topic:
                    by_topic[topic] = {
                        "count": 0,
                        "views": 0,
                        "likes": 0,
                        "comments": 0,
                        "shares": 0,
                    }
                by_topic[topic]["count"] += 1
                by_topic[topic]["views"] += item.get("views", 0)
                by_topic[topic]["likes"] += item.get("likes", 0)
                by_topic[topic]["comments"] += item.get("comments", 0)
                by_topic[topic]["shares"] += item.get("shares", 0)

            # Calculate averages for each topic
            for topic in by_topic:
                count = by_topic[topic]["count"]
                by_topic[topic]["avg_views"] = by_topic[topic]["views"] / count
                by_topic[topic]["avg_likes"] = by_topic[topic]["likes"] / count
                by_topic[topic]["avg_comments"] = by_topic[topic]["comments"] / count
                by_topic[topic]["avg_shares"] = by_topic[topic]["shares"] / count

            return {
                "total_posts": total_posts,
                "avg_views": total_views / total_posts if total_posts > 0 else 0,
                "avg_likes": total_likes / total_posts if total_posts > 0 else 0,
                "avg_comments": total_comments / total_posts if total_posts > 0 else 0,
                "avg_shares": total_shares / total_posts if total_posts > 0 else 0,
                "by_content_type": by_type,
                "by_topic": by_topic,
            }

        except Exception as e:
            logger.error(f"Error getting analytics summary: {e}")
            return {}

    def display_analytics_report(self, days: int = 30):
        """Display a formatted analytics report"""
        summary = self.get_analytics_summary(days)

        print("\n" + "=" * 80)
        print(f"LinkedIn Post Analytics Report (Last {days} Days)")
        print("=" * 80 + "\n")

        if summary.get("total_posts", 0) == 0:
            print("❌ No engagement data available yet.")
            print("💡 Tip: Post content and log metrics to see analytics.")
            return

        print(f"📊 Overall Statistics:")
        print(f"   Total Posts: {summary.get('total_posts', 0)}")
        print(f"   Avg Views: {summary.get('avg_views', 0):.0f}")
        print(f"   Avg Likes: {summary.get('avg_likes', 0):.0f}")
        print(f"   Avg Comments: {summary.get('avg_comments', 0):.1f}")
        print(f"   Avg Shares: {summary.get('avg_shares', 0):.1f}")

        if summary.get("by_content_type"):
            print(f"\n📝 Performance by Content Type:")
            for content_type, stats in summary.get("by_content_type", {}).items():
                print(f"\n   {content_type}:")
                print(f"      Posts: {stats['count']}")
                print(f"      Avg Views: {stats['avg_views']:.0f}")
                print(f"      Avg Likes: {stats['avg_likes']:.0f}")
                print(f"      Avg Comments: {stats['avg_comments']:.1f}")
                print(f"      Avg Engagement Rate: {(stats['avg_likes'] + stats['avg_comments']) / max(stats['avg_views'], 1) * 100:.2f}%")

        if summary.get("by_topic"):
            print(f"\n🏷️  Performance by Topic:")
            for topic, stats in summary.get("by_topic", {}).items():
                print(f"\n   {topic}:")
                print(f"      Posts: {stats['count']}")
                print(f"      Avg Views: {stats['avg_views']:.0f}")
                print(f"      Avg Likes: {stats['avg_likes']:.0f}")

        print("\n" + "=" * 80)

    def get_recommendations(self, days: int = 30) -> str:
        """Get AI-powered recommendations based on analytics"""
        try:
            analytics_data = self.db.get_engagement_analytics(days)
            recommendations = self.generator.analyze_and_recommend(analytics_data)
            return recommendations
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return "Unable to generate recommendations at this time."

    def display_recommendations(self, days: int = 30):
        """Display AI-powered recommendations"""
        print("\n" + "=" * 80)
        print(f"📈 Content Strategy Recommendations (Based on {days} Days of Data)")
        print("=" * 80 + "\n")

        recommendations = self.get_recommendations(days)
        print(recommendations)
        print("\n" + "=" * 80)

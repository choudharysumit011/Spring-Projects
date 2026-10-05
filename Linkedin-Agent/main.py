#!/usr/bin/env python3
import argparse
import logging
import sys
import os
from datetime import datetime
import config
from database import DatabaseManager
from content_gatherer import ContentGatherer
from content_generator import ContentGenerator
from manual_linkedin_handler import ManualLinkedInHandler
from analytics_tracker import AnalyticsTracker
from scheduler import AgentScheduler

# Ensure logs directory exists
os.makedirs(config.LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{config.LOG_DIR}/linkedin_agent.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def initialize_agent():
    """Initialize all agent components"""
    db_manager = DatabaseManager(config.DATABASE_PATH)
    content_gatherer = ContentGatherer(db_manager)
    content_generator = ContentGenerator(db_manager)
    linkedin_handler = ManualLinkedInHandler(db_manager)
    analytics_tracker = AnalyticsTracker(content_generator, db_manager)
    agent_scheduler = AgentScheduler(
        db_manager, content_gatherer, content_generator, linkedin_handler, analytics_tracker
    )

    return {
        "db": db_manager,
        "gatherer": content_gatherer,
        "generator": content_generator,
        "handler": linkedin_handler,
        "analytics": analytics_tracker,
        "scheduler": agent_scheduler,
    }


def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Growth Agent - Automate content creation and posting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --schedule              # Start scheduler (runs daily at configured time)
  python main.py --generate              # Manually generate posts for today
  python main.py --today                 # View today's generated posts
  python main.py --log-post              # Log a posted content with metrics
  python main.py --analytics             # Display analytics and recommendations
        """,
    )

    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Start the scheduler (runs daily at configured time)",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Manually trigger content generation",
    )
    parser.add_argument(
        "--today",
        action="store_true",
        help="Display today's generated posts",
    )
    parser.add_argument(
        "--log-post",
        action="store_true",
        help="Log engagement metrics for a posted content",
    )
    parser.add_argument(
        "--analytics",
        action="store_true",
        help="Display analytics report and recommendations",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days for analytics (default: 30)",
    )
    parser.add_argument(
        "--schedule-time",
        type=str,
        help="Override default schedule time (format: HH:MM)",
    )

    args = parser.parse_args()

    # Check for required API keys
    if not config.OPENROUTER_API_KEY:
        print("❌ Error: OPENROUTER_API_KEY not set in environment variables")
        print("   Please set your OpenRouter API key to use this agent")
        return

    # Initialize agent
    print("🔧 Initializing LinkedIn Agent...")
    agent = initialize_agent()

    # Handle commands
    if args.schedule:
        print("\n🚀 Starting LinkedIn Agent Scheduler")
        print(f"   Schedule time: {config.SCHEDULE_TIME} {config.SCHEDULE_TIMEZONE}")
        print("   Press Ctrl+C to stop\n")
        agent["scheduler"].start_scheduler()

    elif args.generate:
        print("\n⚡ Manually triggering content generation...")
        agent["scheduler"].manual_trigger_daily_job()

    elif args.today:
        print("\n📝 Today's Generated Posts")
        agent["handler"].display_today_posts()

    elif args.log_post:
        print("\n📊 Log Post Engagement Metrics")
        post_url = input("Enter the LinkedIn post URL: ").strip()
        if not post_url:
            print("❌ Invalid URL")
            return

        try:
            views = int(input("Views: "))
            likes = int(input("Likes: "))
            comments = int(input("Comments: "))
            shares = int(input("Shares: "))

            post_type = input("Content type (tips/question/news/thread/other): ").strip() or "other"
            topic = input("Topic/Tags (optional): ").strip() or "general"

            success = agent["analytics"].log_post_engagement(
                post_url=post_url,
                views=views,
                likes=likes,
                comments=comments,
                shares=shares,
                post_content="",
                topic=topic,
                content_type=post_type,
            )

            if success:
                print(f"✅ Engagement metrics logged successfully!")
            else:
                print(f"❌ Failed to log engagement metrics")

        except ValueError:
            print("❌ Invalid input. Please enter numeric values for views, likes, comments, shares")

    elif args.analytics:
        days = args.days or 30
        agent["analytics"].display_analytics_report(days)
        agent["analytics"].display_recommendations(days)

    else:
        # Default: show help and status
        parser.print_help()
        print("\n" + "=" * 80)
        print("📊 LinkedIn Agent Status")
        print("=" * 80)
        print(f"✅ Agent initialized successfully")
        print(f"🗄️  Database: {config.DATABASE_PATH}")
        print(f"⏰ Schedule time: {config.SCHEDULE_TIME}")
        print(f"📁 Posts output: {config.POSTS_OUTPUT_DIR}")
        print(f"📝 Logs: {config.LOG_DIR}/linkedin_agent.log")
        print("\nRun with --help to see available commands")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Agent stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

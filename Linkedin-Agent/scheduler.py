import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import config
from database import DatabaseManager
from content_gatherer import ContentGatherer
from content_generator import ContentGenerator
from manual_linkedin_handler import ManualLinkedInHandler
from analytics_tracker import AnalyticsTracker

logger = logging.getLogger(__name__)


class AgentScheduler:
    """Manages scheduling of content generation and posting workflow"""

    def __init__(
        self,
        db_manager: DatabaseManager,
        content_gatherer: ContentGatherer,
        content_generator: ContentGenerator,
        linkedin_handler: ManualLinkedInHandler,
        analytics_tracker: AnalyticsTracker,
    ):
        self.db = db_manager
        self.gatherer = content_gatherer
        self.generator = content_generator
        self.handler = linkedin_handler
        self.analytics = analytics_tracker
        self.scheduler = BackgroundScheduler()

    def start_scheduler(self):
        """Start the background scheduler"""
        try:
            # Schedule daily content generation
            self.scheduler.add_job(
                self.daily_content_generation_job,
                "cron",
                hour=int(config.SCHEDULE_TIME.split(":")[0]),
                minute=int(config.SCHEDULE_TIME.split(":")[1]),
                timezone=config.SCHEDULE_TIMEZONE,
                id="daily_content_gen",
            )

            # Schedule weekly analytics analysis
            self.scheduler.add_job(
                self.weekly_analytics_job,
                "cron",
                day_of_week="mon",
                hour=9,
                minute=0,
                timezone=config.SCHEDULE_TIMEZONE,
                id="weekly_analytics",
            )

            self.scheduler.start()
            logger.info("Scheduler started successfully")
            print("✅ Scheduler started. Press Ctrl+C to stop.")

            # Keep the scheduler running
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                self.stop_scheduler()

        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            raise

    def stop_scheduler(self):
        """Stop the background scheduler"""
        try:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
            print("❌ Scheduler stopped.")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")

    def daily_content_generation_job(self):
        """Daily job to gather content and generate posts"""
        try:
            logger.info("Starting daily content generation job...")
            print(f"\n🚀 Starting daily content generation at {datetime.now()}")

            # Step 1: Gather content
            print("📥 Gathering content from all sources...")
            gathered_content = self.gatherer.gather_all_content()

            if not any(gathered_content.values()):
                logger.warning("No content gathered")
                print("⚠️  No content gathered from sources")
                return

            # Step 2: Generate posts
            print("✍️  Generating LinkedIn posts...")
            posts = self.generator.generate_posts(gathered_content)

            if not posts:
                logger.warning("No posts generated")
                print("⚠️  Failed to generate posts")
                return

            # Step 3: Prepare for posting
            print("💾 Preparing posts for manual posting...")
            file_paths = self.handler.prepare_posts_for_posting(posts)

            # Step 4: Display summary
            print("\n" + "=" * 80)
            print("✅ Daily Content Generation Complete!")
            print("=" * 80)
            print(f"📊 Summary:")
            print(f"   • Content items gathered: {sum(len(v) for v in gathered_content.values())}")
            print(f"   • Posts generated: {len(posts)}")
            print(f"   • Output files created: {len(file_paths)}")
            print(f"\n📂 Files saved to:")
            for file_path in file_paths:
                print(f"   • {file_path}")
            print(f"\n💡 Next steps:")
            print(f"   1. Review the posts in the files above")
            print(f"   2. Copy your preferred post")
            print(f"   3. Post to LinkedIn manually or use LinkedIn's scheduler")
            print(f"   4. Log engagement metrics using the analytics commands")
            print("=" * 80 + "\n")

            logger.info(f"Daily job completed. Generated {len(posts)} posts")

        except Exception as e:
            logger.error(f"Error in daily content generation job: {e}")
            print(f"❌ Error during daily job: {str(e)}")

    def weekly_analytics_job(self):
        """Weekly job to analyze engagement and provide recommendations"""
        try:
            logger.info("Starting weekly analytics job...")
            print(f"\n📈 Starting weekly analytics analysis at {datetime.now()}")

            # Display analytics
            self.analytics.display_analytics_report(days=7)

            # Generate recommendations
            self.analytics.display_recommendations(days=7)

            logger.info("Weekly analytics job completed")

        except Exception as e:
            logger.error(f"Error in weekly analytics job: {e}")
            print(f"❌ Error during weekly analytics: {str(e)}")

    def manual_trigger_daily_job(self):
        """Manually trigger the daily content generation job"""
        logger.info("Manually triggering daily content generation job")
        self.daily_content_generation_job()

    def manual_trigger_analytics_job(self):
        """Manually trigger the analytics job"""
        logger.info("Manually triggering analytics job")
        self.weekly_analytics_job()

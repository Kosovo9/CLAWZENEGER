from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import httpx
from ..config import settings

logger = logging.getLogger(__name__)

class NeilScheduler:
    def __init__(self, report_generator):
        self.scheduler = AsyncIOScheduler()
        self.report_generator = report_generator

    def start(self):
        # Auditoría cada 3 horas
        self.scheduler.add_job(
            self.run_audit,
            CronTrigger.from_crontab(settings.AUDIT_CRON),
            id="audit_3h",
            replace_existing=True
        )
        # Plan Diario (9 AM)
        self.scheduler.add_job(
            self.run_daily_plan,
            CronTrigger.from_crontab(settings.DAILY_PLAN_CRON),
            id="daily_plan",
            replace_existing=True
        )
        # Reporte Nocturno (9 PM)
        self.scheduler.add_job(
            self.run_nightly_report,
            CronTrigger.from_crontab(settings.NIGHTLY_REPORT_CRON),
            id="nightly_summary",
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info(f"NeilScheduler started. Audit Cron: {settings.AUDIT_CRON}")

    async def run_audit(self):
        logger.info("Executing 3-hour scheduled audit...")
        report = await self.report_generator.generate_audit_report()
        await self._notify(report)

    async def run_daily_plan(self):
        logger.info("Generating Daily Money-Making Plan...")
        report = await self.report_generator.generate_daily_plan()
        await self._notify(report)

    async def run_nightly_report(self):
        logger.info("Generating Nightly Performance Summary...")
        report = await self.report_generator.generate_nightly_report()
        await self._notify(report)

    async def _notify(self, report):
        if settings.NOTIFICATION_WEBHOOK:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(settings.NOTIFICATION_WEBHOOK, json=report)
            except Exception as e:
                logger.error(f"Error sending notification: {e}")
        
        # Log summary to console
        logger.info(f"REPORT GENERATED: {report['type']} - ID: {report['id']}")

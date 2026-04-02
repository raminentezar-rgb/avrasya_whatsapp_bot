import logging

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from core.tasks import check_and_send_birthdays, check_and_send_holidays

logger = logging.getLogger(__name__)

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """This job deletes APScheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Schedule birthday check every day at 08:00
        scheduler.add_job(
            check_and_send_birthdays,
            trigger=CronTrigger(hour="08", minute="00"),
            id="check_and_send_birthdays",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'check_and_send_birthdays'.")

        # Schedule holiday check every day at 08:30
        scheduler.add_job(
            check_and_send_holidays,
            trigger=CronTrigger(hour="08", minute="30"),
            id="check_and_send_holidays",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'check_and_send_holidays'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

from django.core.management.base import BaseCommand
from core.tasks import check_and_send_birthdays, check_and_send_holidays

class Command(BaseCommand):
    help = "Triggers the daily checks for birthdays and holidays immediately to test the logic."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting daily message triggers..."))
        
        self.stdout.write("Checking for Birthdays...")
        check_and_send_birthdays()
        
        self.stdout.write("Checking for Holidays...")
        check_and_send_holidays()
        
        self.stdout.write(self.style.SUCCESS("Daily triggers executed successfully! Please check Django Admin 'Message Logs'."))

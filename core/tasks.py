from datetime import date
from django.utils import timezone
from .models import Employee, Holiday, MessageLog
from .services import send_whatsapp_message, send_telegram_message
import logging

logger = logging.getLogger(__name__)

def check_and_send_birthdays():
    """Scheduled task to send birthday messages."""
    logger.info("Running check_and_send_birthdays task...")
    today = date.today()
    employees = Employee.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
        is_active=True
    )
    
    for emp in employees:
        message = f"Doğum günün kutlu olsun {emp.name}! Avrasya Üniversitesi olarak harika bir yıl geçirmeni dileriz."
        
        # Check if already sent today to avoid duplicates on retries
        if MessageLog.objects.filter(
            employee=emp, 
            message_type='Birthday', 
            sent_at__date=today
        ).exists():
            continue

        send_to_employee(emp, "Birthday", message)
            
def check_and_send_holidays():
    """Scheduled task to send holiday messages."""
    logger.info("Running check_and_send_holidays task...")
    today = date.today()
    
    # Check for specific dates
    holidays = Holiday.objects.filter(date=today, is_active=True)
    
    # Check for recurring dates
    recurring_holidays = Holiday.objects.filter(
        recurring_month=today.month, 
        recurring_day=today.day,
        is_active=True
    )
    
    all_holidays = list(holidays) + list(recurring_holidays)
    
    if not all_holidays:
        return
        
    employees = Employee.objects.filter(is_active=True)
    
    for holiday in all_holidays:
        for emp in employees:
            # Check for duplicates
            if MessageLog.objects.filter(
                employee=emp, 
                message_type=f'Holiday: {holiday.name}', 
                sent_at__date=today
            ).exists():
                continue
                
            message = holiday.message_template.format(name=emp.name)
            send_to_employee(emp, f"Holiday: {holiday.name}", message)

def send_to_employee(employee, message_type, message):
    if employee.phone_number:
        success, error = send_whatsapp_message(employee.phone_number, message)
        MessageLog.objects.create(
            employee=employee,
            message_type=message_type,
            platform='WhatsApp',
            status='SENT' if success else 'FAILED',
            error_message=error
        )
        
    if employee.telegram_chat_id:
        success, error = send_telegram_message(employee.telegram_chat_id, message)
        MessageLog.objects.create(
            employee=employee,
            message_type=message_type,
            platform='Telegram',
            status='SENT' if success else 'FAILED',
            error_message=error
        )

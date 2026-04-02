from django.contrib import admin
from django.contrib import messages
from .models import Employee, Holiday, MessageLog
from .services import send_whatsapp_message, send_telegram_message
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        import_id_fields = ('id',)

class HolidayResource(resources.ModelResource):
    class Meta:
        model = Holiday
        import_id_fields = ('id',)

@admin.action(description='Send Test Message (WhatsApp & Telegram)')
def send_test_message(modeladmin, request, queryset):
    for emp in queryset:
        # Twilio Sandbox requires exact template matches to initiate conversation (if no 24h window open)
        # Sandbox Default Template: Your appointment is coming up on {{1}} at {{2}}
        test_msg_wa = f"Your appointment is coming up on July 1 at 3pm"
        test_msg_tg = f"Merhaba {emp.name}, bu Avrasya Bot'tan Telegram üzerinden gönderilen bir test mesajıdır!"
        
        if emp.phone_number:
            success, err = send_whatsapp_message(emp.phone_number, test_msg_wa)
            MessageLog.objects.create(
                employee=emp, message_type='Test', platform='WhatsApp',
                status='SENT' if success else 'FAILED', error_message=err
            )
            if success:
                messages.success(request, f"WhatsApp sent to {emp.name}")
            else:
                messages.error(request, f"WhatsApp failed to {emp.name}: {err}")
                
        if emp.telegram_chat_id:
            success, err = send_telegram_message(emp.telegram_chat_id, test_msg_tg)
            MessageLog.objects.create(
                employee=emp, message_type='Test', platform='Telegram',
                status='SENT' if success else 'FAILED', error_message=err
            )
            if success:
                messages.success(request, f"Telegram sent to {emp.name}")
            else:
                messages.error(request, f"Telegram failed to {emp.name}: {err}")

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_classes = [EmployeeResource]
    list_display = ('name', 'role', 'department', 'date_of_birth', 'phone_number', 'is_active')
    list_filter = ('role', 'department', 'is_active')
    search_fields = ('name', 'phone_number', 'department')
    actions = [send_test_message]

@admin.register(Holiday)
class HolidayAdmin(ImportExportModelAdmin):
    resource_classes = [HolidayResource]
    list_display = ('name', 'date', 'recurring_month', 'recurring_day', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'message_type', 'platform', 'status', 'sent_at')
    list_filter = ('status', 'platform', 'message_type')
    search_fields = ('employee__name', 'error_message')
    readonly_fields = ('sent_at',)


from django.db import models

class Employee(models.Model):
    ROLE_CHOICES = [
        ('STAFF', 'Staff/Employee'),
        ('PROFESSOR', 'Professor'),
    ]
    name = models.CharField(max_length=200, verbose_name="Full Name")
    phone_number = models.CharField(max_length=20, verbose_name="WhatsApp Number", help_text="Virtual tests can use any number format")
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telegram Chat ID")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    department = models.CharField(max_length=150, verbose_name="Department")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF', verbose_name="Role")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

class Holiday(models.Model):
    name = models.CharField(max_length=150, verbose_name="Holiday/Occasion Name")
    date = models.DateField(verbose_name="Specific Date", null=True, blank=True, help_text="Use this for one-time holidays")
    recurring_month = models.IntegerField(null=True, blank=True, help_text="1-12 for recurring yearly holidays (e.g., 12 for Christmas)")
    recurring_day = models.IntegerField(null=True, blank=True, help_text="Day of the month for recurring holidays (e.g., 25)")
    message_template = models.TextField(verbose_name="Message Template", help_text="Use {name} to insert the employee's name.")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self):
        return self.name

class MessageLog(models.Model):
    STATUS_CHOICES = [
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='message_logs')
    message_type = models.CharField(max_length=50, help_text="e.g., Birthday, Christmas, etc.")
    platform = models.CharField(max_length=20, help_text="WhatsApp or Telegram")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        emp_name = self.employee.name if self.employee else "Unknown"
        return f"[{self.sent_at.strftime('%Y-%m-%d %H:%M')}] {self.status} to {emp_name} via {self.platform}"

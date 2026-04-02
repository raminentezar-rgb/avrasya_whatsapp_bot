import os
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee, Holiday, MessageLog

logger = logging.getLogger(__name__)

# --- WEBHOOK ---
@csrf_exempt
def twilio_webhook(request):
    if request.method == 'POST':
        # Twilio sends data as form-urlencoded POST requests
        sender = request.POST.get('From', '')
        message_body = request.POST.get('Body', '')
        
        logger.info(f"Twilio Webhook Received - From: {sender}, Body: {message_body}")
        
        # Twilio expects a TwiML XML response. 
        # An empty response is valid if we don't want to reply immediately via TwiML.
        return HttpResponse("<Response></Response>", content_type="text/xml")

    return HttpResponse('Method Not Allowed', status=405)


# --- DASHBOARD VIEWS ---
def dashboard_home(request):
    total_employees = Employee.objects.count()
    total_messages = MessageLog.objects.count()
    successful = MessageLog.objects.filter(status='SENT').count()
    success_rate = int((successful / total_messages * 100)) if total_messages > 0 else 0
    
    whatsapp_logs = MessageLog.objects.filter(platform__icontains='WhatsApp').count()
    telegram_logs = MessageLog.objects.filter(platform__icontains='Telegram').count()
    
    recent_logs = MessageLog.objects.order_by('-sent_at')[:7]
    
    # Construct last 7 days chart
    chart_labels = []
    chart_data = []
    today = timezone.now().date()
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        # Using simple string representation
        chart_labels.append(day.strftime("%a"))
        count = MessageLog.objects.filter(sent_at__date=day).count()
        chart_data.append(count)

    context = {
        'total_employees': total_employees,
        'total_messages': total_messages,
        'success_rate': success_rate,
        'recent_logs': recent_logs,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'whatsapp_logs': whatsapp_logs,
        'telegram_logs': telegram_logs,
    }
    return render(request, 'dashboard.html', context)

def employees_list(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file) if excel_file.name.endswith('.xlsx') else pd.read_csv(excel_file)
            
            count = 0
            for index, row in df.iterrows():
                tel = str(row.get('telegram_chat_id', ''))
                if tel == 'nan': tel = ''
                
                Employee.objects.create(
                    name=row.get('name'),
                    phone_number=str(row.get('phone_number', '')),
                    telegram_chat_id=tel,
                    date_of_birth=row.get('date_of_birth'),
                    department=row.get('department', ''),
                    role=row.get('role', 'STAFF'),
                    is_active=bool(row.get('is_active', True))
                )
                count += 1
            messages.success(request, f"{count} personel başarıyla içe aktarıldı!")
        except Exception as e:
            messages.error(request, f"Dosya okuma hatası: {e}")
            
        return redirect('employees_list')

    employees = Employee.objects.all().order_by('-id')
    return render(request, 'employees.html', {'employees': employees})

def holidays_list(request):
    holidays = Holiday.objects.all().order_by('-id')
    return render(request, 'holidays.html', {'holidays': holidays})

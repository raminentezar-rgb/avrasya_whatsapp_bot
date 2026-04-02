from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('employees/', views.employees_list, name='employees_list'),
    path('holidays/', views.holidays_list, name='holidays_list'),
    path('guide/', views.guide_page, name='guide_page'),
    path('webhook/twilio/', views.twilio_webhook, name='twilio_webhook'),

]

import pandas as pd
import datetime

# --- EMPLOYEES ---
# Fields: id, name, phone_number, telegram_chat_id, date_of_birth, department, role, is_active

employees_data = [
    {
        "id": "", # empty to let auto-increment
        "name": "Jane Doe",
        "phone_number": "+1234567890",
        "telegram_chat_id": "987654321",
        "date_of_birth": "1990-05-15",
        "department": "Engineering",
        "role": "STAFF",
        "is_active": True
    },
    {
        "id": "",
        "name": "Prof. Alan Smith",
        "phone_number": "+1987654321",
        "telegram_chat_id": "",
        "date_of_birth": "1975-10-20",
        "department": "Computer Science",
        "role": "PROFESSOR",
        "is_active": True
    }
]

df_employees = pd.DataFrame(employees_data)
df_employees.to_excel("employees_test_data.xlsx", index=False)
print("Generated employees_test_data.xlsx successfully.")

# --- HOLIDAYS ---
# Fields: id, name, date, recurring_month, recurring_day, message_template, is_active

holidays_data = [
    {
        "id": "",
        "name": "New Year Test",
        "date": "2026-01-01",
        "recurring_month": 1,
        "recurring_day": 1,
        "message_template": "Happy New Year {name}!",
        "is_active": True
    },
    {
        "id": "",
        "name": "One-time Special Holiday",
        "date": "2026-04-10",
        "recurring_month": "",
        "recurring_day": "",
        "message_template": "Enjoy the special holiday {name}!",
        "is_active": True
    }
]

df_holidays = pd.DataFrame(holidays_data)
df_holidays.to_excel("holidays_test_data.xlsx", index=False)
print("Generated holidays_test_data.xlsx successfully.")

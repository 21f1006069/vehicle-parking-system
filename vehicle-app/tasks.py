import csv
import os
import requests
from dotenv import load_dotenv
from celery_app import celery
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from models.tasks_models import (
    get_all_users,
    get_user_last_visit,
    get_newly_created_lots,
    get_all_users_email,
    get_user_monthly_data,
    get_most_used_lot,
    get_user_parking_history
)

load_dotenv()

GC_WEBHOOK = os.getenv("GC_WEBHOOK_URL")

def send_gchat_message(text):
    if not GC_WEBHOOK:
        print("Webhook not configured")
        return False
    res = requests.post(GC_WEBHOOK, json={"text": text}, timeout=10)
    return res.ok


@celery.task(name="tasks.send_daily_reminders")
def send_daily_reminders():
    print("Daily Reminder Triggered")

    users = get_all_users()
    newly_added_lots = get_newly_created_lots()

    for user in users:
        user_id = user["user_id"]
        last_visit = get_user_last_visit(user_id)

        needs_reminder = False

        # No visit ever or last visit was previous day
        if not last_visit:
            needs_reminder = True
        else:
            from datetime import datetime
            if last_visit.date() != datetime.now().date():
                needs_reminder = True

        # New lots created today
        if newly_added_lots:
            needs_reminder = True

        if needs_reminder:
            message = f"""
Hello {user['name']},
Just a reminder to check your parking dashboard.
New parking spots may be available.
            """
            send_gchat_message(message)

    return {"status": "Daily reminder job complete"}


#2 For Sending monthly mail

def send_email(to, subject, html):
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", 587))
    user = os.getenv("SMTP_USER")
    pwd = os.getenv("SMTP_PASS")

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))

    s = smtplib.SMTP(host, port)
    s.starttls()
    s.login(user, pwd)
    s.sendmail(user, to, msg.as_string())
    s.quit()

@celery.task(name="tasks.monthly_report_user")
def monthly_report_user(user_id, email, name, year=None, month=None):
    # default → previous month
    now = datetime.now()
    if not year or not month:
        if now.month == 1:
            year = now.year - 1
            month = 12
        else:
            year = now.year
            month = now.month - 1

    rows = get_user_monthly_data(user_id, year, month)
    lot_id, lot_count = get_most_used_lot(user_id, year, month)

    print("Parking History:", rows)
    print("Most Used Lot:", lot_id + lot_count)

    total = sum([r[6] or 0 for r in rows])

    # very simple HTML
    html = f"""
    <h2>Monthly Parking Report ({month}/{year})</h2>

    <p>Hello {name},</p>
    <p>Total bookings: {len(rows)}</p>
    <p>Total spent: ₹{total}</p>
    <p>Most used lot: {lot_id or '-'} ({lot_count} times)</p>

    <h3>Details</h3>
    <table border="1" cellpadding="5">
        <tr>
            <th>Reserve ID</th><th>Lot</th><th>Spot</th>
            <th>Vehicle</th><th>In</th><th>Out</th><th>Cost</th>
        </tr>
    """

    for r in rows:
        html += f"""
        <tr>
            <td>{r[0]}</td>
            <td>{r[1]}</td>
            <td>{r[2]}</td>
            <td>{r[3]}</td>
            <td>{r[4]}</td>
            <td>{r[5] or '-'}</td>
            <td>{r[6] or 0}</td>
        </tr>
        """

    html += "</table>"

    send_email(email, f"Monthly Parking Report {month}/{year}", html)

    return f"Report mailed to {email}"


@celery.task(name="tasks.monthly_report_all")
def monthly_report_all():
    users = get_all_users_email()  # (user_id, email, name)

    for u in users:
        uid, email, name = u
        monthly_report_user.delay(uid, email, name)

    return "Triggered monthly reports for all"


EXPORT_DIR = "/home/ganeshpuppala/vehicle-app/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

@celery.task(name="tasks.export_user_csv")
def export_user_csv(user_id, user_name):
    print("Inside Celery Call")
    data = get_user_parking_history(user_id)

    print(data)

    filename = f"user_export_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    path = os.path.join(EXPORT_DIR, filename)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Spot ID", "Lot ID", "Vehicle Number",
            "Check In", "Check Out", "Cost", "Remarks"
        ])
        writer.writerows(data)

    send_gchat_message(f"Hi {user_name}, your CSV export is ready: {filename}")
    return {"file": filename}
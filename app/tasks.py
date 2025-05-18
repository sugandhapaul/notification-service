from .celery_worker import celery_app

@celery_app.task
def send_notification(notification_id: int):
    print(f"Sending notification with ID {notification_id}")
    # Placeholder — this will eventually trigger email, sms, or websocket

from celery import shared_task

@shared_task
def send_email_task(user_id: int, message: str):
    print(f"Sending email to user {user_id}: {message}")

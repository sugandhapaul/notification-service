from app.tasks import send_email_task

send_email_task.delay(123, "Hello from manual test script!")

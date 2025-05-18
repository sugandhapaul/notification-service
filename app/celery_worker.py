from celery import Celery

celery_app = Celery(
    "worker",
    broker="amqp://guest:guest@localhost:5672//",  # RabbitMQ broker
    backend="rpc://"  # or use Redis if available
)

celery_app.autodiscover_tasks(['app'])

# This is key: make sure the tasks module is imported here
import app.tasks

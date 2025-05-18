class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///notifications.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'pyamqp://guest@localhost//'
    CELERY_RESULT_BACKEND = 'rpc://'

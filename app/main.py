from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal, engine, Base

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST /notifications
@app.post("/notifications", response_model=schemas.NotificationResponse)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    db_notification = models.Notification(
        user_id=notification.user_id,
        type=notification.type,
        message=notification.message,
        sent=False  # We'll update this when sending later
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

# GET /users/{user_id}/notifications
@app.get("/users/{user_id}/notifications", response_model=list[schemas.NotificationResponse])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    notifications = db.query(models.Notification).filter(models.Notification.user_id == user_id).all()
    return notifications

from app.tasks import send_notification

@app.post("/notifications", response_model=schemas.NotificationResponse)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    # Trigger async task
    send_notification.delay(db_notification.id)

    return db_notification

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    type = Column(String, index=True)  # "email", "sms", "in-app"
    message = Column(String)
    sent = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

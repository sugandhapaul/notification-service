from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    type: str  # "email", "sms", "in-app"
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    message: str
    sent: bool
    timestamp: datetime

    class Config:
        from_attributes = True

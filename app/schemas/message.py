from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.message import MessageType


class MessageBase(BaseModel):
    receiver_id: int
    content: Optional[str] = None
    message_type: MessageType = MessageType.TEXT


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    sender_id: int
    file_url: Optional[str] = None
    image_url: Optional[str] = None  # Full URL for accessing image
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    message: str
    receiver_id: int
    message_type: str = "text"
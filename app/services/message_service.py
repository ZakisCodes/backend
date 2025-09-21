from sqlalchemy.orm import Session
from app.models.message import Message, MessageType
from app.schemas.message import MessageCreate
from typing import List, Optional
import os
import aiofiles
from fastapi import UploadFile


class MessageService:
    @staticmethod
    def create_message(db: Session, message: MessageCreate, sender_id: int) -> Message:
        db_message = Message(
            sender_id=sender_id,
            receiver_id=message.receiver_id,
            content=message.content,
            message_type=message.message_type
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    
    @staticmethod
    def get_messages_between_users(db: Session, user1_id: int, user2_id: int) -> List[Message]:
        return db.query(Message).filter(
            ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
            ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
        ).order_by(Message.created_at).all()
    
    @staticmethod
    def get_user_messages(db: Session, user_id: int) -> List[Message]:
        return db.query(Message).filter(
            (Message.sender_id == user_id) | (Message.receiver_id == user_id)
        ).order_by(Message.created_at.desc()).all()
    
    @staticmethod
    async def save_uploaded_file(file: UploadFile, upload_dir: str) -> str:
        """Save uploaded file and return file path"""
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return file_path
    
    @staticmethod
    def create_media_message(
        db: Session, 
        sender_id: int, 
        receiver_id: int, 
        file_path: str, 
        message_type: MessageType,
        content: Optional[str] = None
    ) -> Message:
        db_message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            message_type=message_type,
            file_url=file_path
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
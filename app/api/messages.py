from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.message import MessageType, Message
from app.core.config import settings
import os

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/send", response_model=MessageResponse)
def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify receiver exists
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    
    return MessageService.create_message(db, message, current_user.id)


@router.post("/send-image", response_model=MessageResponse)
async def send_image_message(
    receiver_id: int = Form(...),
    caption: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify receiver exists
    receiver = db.query(User).filter(User.id == receiver_id).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    await file.seek(0)  # Reset file pointer
    
    if file_size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {settings.max_file_size} bytes"
        )
    
    # Save file
    file_path = await MessageService.save_uploaded_file(file, settings.upload_dir)
    
    # Create message
    return MessageService.create_media_message(
        db, current_user.id, receiver_id, file_path, MessageType.IMAGE, caption
    )


@router.get("/conversation/{user_id}", response_model=List[MessageResponse])
def get_conversation(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify other user exists
    other_user = db.query(User).filter(User.id == user_id).first()
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    messages = MessageService.get_messages_between_users(db, current_user.id, user_id)
    
    # Add full image URLs for image messages
    for message in messages:
        if message.message_type == MessageType.IMAGE and message.file_url:
            message.image_url = f"http://localhost:8000/messages/image/{message.id}"
    
    return messages


@router.get("/my-messages", response_model=List[MessageResponse])
def get_my_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return MessageService.get_user_messages(db, current_user.id)


@router.get("/image/{message_id}")
async def get_message_image(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get image file for a specific message"""
    from fastapi.responses import FileResponse
    
    # Get the message
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check if user has access to this message
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Check if message has an image
    if message.message_type != MessageType.IMAGE or not message.file_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message does not contain an image"
        )
    
    # Check if file exists
    if not os.path.exists(message.file_url):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image file not found"
        )
    
    return FileResponse(message.file_url)
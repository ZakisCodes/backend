from fastapi import WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.services.auth_service import AuthService
from app.services.message_service import MessageService
from app.schemas.message import MessageCreate
from app.models.message import MessageType
from .connection_manager import manager
import json


async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    # Verify token and get user
    user_id = verify_token(token)
    if not user_id:
        await websocket.close(code=4001, reason="Invalid token")
        return
    
    user = AuthService.get_user_by_id(db, int(user_id))
    if not user:
        await websocket.close(code=4001, reason="User not found")
        return
    
    await manager.connect(websocket, user.id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Validate message structure
            if "receiver_id" not in message_data or "message" not in message_data:
                await websocket.send_text(json.dumps({
                    "error": "Invalid message format. Required: receiver_id, message"
                }))
                continue
            
            receiver_id = message_data["receiver_id"]
            message_content = message_data["message"]
            message_type = message_data.get("message_type", "text")
            
            # Verify receiver exists
            receiver = AuthService.get_user_by_id(db, receiver_id)
            if not receiver:
                await websocket.send_text(json.dumps({
                    "error": "Receiver not found"
                }))
                continue
            
            # Save message to database
            message_create = MessageCreate(
                receiver_id=receiver_id,
                content=message_content,
                message_type=MessageType.TEXT if message_type == "text" else MessageType.TEXT
            )
            
            saved_message = MessageService.create_message(db, message_create, user.id)
            
            # Prepare message for real-time delivery
            real_time_message = {
                "id": saved_message.id,
                "sender_id": user.id,
                "sender_username": user.username,
                "receiver_id": receiver_id,
                "message": message_content,
                "message_type": message_type,
                "timestamp": saved_message.created_at.isoformat()
            }
            
            # Send to receiver (if online)
            await manager.send_personal_message(real_time_message, receiver_id)
            
            # Send confirmation back to sender
            await websocket.send_text(json.dumps({
                "status": "sent",
                "message_id": saved_message.id,
                "timestamp": saved_message.created_at.isoformat()
            }))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user.id)
from typing import Dict, List
from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self):
        # Store active connections: {user_id: [websocket_connections]}
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"User {user_id} disconnected")
    
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            # Send to all connections of this user (multiple tabs/devices)
            disconnected_connections = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    # Connection is broken, mark for removal
                    disconnected_connections.append(connection)
            
            # Remove broken connections
            for conn in disconnected_connections:
                self.active_connections[user_id].remove(conn)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def broadcast_to_users(self, message: dict, user_ids: List[int]):
        for user_id in user_ids:
            await self.send_personal_message(message, user_id)
    
    def get_connected_users(self) -> List[int]:
        return list(self.active_connections.keys())


# Global connection manager instance
manager = ConnectionManager()
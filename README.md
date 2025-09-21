# Social Media Backend API

A production-ready FastAPI backend for a social media platform with real-time chat functionality.

## Features

- **Authentication System**: User registration, login with JWT tokens
- **Real-time Chat**: WebSocket-based messaging with P2P communication
- **Media Sharing**: Support for text, images, videos, audio files
- **Scalable Architecture**: Modular design for easy feature additions
- **Database Integration**: SQLAlchemy with support for PostgreSQL/SQLite
- **Security**: JWT token validation, password hashing

## Project Structure

```
app/
├── api/                 # API endpoints
│   ├── auth.py         # Authentication routes
│   ├── messages.py     # Message handling routes
│   └── dependencies.py # Shared dependencies
├── core/               # Core functionality
│   ├── config.py       # Configuration settings
│   ├── database.py     # Database connection
│   └── security.py     # Security utilities
├── models/             # Database models
│   ├── user.py         # User model
│   └── message.py      # Message model
├── schemas/            # Pydantic schemas
│   ├── user.py         # User schemas
│   └── message.py      # Message schemas
├── services/           # Business logic
│   ├── auth_service.py # Authentication service
│   └── message_service.py # Message service
└── websocket/          # WebSocket functionality
    ├── connection_manager.py # Connection management
    └── chat.py         # Chat WebSocket handler
```

## Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment setup**:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the server**:

   ```bash
   python main.py
   ```

4. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Testing

### Automated Testing

Run the test script to verify functionality:

```bash
python test_api.py
```

### Manual Testing Steps

1. **Register Users**:

   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
   -H "Content-Type: application/json" \
   -d '{"username": "alice", "email": "alice@example.com", "password": "password123", "full_name": "Alice Johnson"}'
   ```

2. **Login**:

   ```bash
   curl -X POST "http://localhost:8000/auth/login" \
   -H "Content-Type: application/json" \
   -d '{"username": "alice", "password": "password123"}'
   ```

3. **Send Message**:

   ```bash
   curl -X POST "http://localhost:8000/messages/send" \
   -H "Authorization: Bearer YOUR_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{"receiver_id": 2, "content": "Hello!", "message_type": "TEXT"}'
   ```

4. **Send Image** (using curl):
   ```bash
   curl -X POST "http://localhost:8000/messages/send-image" \
   -H "Authorization: Bearer YOUR_TOKEN" \
   -F "receiver_id=2" \
   -F "caption=Check this out!" \
   -F "file=@path/to/image.jpg"
   ```

### WebSocket Testing

Connect to WebSocket endpoint: `ws://localhost:8000/ws/chat?token=YOUR_JWT_TOKEN`

Send message format:

```json
{
  "receiver_id": 2,
  "message": "Hello from WebSocket!",
  "message_type": "text"
}
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info
- `GET /auth/users` - List all users (demo)

### Messages

- `POST /messages/send` - Send text message
- `POST /messages/send-image` - Send image message
- `GET /messages/conversation/{user_id}` - Get conversation with user
- `GET /messages/my-messages` - Get all user messages

### WebSocket

- `WS /ws/chat` - Real-time chat connection

## Media Support

Currently implemented:

- ✅ Text messages
- ✅ Image sharing
- 🚧 Video sharing (structure ready, needs implementation)
- 🚧 Audio sharing (structure ready, needs implementation)

## Future Services

The architecture supports easy addition of:

- User feed system
- Following/followers functionality
- Post creation and management
- Notifications system
- User profiles and settings

## Production Considerations

1. **Database**: Switch to PostgreSQL in production
2. **File Storage**: Use cloud storage (S3, CloudFlare R2) for media files
3. **Security**: Configure CORS properly, use environment variables
4. **Monitoring**: Add logging, metrics, and health checks
5. **Scaling**: Consider Redis for WebSocket scaling across multiple instances

## Supabase Integration

The code includes commented Supabase integration for production use:

- JWT token verification with Supabase
- User authentication through Supabase Auth
- Uncomment and configure when ready to integrate

## Notes

- SQLite is used for development; switch to PostgreSQL for production
- File uploads are stored locally; consider cloud storage for production
- WebSocket connections support multiple tabs/devices per user
- All endpoints include proper error handling and validation

{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzU4NDcyNTQ2fQ.K_04cD9nEBL1Ha1G8HoZVOm3RuwLc9naIxn60k4uACU",
"token_type": "bearer"
}

import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_registration_and_messaging():
    """Test script to demonstrate the API functionality"""
    
    # Test 1: Register first user
    print("=== Testing User Registration ===")
    user1_data = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
        "full_name": "Alice Johnson"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user1_data)
    print(f"User 1 Registration: {response.status_code}")
    if response.status_code == 200:
        user1 = response.json()
        print(f"Created user: {user1['username']} (ID: {user1['id']})")
    else:
        print(f"Error: {response.text}")
        return
    
    # Test 2: Register second user
    user2_data = {
        "username": "bob",
        "email": "bob@example.com", 
        "password": "password456",
        "full_name": "Bob Smith"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user2_data)
    print(f"User 2 Registration: {response.status_code}")
    if response.status_code == 200:
        user2 = response.json()
        print(f"Created user: {user2['username']} (ID: {user2['id']})")
    else:
        print(f"Error: {response.text}")
        return
    
    # Test 3: Login first user
    print("\n=== Testing User Login ===")
    login_data = {"username": "alice", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        alice_token = token_data["access_token"]
        print("Alice logged in successfully")
    else:
        print(f"Login failed: {response.text}")
        return
    
    # Test 4: Login second user
    login_data = {"username": "bob", "password": "password456"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        bob_token = token_data["access_token"]
        print("Bob logged in successfully")
    else:
        print(f"Login failed: {response.text}")
        return
    
    # Test 5: Send message from Alice to Bob
    print("\n=== Testing Message Sending ===")
    headers = {"Authorization": f"Bearer {alice_token}"}
    message_data = {
        "receiver_id": user2["id"],
        "content": "Hello Bob! This is Alice.",
        "message_type": "TEXT"
    }
    
    response = requests.post(f"{BASE_URL}/messages/send", json=message_data, headers=headers)
    if response.status_code == 200:
        message = response.json()
        print(f"Message sent: ID {message['id']}")
    else:
        print(f"Message send failed: {response.text}")
    
    # Test 6: Get conversation between Alice and Bob (from Bob's perspective)
    print("\n=== Testing Message Retrieval ===")
    headers = {"Authorization": f"Bearer {bob_token}"}
    response = requests.get(f"{BASE_URL}/messages/conversation/{user1['id']}", headers=headers)
    
    if response.status_code == 200:
        messages = response.json()
        print(f"Found {len(messages)} messages in conversation:")
        for msg in messages:
            sender = "Alice" if msg["sender_id"] == user1["id"] else "Bob"
            print(f"  {sender}: {msg['content']}")
    else:
        print(f"Failed to get messages: {response.text}")
    
    # Test 7: List all users
    print("\n=== Testing User List ===")
    response = requests.get(f"{BASE_URL}/auth/users")
    if response.status_code == 200:
        users = response.json()
        print("All users:")
        for user in users:
            print(f"  - {user['username']} ({user['email']})")
    
    print("\n=== Test Complete ===")
    print("You can now test WebSocket chat by connecting to ws://localhost:8000/ws/chat?token=<your_token>")


if __name__ == "__main__":
    test_user_registration_and_messaging()
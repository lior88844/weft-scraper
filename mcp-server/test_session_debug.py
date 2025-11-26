#!/usr/bin/env python3
"""
Quick test to verify session isolation is working
Run this to simulate multiple users with different sessions
"""

import requests
import json

# Server URL (adjust if needed)
SERVER_URL = "http://localhost:8080/mcp"

def simulate_session(session_id, name):
    """Simulate a user session"""
    print(f"\n{'='*60}")
    print(f"Testing Session: {name} (ID: {session_id})")
    print('='*60)
    
    # Create request with session ID in metadata
    request_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "debug_session",
            "arguments": {},
            "_meta": {
                "sessionId": session_id
            }
        }
    }
    
    try:
        response = requests.post(SERVER_URL, json=request_payload)
        if response.status_code == 200:
            result = response.json()
            print("✓ Response received:")
            print(json.dumps(result, indent=2))
        else:
            print(f"✗ Error: Status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Connection error: {e}")
        print("\nIs the MCP server running?")
        print("Start it with: cd mcp-server && python server.py")

if __name__ == "__main__":
    print("🧪 Session Isolation Test")
    print("="*60)
    
    # Simulate two different users
    simulate_session("test-alice-12345", "Alice")
    simulate_session("test-bob-67890", "Bob")
    
    print("\n" + "="*60)
    print("✓ Test complete!")
    print("\nIf both sessions show different session IDs,")
    print("session isolation is working correctly!")
    print("="*60)


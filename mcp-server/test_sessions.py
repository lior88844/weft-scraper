#!/usr/bin/env python3
"""
Test script to verify session isolation in the MCP server
Run this after starting the server to simulate multiple chat sessions
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
SERVER_URL = "http://localhost:8080/mcp"
HEADERS = {"Content-Type": "application/json"}


def make_request(method: str, params: Dict[str, Any], session_id: str = None) -> Dict:
    """Make an MCP protocol request"""
    request_data = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": method,
        "params": params
    }
    
    # Add session ID to params metadata if provided
    if session_id:
        if "_meta" not in request_data["params"]:
            request_data["params"]["_meta"] = {}
        request_data["params"]["_meta"]["sessionId"] = session_id
    
    print(f"\n🔵 Request ({session_id or 'no-session'}):")
    print(f"   Method: {method}")
    if session_id:
        print(f"   Session: {session_id}")
    
    try:
        response = requests.post(SERVER_URL, json=request_data, headers=HEADERS)
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Response: {result.get('result', {}).get('content', [{}])[0].get('text', 'N/A')[:100]}...")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}


def test_session_isolation():
    """Test that different sessions have isolated carts"""
    
    print("\n" + "="*80)
    print("SESSION ISOLATION TEST")
    print("="*80)
    
    # Define two different sessions
    session_a = "test-session-alice"
    session_b = "test-session-bob"
    
    print("\n📋 Test Plan:")
    print("1. Session A: Search products and add items to cart")
    print("2. Session B: View cart (should be empty)")
    print("3. Session B: Add different items")
    print("4. Session A: View cart (should show original items only)")
    print("5. Both sessions: Run debug to compare session IDs")
    
    # Step 1: Session A - Search and add products
    print("\n\n--- STEP 1: Session A adds items ---")
    
    # Search for products
    make_request(
        "tools/call",
        {
            "name": "search_products",
            "arguments": {"search": ""}
        },
        session_a
    )
    
    time.sleep(0.5)
    
    # Add first product (assuming products exist)
    make_request(
        "tools/call",
        {
            "name": "add_to_cart",
            "arguments": {"product_id": "nitzat-haduvdevan:0", "quantity": 2}
        },
        session_a
    )
    
    time.sleep(0.5)
    
    # Add second product
    make_request(
        "tools/call",
        {
            "name": "add_to_cart",
            "arguments": {"product_id": "nitzat-haduvdevan:1", "quantity": 1}
        },
        session_a
    )
    
    # Step 2: Session B - View cart (should be empty)
    print("\n\n--- STEP 2: Session B views cart (should be empty) ---")
    time.sleep(0.5)
    
    result = make_request(
        "tools/call",
        {
            "name": "view_cart",
            "arguments": {}
        },
        session_b
    )
    
    # Check if cart is empty
    if result.get("result", {}).get("content", [{}])[0].get("text", "").find("ריקה") != -1:
        print("   ✅ PASS: Session B cart is empty")
    else:
        print("   ❌ FAIL: Session B cart is not empty!")
    
    # Step 3: Session B - Add different items
    print("\n\n--- STEP 3: Session B adds different items ---")
    time.sleep(0.5)
    
    make_request(
        "tools/call",
        {
            "name": "add_to_cart",
            "arguments": {"product_id": "nitzat-haduvdevan:5", "quantity": 3}
        },
        session_b
    )
    
    # Step 4: Session A - View cart (should have original items)
    print("\n\n--- STEP 4: Session A views cart (should have original 2 items) ---")
    time.sleep(0.5)
    
    result_a = make_request(
        "tools/call",
        {
            "name": "view_cart",
            "arguments": {}
        },
        session_a
    )
    
    # Step 5: Debug both sessions
    print("\n\n--- STEP 5: Debug session information ---")
    time.sleep(0.5)
    
    print("\n🔍 Session A Debug:")
    make_request(
        "tools/call",
        {
            "name": "debug_session",
            "arguments": {}
        },
        session_a
    )
    
    time.sleep(0.5)
    
    print("\n🔍 Session B Debug:")
    make_request(
        "tools/call",
        {
            "name": "debug_session",
            "arguments": {}
        },
        session_b
    )
    
    # Summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print("""
If the test passed:
✅ Session A and B should show different session IDs
✅ Session A cart should have 2 items (products 0 and 1)
✅ Session B cart should have 1 item (product 5)
✅ Carts should not overlap

If the test failed:
❌ Both sessions might be using 'default' session ID
❌ Check server logs for session ID warnings
❌ ChatGPT might not be sending session context properly
""")


def test_without_session_id():
    """Test what happens when no session ID is provided"""
    
    print("\n" + "="*80)
    print("NO SESSION ID TEST (Fallback Behavior)")
    print("="*80)
    
    print("\n📋 This test verifies the fallback behavior when ChatGPT doesn't send session IDs")
    print("Expected: All requests should use 'default' session")
    
    make_request(
        "tools/call",
        {
            "name": "debug_session",
            "arguments": {}
        },
        session_id=None  # No session ID
    )
    
    print("\n⚠️  If you see 'default' session, ChatGPT is not sending session context!")


if __name__ == "__main__":
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    MCP SERVER SESSION ISOLATION TEST                      ║
╚══════════════════════════════════════════════════════════════════════════╝

This script tests whether different chat sessions have isolated carts.

Prerequisites:
1. MCP server must be running (python server.py)
2. Server should be accessible at http://localhost:8080/mcp
3. Products should be loaded

""")
    
    try:
        # Test 1: Session isolation
        test_session_isolation()
        
        # Test 2: No session ID fallback
        test_without_session_id()
        
        print("\n✅ All tests completed!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


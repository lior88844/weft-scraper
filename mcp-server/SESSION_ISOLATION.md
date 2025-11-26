# Session Isolation Guide

## Overview

The Weft MCP Server maintains **separate shopping carts for each chat conversation**. This means:
- ✅ Each ChatGPT conversation has its own isolated cart
- ✅ Items added in one chat don't appear in another chat
- ✅ Multiple users can interact with the MCP server simultaneously without cart conflicts

## How It Works

### Session ID Extraction

The server extracts a unique session identifier from each request sent by ChatGPT:

1. **Primary Source**: `req.params._meta.sessionId` or `req.params._meta.conversationId`
2. **Secondary Source**: `req._meta.sessionId` or `req._meta.conversationId`
3. **Fallback**: If no session ID is provided, uses `"default"` (all chats share cart)

### Cart Storage

Carts are stored in memory using this structure:

```python
user_carts = {
    "session-abc123": {
        "nitzat-haduvdevan:42": {
            "product": {...},
            "store": "nitzat-haduvdevan",
            "quantity": 2
        }
    },
    "session-xyz789": {
        "nitzat-haduvdevan:15": {
            "product": {...},
            "store": "nitzat-haduvdevan",
            "quantity": 1
        }
    }
}
```

Each session has its own dictionary of cart items.

## Testing Session Isolation

### Method 1: Use the Debug Tool

In any ChatGPT conversation with your MCP server:

```
Can you run the debug_session tool?
```

This will show:
- Your current session ID
- Number of items in your cart
- Total active sessions
- Other sessions (without exposing their contents)

### Method 2: Manual Testing

1. **Start Chat A**:
   - Search for products
   - Add 2-3 items to cart
   - View cart (should show your items)
   - Note your session ID using `debug_session`

2. **Start Chat B** (new conversation):
   - View cart immediately (should be EMPTY)
   - Run `debug_session` (should show different session ID)
   - Add different items

3. **Return to Chat A**:
   - View cart (should still show original items, not items from Chat B)

## Debugging Session Issues

### Problem: All Chats Share Same Cart

**Symptoms:**
- Items added in Chat A appear in Chat B
- `debug_session` shows session ID is `"default"`
- Server logs show: `⚠️ No session ID provided by ChatGPT!`

**Causes:**
1. ChatGPT is not sending session context
2. MCP configuration issue
3. Server is extracting session ID incorrectly

**Solutions:**

#### Check Server Logs

When you make a request, look for these log lines:

```
INFO:__main__:handle_call_tool called: add_to_cart
INFO:__main__:Request params _meta: {...}
INFO:__main__:✓ Using session ID: abc123xyz
```

If you see:
```
WARNING:__main__:⚠️ No session ID provided by ChatGPT!
WARNING:__main__:⚠️ Using fallback session ID: default
```

Then ChatGPT is not sending session context.

#### Verify ChatGPT Configuration

1. Check your ChatGPT GPT Actions configuration
2. Ensure the MCP server URL is correct
3. Try reconnecting the MCP server in ChatGPT settings

#### Update Session Extraction (if needed)

If ChatGPT sends session info in a different format, update `handle_call_tool`:

```python
# Add more extraction methods
if not session_id:
    # Try other potential locations
    session_id = arguments.get('_sessionId')  # Check arguments
    session_id = req.params.get('session')     # Check params directly
```

### Problem: Sessions Persist After Server Restart

**Symptoms:**
- Cart remains after restarting the MCP server
- Old session IDs still appear in debug info

**Cause:**
Carts are stored in memory (`user_carts = {}`). This is intentional - carts should NOT persist across restarts.

**Expected Behavior:**
- Server restart = all carts cleared
- This is by design for the current implementation

**To Add Persistence:**
You would need to:
1. Use Redis, PostgreSQL, or file-based storage
2. Serialize carts on shutdown
3. Deserialize on startup

## Advanced Configuration

### Custom Session ID Generation

If you want to generate deterministic session IDs when ChatGPT doesn't provide them:

```python
if not session_id:
    import hashlib
    # Use request timestamp + client info
    session_data = f"{req.params.name}:{time.time()}"
    session_id = hashlib.md5(session_data.encode()).hexdigest()[:16]
```

⚠️ **Warning**: This won't provide true session isolation without client-provided context.

### Session Timeout/Cleanup

To automatically clean up old sessions (not implemented):

```python
import time

# Add timestamps to cart entries
user_carts = {
    "session-123": {
        "_last_accessed": 1234567890,
        "items": {...}
    }
}

# Periodic cleanup (run every hour)
def cleanup_old_sessions(max_age_hours=24):
    now = time.time()
    max_age = max_age_hours * 3600
    
    for session_id in list(user_carts.keys()):
        if now - user_carts[session_id]["_last_accessed"] > max_age:
            del user_carts[session_id]
            logger.info(f"Cleaned up old session: {session_id}")
```

## API Reference

### Debug Tool

**Tool Name**: `debug_session`

**Description**: Display session information and cart statistics

**Parameters**: None

**Returns**:
- Current session ID
- Number of items in cart
- Total active sessions
- Other session summaries (non-sensitive)

**Example Usage** (in ChatGPT):
```
Show me my session info
```

or

```
Run debug_session
```

## Best Practices

1. **Always test with multiple conversations** before deploying
2. **Monitor server logs** for session ID warnings
3. **Use `debug_session` tool** to verify isolation
4. **Don't rely on session persistence** across server restarts
5. **Consider adding authentication** for production use

## Troubleshooting Checklist

- [ ] Server logs show unique session IDs for different chats
- [ ] `debug_session` returns different IDs in different conversations
- [ ] Cart is empty when starting a new conversation
- [ ] Items from Chat A don't appear in Chat B
- [ ] No warnings about "default" session in logs

## Future Improvements

Potential enhancements for session management:

1. **Persistent Storage**: Use Redis/PostgreSQL for cart persistence
2. **Session Authentication**: Require user authentication
3. **Session Expiration**: Auto-cleanup old carts
4. **Session Migration**: Allow users to continue shopping across devices
5. **Anonymous vs Authenticated**: Different handling for logged-in users

## Need Help?

If session isolation isn't working:

1. Check server logs for session ID warnings
2. Run `debug_session` in multiple conversations
3. Verify ChatGPT is sending conversation context
4. Check the `handle_call_tool` function for session extraction logic
5. Test with fresh conversations (not threads from before the update)


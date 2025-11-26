# Session Isolation - Quick Reference Card

## 🎯 What is Session Isolation?

**Each ChatGPT conversation = its own shopping cart**

- Chat A adds items → only in Chat A's cart
- Chat B (new conversation) → starts with empty cart
- Sessions don't interfere with each other

## 🧪 Quick Test (30 seconds)

### In ChatGPT:

**Chat A:**
```
1. "Search for products"
2. "Add the first product to cart"
3. "Run debug_session"
   → Note your session ID
```

**Chat B (new conversation):**
```
1. "View my cart"
   → Should be EMPTY ✓
2. "Run debug_session"
   → Should show DIFFERENT session ID ✓
```

✅ If both tests pass = session isolation is working!

## 🔧 New Tools

### debug_session

**What it does**: Shows your session info and cart stats

**How to use in ChatGPT**:
```
"Run debug_session"
"Show my session info"
"Debug my cart"
```

**What you'll see**:
```
Current Session ID: abc123xyz
Total Active Sessions: 2
Items in Your Cart: 3
Your Cart Total: 45.80 ₪
```

## 📝 Common Commands

| Command | What it does |
|---------|--------------|
| `"View my cart"` | Show items in YOUR cart (this session) |
| `"Add [product] to cart"` | Adds to YOUR cart only |
| `"Run debug_session"` | Check session ID and stats |
| `"Clear my cart"` | Clear YOUR cart (doesn't affect other sessions) |

## 🔍 Troubleshooting

### Problem: Items from other chats appear in my cart

**Quick Fix**:
1. Run `debug_session` in both chats
2. Check if both show same session ID
3. If yes → session isolation not working

**Check**:
```bash
# In terminal (where server is running)
# Look for this warning:
⚠️  No session ID provided by ChatGPT!
```

### Problem: Session ID shows as "default"

**Means**: ChatGPT isn't sending conversation context

**Solutions**:
- Reconnect MCP server in ChatGPT
- Restart server
- Check MCP configuration

## 🚀 Testing Script

```bash
cd mcp-server
python test_sessions.py
```

Runs automated tests to verify isolation works.

## 📂 Key Files

| File | Purpose |
|------|---------|
| `server.py` | Main server with session handling |
| `SESSION_ISOLATION.md` | Complete documentation |
| `test_sessions.py` | Automated testing |
| `QUICK_REFERENCE_SESSIONS.md` | This cheat sheet |

## ⚡ Developer Quick Start

### Check session in code:

```python
# In any tool function
async def my_tool(ctx: Context):
    session_id = ctx.session_id
    logger.info(f"Session: {session_id}")
    
    # Access this session's cart
    cart = user_carts.get(session_id, {})
```

### Add logging:

```python
# See what ChatGPT is sending
logger.info(f"Request params: {req.params._meta}")
logger.info(f"Session ID: {session_id}")
```

## 🎓 Key Concepts

**Session ID** = Unique identifier for each chat conversation
- Format: `"abc123xyz..."` (alphanumeric string)
- Sent by ChatGPT with each request
- Used as key in `user_carts` dictionary

**Cart Storage**:
```python
user_carts = {
    "session-A": {"product-1": {...}, "product-2": {...}},
    "session-B": {"product-3": {...}}
}
```

**Isolation** = Each session_id has separate cart data

## 📊 Status Indicators

| Log Message | Meaning | Status |
|-------------|---------|--------|
| `✓ Using session ID: abc123` | Session ID found | ✅ Good |
| `⚠️ No session ID provided` | Using "default" | ⚠️ Problem |
| `Found session ID in params._meta` | Extracted successfully | ✅ Good |

## 🔐 Security Notes

- Sessions are in-memory (cleared on restart)
- No authentication required (local dev)
- Each session = isolated cart
- No cross-session data leakage

## 💡 Pro Tips

1. **Test in new conversations**: Always test isolation with fresh chats
2. **Use debug_session often**: Verify your session ID
3. **Check logs**: Server logs show all session activity
4. **Restart = fresh start**: Server restart clears all carts

## 📖 More Info

- Full docs: `SESSION_ISOLATION.md`
- Main README: `README.md`
- Test script: `test_sessions.py`
- Implementation: `server.py` (lines 565-605)

---

**Need help?** Run the test script or check SESSION_ISOLATION.md


# 🚀 Quick Start Guide - Weft MCP Server

Get your Weft MCP server running in 5 minutes!

## Step 1: Check Your Setup ✅

Run the test script to see what you need:

```bash
cd mcp-server
python3 test_setup.py
```

**Expected output:**
```
✓ PASS - Project Structure
✓ PASS - Store Data
❌ FAIL - Python Version (if you have 3.9)
❌ FAIL - Dependencies (if not installed yet)
```

## Step 2: Install Python 3.10+ (if needed) 🐍

### macOS (Homebrew)
```bash
brew install python@3.11

# Verify
python3.11 --version
```

### macOS (Official Installer)
1. Download from: https://www.python.org/downloads/
2. Install the `.pkg` file
3. Verify: `python3 --version`

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11
```

## Step 3: Install Dependencies 📦

```bash
# Use Python 3.11 if you just installed it
python3.11 -m pip install -r requirements.txt

# Or if python3 is already 3.10+
pip3 install -r requirements.txt
```

**What gets installed:**
- `fastmcp` - MCP server framework
- `httpx` - HTTP client
- `python-dotenv` - Environment variables

## Step 4: Start the Server 🚀

```bash
# With Python 3.11
python3.11 server.py

# Or with python3 if it's 3.10+
python3 server.py
```

**You should see:**
```
Starting Weft MCP Server on port 8547
MCP endpoint: http://0.0.0.0:8547/mcp

Available stores (1):
  - nitzat-haduvdevan: 1325 products
```

✅ **Server is running!** Keep this terminal window open.

## Step 5: Configure ChatGPT 💬

1. Open **ChatGPT** (https://chat.openai.com)
2. Click your profile → **Settings**
3. Go to **Beta Features**
4. Enable **MCP (Model Context Protocol)**
5. Add this server configuration:

```json
{
  "mcp_servers": {
    "weft": {
      "url": "http://localhost:8547/mcp",
      "name": "Weft Store",
      "description": "Browse organic products from Weft stores",
      "transport": "http"
    }
  }
}
```

6. Click **Save**
7. Reload ChatGPT

## Step 6: Test It! 🎉

Open a new ChatGPT chat and try:

### Example 1: Browse Products
```
You: Show me all products from Weft
```

ChatGPT will display a beautiful product grid with images!

### Example 2: Search
```
You: Find quinoa products
You: What grains do you have under 20 shekels?
You: Show me products in the דגנים category
```

### Example 3: Shopping Cart
```
You: Add the 500g quinoa to my cart
You: What's in my cart?
You: Remove the quinoa
```

## Troubleshooting 🔧

### "Python version 3.9"
You need Python 3.10+. See Step 2 above.

### "ModuleNotFoundError: No module named 'fastmcp'"
Install dependencies: `pip3 install -r requirements.txt`

### "Port 8547 already in use"
Another process is using the port. Either:
- Stop the other process
- Or change the port: `PORT=8548 python3 server.py`

### "No valid stores found"
Make sure you have store data:
```bash
ls -la ../stores/*/data/products.json
```

### ChatGPT can't connect
1. Check server is running (see Step 4)
2. Verify the URL: `http://localhost:8547/mcp`
3. Try reloading ChatGPT

## What's Next? 🎯

### Add More Stores
Run Weft scrapers to add more stores:
```bash
cd ../stores/your-store
npm install
npm start
```

The MCP server will automatically detect new stores!

### Customize
Edit `server.py` to add features:
- Order export
- Price tracking
- Custom filters

### Deploy
Want to access from anywhere? Deploy to:
- Google Cloud Run
- Railway
- Heroku
- Your own server

## Need Help? 💡

- Read the full [README](README.md)
- Check the [main Weft docs](../README.md)
- Review test output: `python3 test_setup.py`

---

**Happy shopping with AI! 🛒✨**


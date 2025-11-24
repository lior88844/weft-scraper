# 🤖 Nitzat Haduvdevan MCP Server

An MCP (Model Context Protocol) server that enables ChatGPT to browse and order from the Nitzat Haduvdevan store. Browse organic products, search by category, and manage your shopping cart directly through ChatGPT!

## 🌟 Features

- 🔍 **Search Products** - Find products by name or category from Nitzat Haduvdevan
- 🏪 **Single-Store Focus** - Always uses `stores/nitzat-haduvdevan/data/products.json`
- 🛒 **Shopping Cart** - Add items, view cart, remove items through ChatGPT
- 🖼️ **Visual Product Widget** - Beautiful product grid with images and prices in ChatGPT
- 💬 **Natural Language** - Just chat with ChatGPT: "Show me quinoa products"

## 📋 Prerequisites

- **Python 3.10 or higher** (required by fastmcp)
- ChatGPT Plus account (for MCP support)
- Nitzat Haduvdevan data in `../stores/nitzat-haduvdevan/data/products.json`

### Installing Python 3.10+

If you don't have Python 3.10+, install it using:

**macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Or download from python.org
# https://www.python.org/downloads/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11
```

**Windows:**
Download from https://www.python.org/downloads/

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd mcp-server
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python server.py
```

The server will start on `http://localhost:8547` and display available stores:

```
Starting Nitzat Haduvdevan MCP Server on port 8547
MCP endpoint: http://0.0.0.0:8547/mcp

Available stores (1):
  - nitzat-haduvdevan: 1325 products
```

### 3. Configure ChatGPT

1. Open ChatGPT Settings → **Beta Features** → Enable **MCP**
2. Add the server configuration from `chatgpt_config.json`:

```json
{
  "mcp_servers": {
    "nitzat-haduvdevan": {
      "url": "http://localhost:8547/mcp",
      "name": "Nitzat Haduvdevan Store",
      "description": "Browse and order from Nitzat Haduvdevan products",
      "transport": "http"
    }
  }
}
```

### 4. Start Chatting!

Open ChatGPT and try:
- "Show me all products from Nitzat Haduvdevan"
- "Find quinoa products"
- "What grains do you have?"
- "Add organic rice to my cart"
- "What's in my cart?"

## 💬 Example Conversations

### Browse Products
```
You: Show me quinoa products
ChatGPT: [Displays beautiful product grid with images]
Found 2 products:
• קינואה רויאל אורגנית, 500 גרם
  מחיר: 15.9 ₪
  קטגוריה: דגנים
```

### Add to Cart
```
You: Add the 500g quinoa to my cart
ChatGPT: ✓ המוצר נוסף לעגלה!

קינואה רויאל אורגנית, 500 גרם
כמות: 1

סה"כ פריטים בעגלה: 1
סכום כולל: 15.90 ₪
```

### View Cart
```
You: What's in my cart?
ChatGPT: 🛒 העגלה שלך:

• קינואה רויאל אורגנית, 500 גרם
  כמות: 1
  מחיר ליחידה: 15.9 ₪
  סה"כ: 15.90 ₪

**סה"כ לתשלום: 15.90 ₪**
```

## 🛠️ Available Tools

The MCP server provides these tools to ChatGPT:

1. **list_stores** - Show the Nitzat Haduvdevan store status
2. **search_products** - Search products by name or category
3. **add_to_cart** - Add a product to shopping cart
4. **view_cart** - View current cart contents
5. **remove_from_cart** - Remove an item from cart
6. **clear_cart** - Clear entire cart

## 📁 Project Structure

```
mcp-server/
├── server.py              # Main MCP server
├── requirements.txt       # Python dependencies
├── chatgpt_config.json    # ChatGPT MCP configuration
├── web/
│   └── dist/
│       └── products.html  # Product display widget
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional):

```bash
PORT=8547  # Server port (default: 8547)
```

### Data Source

The MCP server loads data from a single location:

```
stores/
└── nitzat-haduvdevan/
    └── data/
        └── products.json
```

The `products.json` format:
```json
{
  "scrapedAt": "2025-11-24T09:06:43.064Z",
  "totalProducts": 100,
  "products": [
    {
      "name": "Product Name",
      "price": "25.90",
      "category": "Category",
      "url": "product-url",
      "image": "path/to/image.jpg"
    }
  ]
}
```

## 🐛 Troubleshooting

### Server won't start
- **Check Python version**: `python3 --version` (need 3.10+)
  - If you have Python 3.9 or lower, fastmcp won't install
  - Install Python 3.10+ using the instructions above
- Verify dependencies: `pip3 install -r requirements.txt`
- Check port availability: Port 8547 might be in use

### ChatGPT can't connect
- Ensure server is running: `python server.py`
- Check the URL in ChatGPT settings: `http://localhost:8547/mcp`
- Verify MCP is enabled in ChatGPT Beta Features

### Products not showing
- Verify store data exists: `ls -la ../stores/nitzat-haduvdevan/data/products.json`
- Check server logs for errors
- Ensure JSON format is correct

### Widget not displaying
- Check browser console for errors (F12)
- Verify `web/dist/products.html` exists
- Check server logs for widget loading errors

## 🎯 How It Works

1. **Data Source**: Reads product data from `../stores/nitzat-haduvdevan/data/products.json`
2. **MCP Protocol**: Implements Model Context Protocol for ChatGPT integration
3. **Session Management**: Maintains shopping carts per ChatGPT session
4. **Widget**: Displays products in a beautiful interactive grid

## 🔒 Security Notes

- Server runs locally on your machine
- No external API calls or data transmission
- Shopping cart is stored in memory (not persistent)
- All data stays on your computer

## 📝 Development

### Run in Debug Mode

```bash
# Add logging
export PYTHONUNBUFFERED=1
python server.py
```

### Test Without ChatGPT

You can test the server endpoints directly:

```bash
# List stores
curl http://localhost:8547/mcp

# Search products (requires MCP client)
```

## 🤝 Contributing

1. Add new features to `server.py`
2. Update the widget in `web/dist/products.html`
3. Test with ChatGPT
4. Document changes in README

## 📜 License

ISC - Same as parent Weft project

## 🔗 Related Projects

- **Weft** - Multi-store product scraper (parent project)
- **FastMCP** - Python MCP framework
- **Model Context Protocol** - OpenAI's MCP specification

## 💡 Future Ideas

- [ ] Persistent cart storage (SQLite)
- [ ] Price tracking over time
- [ ] Multi-store comparison
- [ ] Order history
- [ ] Export shopping list
- [ ] WhatsApp/Email order links

## 👨‍💻 Author

Part of the Weft project by [lior88844](https://github.com/lior88844)

---

**Enjoy shopping with ChatGPT! 🛒✨**


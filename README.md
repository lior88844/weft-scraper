# 🛒 Weft - Multi-Store Product Scraper

A powerful product catalog system with **local scraping**, **web viewing**, and **ChatGPT integration**. 

## 🎯 Three-Part Architecture

1. **🖥️ Local Scraping** - Run scrapers on your computer to extract fresh data
2. **🌐 GitHub Pages** - Beautiful web viewer for your team (Free!)
3. **🤖 Railway MCP** - ChatGPT integration for AI-powered shopping ($5/month)

## 🌐 Live Demo

View all products: **[https://YOUR-USERNAME.github.io/Weft/](https://YOUR-USERNAME.github.io/Weft/)**  
ChatGPT MCP: **`https://your-app.railway.app/mcp`**

## 📋 Available Stores

### 🌿 Nitzat Haduvdevan
**Status:** ✅ Active  
**URL:** https://www.nizat.com/  
**Products:** 1,325 (as of last scrape)  
**Categories:** Snacks, nuts, grains, legumes, pasta, flour, spices, baking supplies  
**Description:** Organic and natural dry goods and pantry staples

[View Products](stores/nitzat-haduvdevan/index.html) | [Scraper README](stores/nitzat-haduvdevan/README.md)

### 🏪 Additional Stores
Coming soon... Add more stores by following the structure below.

## 🚀 Project Structure

```
Weft/
├── index.html              # Main landing page with store navigation
├── stores/                 # Individual store scrapers
│   ├── nitzat-haduvdevan/
│   │   ├── scraper.js     # Scraper script
│   │   ├── package.json   # Dependencies
│   │   ├── index.html     # Product viewer
│   │   ├── data/          # Scraped data
│   │   │   ├── products.json
│   │   │   └── products.js
│   │   └── README.md
│   └── [future-stores]/
├── mcp-server/            # 🆕 ChatGPT MCP integration
│   ├── server.py          # MCP server
│   ├── requirements.txt   # Python dependencies
│   ├── test_setup.py      # Setup validation script
│   ├── web/
│   │   └── dist/
│   │       └── products.html  # Product widget
│   └── README.md
└── README.md              # This file
```

## 🛠️ Adding a New Store

1. Create a new folder under `stores/`:
```bash
mkdir stores/your-store-name
```

2. Copy the template from an existing store:
```bash
cp -r stores/nitzat-haduvdevan/* stores/your-store-name/
```

3. Modify `scraper.js` with the new store's URL and selectors

4. Update `index.html` to add the new store card with:
   - Store name and icon
   - Description
   - Product count
   - Link to `stores/your-store-name/index.html`

5. Run the scraper:
```bash
cd stores/your-store-name
npm install
npm start
```

## 🚀 Quick Start

### 1. Run Scraper Locally

```bash
# Install dependencies (first time only)
npm install

# Run the scraper
npm run scrape
```

The scraper will:
1. Launch a headless browser
2. Extract product information
3. Save to `stores/nitzat-haduvdevan/data/products.json`

### 2. Deploy to GitHub Pages

```bash
# Commit the new data
git add stores/nitzat-haduvdevan/data/products.json
git commit -m "Update products"
git push origin main
```

Enable GitHub Pages:
- Go to **Settings** → **Pages**
- Source: **main** branch, **`/docs`** folder
- Your site will be live at: `https://YOUR-USERNAME.github.io/Weft/`

### 3. Deploy MCP to Railway

1. Go to [Railway.app](https://railway.app)
2. Create **New Project** → **Deploy from GitHub**
3. Select your Weft repository
4. Railway auto-deploys! ✨

Configure ChatGPT:
- URL: `https://your-app.railway.app/mcp`

📖 **Full workflow guide:** [WORKFLOW.md](WORKFLOW.md)

## 👀 Viewing Products

### For Your Team (GitHub Pages)
**URL:** `https://YOUR-USERNAME.github.io/Weft/`

Features:
- 🔍 Search products
- 🏷️ Filter by category
- 💰 Sort by price
- 📱 Mobile-friendly
- 🌐 Hebrew RTL support

### For ChatGPT (Railway MCP)
**URL:** `https://your-app.railway.app/mcp`

Example prompts:
- "Show me all quinoa products"
- "Add organic rice to my cart"
- "What's cheaper than 20 NIS?"

### Local Preview (During Development)
```bash
npm run serve
# Open http://localhost:8000
```

## 💰 Cost Breakdown

| Component | Hosting | Cost | Purpose |
|-----------|---------|------|---------|
| 🖥️ **Scraping** | Your Computer | **FREE** | Extract product data |
| 🌐 **Web Viewer** | GitHub Pages | **FREE** | Team product catalog |
| 🤖 **ChatGPT MCP** | Railway | **$5/month** | AI shopping assistant |

**Total:** **$5/month** (or FREE if you skip ChatGPT integration!)

## 🎯 Why This Architecture?

✅ **No expensive cloud scraping** - Chromium runs locally, not in the cloud  
✅ **Fast deployments** - No heavy dependencies, builds in seconds  
✅ **Cost effective** - GitHub Pages is free, Railway is $5/month  
✅ **Easy updates** - Just run scraper locally and push  
✅ **Team friendly** - Everyone can view products on GitHub Pages  
✅ **AI powered** - Optional ChatGPT integration for advanced features

## 📊 Features

- ✅ **Multi-store support** - Easily add new stores
- ✅ **Product images** - 100% image capture rate
- ✅ **Search & filter** - Find products quickly
- ✅ **Category navigation** - Browse by category
- ✅ **Price tracking** - Monitor product prices
- ✅ **Responsive design** - Works on all devices
- ✅ **Hebrew support** - Full RTL layout
- 🆕 **ChatGPT integration** - Shop through AI conversation

## 🔧 Configuration

Each store's scraper can be configured by editing `scraper.js`:

```javascript
const CONFIG = {
  baseUrl: 'https://example.com',
  maxCategories: 10,        // Number of categories to scrape
  delayBetweenRequests: 2000, // Delay in ms
  headless: true,           // Run in headless mode
  debug: false              // Enable debug mode
};
```

## 📁 Output Format

Each scraper generates:

### `data/products.json`
```json
{
  "scrapedAt": "2025-11-22T10:00:00.000Z",
  "totalProducts": 376,
  "products": [
    {
      "name": "Product Name",
      "price": "25.90",
      "category": "Category",
      "url": "/product/link",
      "image": "path/to/image.jpg"
    }
  ]
}
```

### `data/products.js`
JavaScript version for web viewer (automatically generated)

## 🤝 Contributing

1. Fork the repository
2. Add a new store under `stores/`
3. Test the scraper locally
4. Update the main `index.html` with the new store
5. Submit a pull request

## ⚖️ Legal Notice

Please ensure you comply with each store's Terms of Service and robots.txt when using these scrapers. This tool is for educational and research purposes only. Always respect:

- Website terms of service
- Rate limiting
- robots.txt directives
- Data privacy laws

## 📝 License

ISC

## 👨‍💻 Author

Created by [lior88844](https://github.com/lior88844)

## 🔗 Links

- **GitHub Repository:** https://github.com/lior88844/weft-scraper
- **Live Demo:** https://lior88844.github.io/weft-scraper/
- **Issues & Suggestions:** https://github.com/lior88844/weft-scraper/issues

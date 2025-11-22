# 🛒 Weft - Multi-Store Product Scraper

A collection of web scrapers for various online stores, built with Node.js and Puppeteer. Each scraper extracts product information and provides an interactive web viewer with images, search, and filtering capabilities.

## 🌐 Live Demo

View all scraped products online: **https://lior88844.github.io/weft-scraper/**

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

## 💻 Running Scrapers Locally

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation & Usage

Navigate to a specific store and run:

```bash
cd stores/nitzat-haduvdevan
npm install
npm start
```

The scraper will:
1. Launch a headless browser
2. Navigate to the store website
3. Extract product information
4. Save data to `data/products.json` and `data/products.js`

## 🌐 Viewing Results

### Option 1: Online (GitHub Pages)
Visit: https://lior88844.github.io/weft-scraper/

### Option 2: Local Web Server
```bash
# From project root
python3 -m http.server 8000
# Open http://localhost:8000/
```

### Option 3: Open Directly
Simply open `index.html` in your browser (some features may require a web server)

## 📊 Features

- ✅ **Multi-store support** - Easily add new stores
- ✅ **Product images** - 100% image capture rate
- ✅ **Search & filter** - Find products quickly
- ✅ **Category navigation** - Browse by category
- ✅ **Price tracking** - Monitor product prices
- ✅ **Responsive design** - Works on all devices
- ✅ **Hebrew support** - Full RTL layout

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

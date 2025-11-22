# Weft - Nitzat Haduvdevan Product Scraper

A Node.js web scraper that extracts product information from [Nitzat Haduvdevan](https://www.nizat.com/) using Puppeteer and saves the data in JSON format.

## 🌐 Live Demo

View the scraped products online: **[GitHub Pages Link]** (will be available after deployment)

## Features

- 🚀 Automated product scraping using Puppeteer
- 📦 Extracts product names, prices, categories, URLs, and images
- 🇮🇱 Handles Hebrew language content properly
- 💾 Exports data to JSON format
- ⏱️ Includes rate limiting to be respectful to the server
- 🍪 Automatically handles cookie consent dialogs

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn

## Installation

1. Navigate to the project directory:
```bash
cd /Users/lior/development/Weft
```

2. Install dependencies:
```bash
npm install
```

This will install Puppeteer and all required dependencies (including Chromium browser).

## Usage

Run the scraper using one of these commands:

```bash
npm start
```

or

```bash
npm run scrape
```

or

```bash
node scraper.js
```

The scraper will:
1. Launch a headless browser
2. Navigate to Nitzat Haduvdevan website
3. Extract categories from the main menu
4. Scrape products from each category
5. Save the results to `data/products.json`

## Output Format

The scraper generates a JSON file in the `data/` directory with the following structure:

```json
{
  "scrapedAt": "2025-11-22T10:30:00.000Z",
  "totalProducts": 150,
  "products": [
    {
      "name": "Product Name",
      "price": "25.90",
      "category": "Category Name",
      "url": "/product/example",
      "image": "https://example.com/image.jpg"
    }
  ]
}
```

### Fields Description

- `scrapedAt`: Timestamp of when the scraping was performed
- `totalProducts`: Total number of products scraped
- `products`: Array of product objects containing:
  - `name`: Product name (string)
  - `price`: Product price (string)
  - `category`: Category name (string)
  - `url`: Product page URL (string)
  - `image`: Product image URL (string)

## Configuration

You can modify the scraper settings by editing the `CONFIG` object in `scraper.js`:

```javascript
const CONFIG = {
  baseUrl: 'https://www.nizat.com',
  outputDir: path.join(__dirname, 'data'),
  outputFile: 'products.json',
  delayBetweenRequests: 2000, // milliseconds
  headless: true,
  userAgent: '...'
};
```

### Configuration Options

- `baseUrl`: The base URL of the website to scrape
- `outputDir`: Directory where JSON output will be saved
- `outputFile`: Name of the output JSON file
- `delayBetweenRequests`: Delay between page requests (in milliseconds)
- `headless`: Run browser in headless mode (true/false)
- `userAgent`: Custom user agent string

## Troubleshooting

### Puppeteer Installation Issues

If Puppeteer fails to download Chromium:

```bash
npm install puppeteer --unsafe-perm=true --allow-root
```

### Timeout Errors

If you encounter timeout errors, try increasing the timeout value in the `page.goto()` calls in `scraper.js`.

### Missing Products

The scraper uses generic selectors to find products. If the website structure changes, you may need to update the selectors in the `page.evaluate()` function.

## Notes

- The scraper is configured to respect the server by including delays between requests
- Currently limited to the first 5 categories for testing purposes (remove limit in line 98 of `scraper.js`)
- The scraper handles Hebrew text encoding properly with UTF-8

## Viewing Scraped Products

### Option 1: Online Viewer (GitHub Pages)
Open `index.html` in your browser or visit the GitHub Pages URL to see all scraped products with images, search, and filtering capabilities.

### Option 2: Local Web Server
```bash
cd /Users/lior/development/Weft
python3 -m http.server 8000
```
Then open: http://localhost:8000/

### Product Data Files
- `data/products.json` - Raw JSON data with all product information
- `data/products.js` - JavaScript version for the web viewer
- `index.html` - Interactive product viewer with images

## Legal Notice

Please ensure you comply with Nitzat Haduvdevan's Terms of Service and robots.txt when using this scraper. This tool is for educational purposes only.

## License

ISC


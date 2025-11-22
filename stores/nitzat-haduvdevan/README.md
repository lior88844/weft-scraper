# Nitzat Haduvdevan Scraper

Web scraper for [Nitzat Haduvdevan](https://www.nizat.com/) - an organic and natural products store.

## Running the Scraper

```bash
cd stores/nitzat-haduvdevan
npm install
npm start
```

## Configuration

Edit `scraper.js` to modify:
- `maxCategories`: Number of categories to scrape (default: 10)
- `delayBetweenRequests`: Delay in milliseconds (default: 2000ms)
- `headless`: Run browser in headless mode (default: true)

## Output

- `data/products.json` - Raw product data
- `data/products.js` - JavaScript format for web viewer
- `index.html` - Product viewer with images

## Data Structure

Each product includes:
- `name` - Product name
- `price` - Product price (when available)
- `category` - Product category
- `url` - Product page URL
- `image` - Product image path


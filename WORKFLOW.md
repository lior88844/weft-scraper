# 🔄 Weft Workflow Guide

This guide explains the complete workflow for scraping, viewing, and deploying Weft product data.

## Architecture Overview

```
┌─────────────────┐
│  Your Computer  │
│   (Scraping)    │
└────────┬────────┘
         │
         ↓ Run scraper
┌─────────────────┐
│ products.json   │
└────────┬────────┘
         │
         ↓ Git commit & push
         │
    ┌────┴────┐
    │         │
    ↓         ↓
┌─────────┐ ┌──────────┐
│ GitHub  │ │ Railway  │
│  Pages  │ │   MCP    │
└─────────┘ └──────────┘
    │            │
    ↓            ↓
Coworkers    ChatGPT
 (View)       (Use)
```

## Step 1: Run Scraper Locally

Run the scraper on your computer to extract fresh product data:

```bash
# Install dependencies (first time only)
npm install

# Run the scraper
npm run scrape
```

This creates/updates: `stores/nitzat-haduvdevan/data/products.json`

## Step 2: Review Data

Check the generated data:

```bash
# View products locally in browser
npm run serve
```

Open: http://localhost:8000

## Step 3: Commit to GitHub

Once you're happy with the data:

```bash
git add stores/nitzat-haduvdevan/data/products.json
git commit -m "Update product data - $(date +%Y-%m-%d)"
git push origin main
```

## Step 4: Deploy to GitHub Pages

### First Time Setup

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **main** / Folder: **`/docs`**
5. Click **Save**

After 1-2 minutes, your site will be live at:
`https://YOUR-USERNAME.github.io/Weft/`

### Automatic Updates

Every time you push to `main`, GitHub Pages automatically updates.

## Step 5: Deploy MCP to Railway

### First Time Setup

1. Go to [Railway.app](https://railway.app)
2. Create **New Project** → **Deploy from GitHub repo**
3. Select your Weft repository
4. Railway will auto-detect and deploy

### Environment Variables

In Railway dashboard, add:
- `PORT`: `8547` (or any port you prefer)

### Automatic Updates

Every time you push to `main`, Railway automatically redeploys.

## Step 6: Configure ChatGPT

Add the MCP server to ChatGPT:

1. Go to ChatGPT Settings
2. Add Custom GPT Action
3. URL: `https://your-app.railway.app/mcp`
4. Name: "Weft Store Browser"

## Usage Examples

### For Coworkers (GitHub Pages)

- **View all products**: Visit your GitHub Pages URL
- **Search products**: Use the search box
- **Filter by category**: Use category dropdown
- **Sort by price**: Use sort dropdown

### For ChatGPT (Railway MCP)

Example prompts:
- "Show me all products from Nitzat Haduvdevan"
- "What grains are available?"
- "Add quinoa to my cart"
- "Show me products under 20 NIS"

## File Structure

```
Weft/
├── scraper.js                           # Local scraping script
├── package.json                         # Node dependencies
├── stores/
│   └── nitzat-haduvdevan/
│       └── data/
│           └── products.json            # Generated data
├── docs/
│   └── index.html                       # GitHub Pages site
├── mcp-server/
│   ├── server.py                        # Railway MCP server
│   └── requirements.txt                 # Python dependencies
└── WORKFLOW.md                          # This file
```

## Maintenance Schedule

### Daily/Weekly (as needed)
- Run scraper locally
- Commit and push updates

### The system handles automatically:
- ✅ GitHub Pages deployment
- ✅ Railway MCP deployment
- ✅ Data serving to ChatGPT

## Troubleshooting

### GitHub Pages not updating?
- Wait 2-3 minutes after push
- Check Settings → Pages for build status
- Ensure `/docs` folder is committed

### Railway not deploying?
- Check Railway logs
- Verify `requirements.txt` has all dependencies
- Ensure `railway.json` is in root

### MCP not working in ChatGPT?
- Verify Railway app is running
- Test endpoint: `https://your-app.railway.app/mcp`
- Check Railway logs for errors

### Scraper failing locally?
- Update dependencies: `npm install`
- Check website hasn't changed structure
- Run with debug: `node scraper.js`

## Cost Breakdown

| Service | Cost | Purpose |
|---------|------|---------|
| Local Scraping | Free | Run on your computer |
| GitHub Pages | Free | Static site hosting |
| Railway (Hobby) | $5/month | MCP server hosting |

**Total: $5/month** (Railway only)

## Benefits of This Architecture

✅ **No expensive cloud scraping** - Runs on your computer  
✅ **Free viewer** - GitHub Pages is free for public repos  
✅ **Lightweight deployment** - No Chromium/Puppeteer in cloud  
✅ **Fast builds** - Railway deploys in seconds  
✅ **Easy updates** - Just run scraper and push  
✅ **Cost effective** - Only $5/month for MCP hosting  

## Next Steps

1. Run your first scrape: `npm run scrape`
2. Enable GitHub Pages (Settings → Pages)
3. Deploy to Railway
4. Share GitHub Pages URL with coworkers
5. Configure ChatGPT MCP

---

**Questions?** Check the main [README.md](README.md) or open an issue.


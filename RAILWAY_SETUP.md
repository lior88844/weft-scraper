# 🚂 Railway Deployment Guide

Deploy your MCP server to Railway for ChatGPT integration.

## 🎯 What You'll Get

- Live MCP endpoint: `https://your-app.railway.app/mcp`
- ChatGPT integration ready
- Automatic deployments on git push
- Cost: $5/month (Hobby Plan)

## ⚡ Quick Setup (5 minutes)

### Step 1: Create Railway Account

1. Go to [Railway.app](https://railway.app)
2. Click **Login** → **Login with GitHub**
3. Authorize Railway to access your GitHub

### Step 2: Create New Project

1. Click **New Project**
2. Select **Deploy from GitHub repo**
3. Choose your **Weft** repository
4. Railway detects Python automatically ✨

### Step 3: Configure Environment

Railway should auto-detect everything, but verify:

- **Build Command:** `pip install -r mcp-server/requirements.txt`
- **Start Command:** `cd mcp-server && python server.py`
- **Port:** Railway auto-assigns (dynamic)

### Step 4: Add Environment Variable (Optional)

If you want a specific port:

1. Click your project
2. Go to **Variables** tab
3. Add: `PORT` = `8547`

### Step 5: Deploy!

- Railway automatically starts building
- First deploy takes 1-2 minutes
- Watch logs in real-time

### Step 6: Get Your URL

1. Go to **Settings** tab
2. Click **Generate Domain**
3. Your URL: `https://your-app-name.railway.app`

## 🤖 Configure ChatGPT

### For ChatGPT with Custom Actions

1. Go to ChatGPT Settings
2. **Beta Features** → **Actions**
3. Add new action:
   - URL: `https://your-app.railway.app/mcp`
   - Name: "Weft Store Browser"
   - Description: "Browse Nitzat Haduvdevan products"

### For MCP-Compatible Clients

Add to your MCP client config:

```json
{
  "mcpServers": {
    "weft": {
      "url": "https://your-app.railway.app/mcp",
      "transport": "http"
    }
  }
}
```

## 🔄 Automatic Deployments

Every time you push to `main`:

```bash
git add stores/nitzat-haduvdevan/data/products.json
git commit -m "Update products"
git push origin main
```

Railway automatically:
1. Detects the change
2. Rebuilds the container
3. Deploys new version
4. Keeps zero downtime

## 📊 Monitoring

### View Logs

1. Go to your Railway project
2. Click **Deployments** tab
3. Click latest deployment
4. View real-time logs

### Check Health

Visit: `https://your-app.railway.app/`

Should return:
```json
{
  "status": "healthy",
  "stores": ["nitzat-haduvdevan"]
}
```

### Test MCP Endpoint

Visit: `https://your-app.railway.app/mcp`

Should return MCP server info.

## 💰 Pricing

### Hobby Plan ($5/month)
- Perfect for personal use
- 500 hours of runtime/month
- 8GB RAM
- 8GB storage
- Your MCP server runs 24/7

### Pro Plan ($20/month)
- For teams
- Unlimited hours
- 32GB RAM
- Priority support

**Estimated cost for Weft:** $5/month

## 🐛 Troubleshooting

### Build Failed?

Check Railway logs for errors:

1. Click **Deployments**
2. Click failed deployment
3. Look for error messages

Common issues:
- Missing `requirements.txt`
- Wrong Python version (needs 3.10+)
- Missing `mcp-server/` directory

### App Crashes on Start?

Check logs for:
```
ModuleNotFoundError: No module named 'fastmcp'
```

Fix:
1. Verify `mcp-server/requirements.txt` exists
2. Check build command includes: `pip install -r mcp-server/requirements.txt`

### Products Not Loading?

Verify:
1. `stores/nitzat-haduvdevan/data/products.json` exists in repo
2. JSON file is valid
3. Path is correct in `server.py`:
   ```python
   STORES_DIR = PROJECT_ROOT / "stores"
   ```

### MCP Not Responding?

1. Check Railway logs for errors
2. Verify domain is generated
3. Test endpoint: `curl https://your-app.railway.app/mcp`
4. Check firewall isn't blocking Railway

## 🔒 Security

### Environment Variables

Store sensitive data in Railway:

1. Go to **Variables** tab
2. Add variables (they're encrypted)
3. Access in Python:
   ```python
   import os
   api_key = os.getenv('API_KEY')
   ```

### Make Repository Private

If you want to keep code private:

1. Go to GitHub repo **Settings**
2. Scroll to **Danger Zone**
3. Click **Change visibility** → **Private**
4. Railway still has access via OAuth

## 🚀 Advanced Features

### Custom Domain

1. Go to **Settings** → **Domains**
2. Add custom domain: `api.yourstore.com`
3. Add CNAME record at your DNS provider:
   ```
   CNAME api.yourstore.com your-app.railway.app
   ```

### Multiple Environments

Create staging environment:

1. Duplicate project
2. Point to `develop` branch
3. Test changes before production

### Rollback Deployment

1. Go to **Deployments**
2. Click previous working deployment
3. Click **Redeploy**

## 📝 Configuration Files

Railway uses these files (already set up):

### `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r mcp-server/requirements.txt"
  },
  "deploy": {
    "startCommand": "cd mcp-server && python server.py"
  }
}
```

### `mcp-server/Procfile`
```
web: python server.py
```

### `mcp-server/requirements.txt`
```
fastmcp
httpx
python-dotenv
mcp
```

## ✅ Deployment Checklist

Before deploying:

- [ ] GitHub repository is public (or Railway has access)
- [ ] `mcp-server/requirements.txt` exists
- [ ] `mcp-server/server.py` exists
- [ ] `stores/nitzat-haduvdevan/data/products.json` has data
- [ ] Tested locally: `cd mcp-server && python server.py`

After deploying:

- [ ] Railway build succeeded (green checkmark)
- [ ] Generated domain
- [ ] Visited `https://your-app.railway.app/` (returns JSON)
- [ ] Tested MCP endpoint: `https://your-app.railway.app/mcp`
- [ ] Added to ChatGPT (if using)

## 🎉 You're Live!

Your MCP server is now running 24/7 at:
```
https://your-app.railway.app/mcp
```

ChatGPT can now:
- 🔍 Search your products
- 🛒 Add items to cart
- 💰 Calculate totals
- 📦 View product details

---

**Questions?** Check [WORKFLOW.md](WORKFLOW.md) or [README.md](README.md)


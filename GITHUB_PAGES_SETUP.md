# 📄 GitHub Pages Setup Guide

Quick guide to enable GitHub Pages for your Weft product viewer.

## 🎯 What You'll Get

A free, public website at: `https://YOUR-USERNAME.github.io/Weft/`

## ⚡ Quick Setup (2 minutes)

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**

### Step 2: Wait for Deployment

- First deployment takes 2-3 minutes
- You'll see a green checkmark when ready
- GitHub will show your site URL

### Step 3: Visit Your Site

Your product catalog is now live at:
```
https://YOUR-USERNAME.github.io/Weft/
```

## 🔄 Automatic Updates

Every time you push product data:

```bash
git add stores/nitzat-haduvdevan/data/products.json
git commit -m "Update products"
git push origin main
```

GitHub Pages automatically updates in 1-2 minutes! ✨

## 📊 Features Available

✅ **Search products** - Real-time filtering  
✅ **Category filters** - Browse by category  
✅ **Sort options** - By name or price  
✅ **Mobile responsive** - Works on all devices  
✅ **Hebrew support** - Full RTL layout  
✅ **Beautiful UI** - Modern gradient design

## 🔒 Privacy Options

### Option 1: Public (Free)
- Repository: Public
- Anyone can view your site
- Perfect for team sharing

### Option 2: Private (GitHub Pro)
- Repository: Private
- Only invited collaborators can view
- Requires GitHub Pro ($4/month)

## 🛠️ Customization

### Change Site Colors

Edit `docs/index.html` and modify the CSS gradient:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Try these color schemes:
- **Ocean:** `#2E3192 0%, #1BFFFF 100%`
- **Sunset:** `#FA8BFF 0%, #2BD2FF 100%`
- **Forest:** `#134E5E 0%, #71B280 100%`

### Add Your Logo

Replace the emoji in the `<h1>` tag:

```html
<h1>🛒 Your Store Name</h1>
<!-- Change to: -->
<h1><img src="logo.png" alt="Logo"> Your Store Name</h1>
```

## 🐛 Troubleshooting

### Site not updating?
1. Check **Actions** tab for build status
2. Ensure `/docs` folder is committed
3. Wait 2-3 minutes after push
4. Clear browser cache (Cmd+Shift+R)

### 404 Error?
1. Verify Pages is enabled (Settings → Pages)
2. Check branch is `main` and folder is `/docs`
3. Ensure `docs/index.html` exists in repository

### Products not showing?
1. Check browser console for errors (F12)
2. Verify `stores/nitzat-haduvdevan/data/products.json` exists
3. Check JSON file is valid (use JSONLint.com)

### Images not loading?
- Image paths are relative to repository
- GitHub Pages may take longer to serve images
- Check image URLs in products.json

## 📱 Share With Your Team

Send them the link:
```
https://YOUR-USERNAME.github.io/Weft/
```

They can:
- 🔍 Search for products
- 🏷️ Filter by category
- 💰 Compare prices
- 📱 View on any device

**No login required!** It's a public site.

## 🚀 Next Steps

1. ✅ Enable GitHub Pages (you just did!)
2. 📊 Run your first scrape: `npm run scrape`
3. 📤 Push data: `git push origin main`
4. 🎉 Share the link with your team
5. 🤖 Optional: Deploy MCP to Railway for ChatGPT

---

**Questions?** Check [WORKFLOW.md](WORKFLOW.md) or [README.md](README.md)


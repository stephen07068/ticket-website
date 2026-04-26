# Deployment Guide - TicketHubLive

## 🚀 Deploy to GitHub

### Step 1: Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit - TicketHubLive event ticketing platform"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `tickethublive` (or your preferred name)
3. Description: "Event ticketing platform with crypto payments and admin dashboard"
4. Choose: Public or Private
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

### Step 3: Connect and Push

```bash
git remote add origin https://github.com/YOUR_USERNAME/tickethublive.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## 🌐 Deploy to GitHub Pages (Frontend Only)

GitHub Pages can host the static HTML files, but you'll need a separate backend host for the Python Flask API.

### Option 1: Static Demo (No Backend)

```bash
# Create gh-pages branch
git checkout -b gh-pages

# Push to GitHub Pages
git push origin gh-pages
```

Then enable GitHub Pages in repository settings:
- Settings → Pages → Source: gh-pages branch

**Note**: This will only show the frontend. Backend features won't work.

---

## 🔧 Deploy Full Stack (Recommended Options)

### Option A: Render.com (Free Tier Available)

1. **Push to GitHub** (follow steps above)
2. Go to https://render.com
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Name: `tickethublive`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
6. Click "Create Web Service"

**Environment Variables to Add:**
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

### Option B: Railway.app (Free Tier Available)

1. **Push to GitHub** (follow steps above)
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys!

### Option C: PythonAnywhere (Free Tier Available)

1. **Push to GitHub** (follow steps above)
2. Go to https://www.pythonanywhere.com
3. Create free account
4. Open Bash console
5. Clone your repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/tickethublive.git
   cd tickethublive
   pip install -r requirements.txt
   ```
6. Set up web app in Web tab

### Option D: Heroku

1. **Push to GitHub** (follow steps above)
2. Create `Procfile`:
   ```
   web: python app.py
   ```
3. Install Heroku CLI
4. Deploy:
   ```bash
   heroku login
   heroku create tickethublive
   git push heroku main
   ```

---

## 📋 Pre-Deployment Checklist

- [x] All bugs fixed
- [x] .gitignore created
- [x] requirements.txt exists
- [x] README.md updated
- [ ] Change admin password in production
- [ ] Set up environment variables
- [ ] Configure CORS for production domain
- [ ] Set up database backups
- [ ] Add SSL certificate (HTTPS)

---

## 🔐 Security Notes for Production

1. **Change Admin Credentials**:
   - Update `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `app.py`
   - Use environment variables instead of hardcoding

2. **Update CORS Settings**:
   ```python
   # In app.py, change:
   CORS(app)
   # To:
   CORS(app, origins=['https://yourdomain.com'])
   ```

3. **Use Environment Variables**:
   ```python
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
   ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@tickethublive.com')
   ```

4. **Enable HTTPS**: Most hosting platforms provide free SSL

---

## 📞 Support

For deployment issues:
- WhatsApp: +1 (478) 233-8453
- Email: tickethublive@gmail.com

---

## 🎉 Quick Deploy Commands

```bash
# 1. Initialize and commit
git init
git add .
git commit -m "Initial commit - TicketHubLive"

# 2. Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/tickethublive.git
git branch -M main
git push -u origin main

# 3. Deploy to Render/Railway/PythonAnywhere (follow their docs)
```

**That's it! Your TicketHubLive platform is now on GitHub! 🚀**

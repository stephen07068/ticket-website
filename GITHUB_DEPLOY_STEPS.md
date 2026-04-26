# 🚀 Deploy TicketHubLive to GitHub - Simple Steps

## Method 1: Using the Automated Script (Easiest)

### Step 1: Run the deployment script
```bash
deploy-to-github.bat
```

Follow the prompts and you're done! ✅

---

## Method 2: Manual Deployment (Step by Step)

### Step 1: Initialize Git (if not already done)

Open Command Prompt or PowerShell in your project folder and run:

```bash
git init
```

### Step 2: Add all files

```bash
git add .
```

### Step 3: Commit your code

```bash
git commit -m "Initial commit - TicketHubLive platform"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `tickethublive` (or any name you want)
   - **Description**: "Event ticketing platform with crypto payments"
   - **Visibility**: Choose Public or Private
3. **IMPORTANT**: Do NOT check "Initialize with README"
4. Click **"Create repository"**

### Step 5: Connect to GitHub

Copy the commands from GitHub (they look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/tickethublive.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 6: Push your code

```bash
git push -u origin main
```

**Done! Your code is now on GitHub! 🎉**

---

## Verify Deployment

1. Go to your GitHub repository URL
2. You should see all your files listed
3. Check that these files are present:
   - ✅ app.py
   - ✅ models.py
   - ✅ index.html
   - ✅ requirements.txt
   - ✅ README.md

---

## Next Steps: Deploy to Live Server

Your code is on GitHub, but you need a server to run the Python backend.

### Option A: Render.com (Recommended - Free Tier)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your `tickethublive` repository
5. Configure:
   - **Name**: tickethublive
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. Your site will be live at: `https://tickethublive.onrender.com`

### Option B: Railway.app (Easiest - Free Tier)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `tickethublive` repository
5. Railway automatically detects Python and deploys!
6. Your site will be live in 1-2 minutes

### Option C: PythonAnywhere (Free Tier)

1. Go to https://www.pythonanywhere.com
2. Create free account
3. Open Bash console
4. Run:
   ```bash
   git clone https://github.com/YOUR_USERNAME/tickethublive.git
   cd tickethublive
   pip install -r requirements.txt
   ```
5. Set up web app in the Web tab
6. Point it to your `app.py` file

---

## Troubleshooting

### "Permission denied" error
```bash
# You need to authenticate with GitHub
# Use GitHub Desktop or set up SSH keys
```

### "Repository not found" error
```bash
# Check your repository URL is correct
git remote -v
# If wrong, remove and re-add:
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/tickethublive.git
```

### "Failed to push" error
```bash
# Try force push (only if it's a new repo)
git push -u origin main --force
```

### Need to update after changes
```bash
git add .
git commit -m "Updated features"
git push
```

---

## 📞 Need Help?

- WhatsApp: +1 (478) 233-8453
- Email: tickethublive@gmail.com

---

## 🎉 Congratulations!

Your TicketHubLive platform is now:
- ✅ Version controlled with Git
- ✅ Backed up on GitHub
- ✅ Ready to deploy to any hosting platform
- ✅ Shareable with your team

**Happy deploying! 🚀**

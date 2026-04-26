# 🔧 TicketHubLive - Troubleshooting Guide

## ✅ Server is Running!

Your Flask server is currently running on **http://localhost:5000**

---

## 🌐 How to Access the Website

### Method 1: Direct URL
1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Type in the address bar: `http://localhost:5000`
3. Press Enter

### Method 2: Use the Launcher
1. Double-click `OPEN_WEBSITE.html` in this folder
2. It will automatically redirect to the website

### Method 3: Copy-Paste
Copy this URL and paste it in your browser:
```
http://localhost:5000
```

---

## 🚨 Common Issues & Solutions

### Issue 1: "This site can't be reached"

**Solution A: Check if server is running**
```bash
# Look for this message in your terminal:
# "Running on http://127.0.0.1:5000"
```

**Solution B: Restart the server**
1. Press `Ctrl+C` in the terminal to stop
2. Run: `python app.py`
3. Wait for "Running on http://127.0.0.1:5000"
4. Try accessing again

### Issue 2: Port 5000 already in use

**Solution: Use a different port**
1. Open `app.py`
2. Find the last line: `app.run(debug=True, port=5000)`
3. Change to: `app.run(debug=True, port=5001)`
4. Save and restart
5. Access at: `http://localhost:5001`

### Issue 3: Browser shows "Connection refused"

**Solution: Check firewall**
1. Windows Firewall might be blocking
2. Allow Python through firewall
3. Or try: `http://127.0.0.1:5000` instead

### Issue 4: Page loads but shows errors

**Solution: Check dependencies**
```bash
pip install -r requirements.txt
```

### Issue 5: Database errors

**Solution: Reset database**
```bash
# Delete the database file
del tickethub.db

# Restart the server (it will recreate the database)
python app.py
```

### Issue 6: Create Event button not working in Admin Panel

**Most Common Cause: Browser Cache**

**Solution A: Hard Refresh (Try this first!)**
1. Open the admin page: `http://localhost:5000/admin.html`
2. Press one of these key combinations:
   - **Windows/Linux:** `Ctrl + Shift + R` or `Ctrl + F5`
   - **Mac:** `Cmd + Shift + R`
3. This forces the browser to reload all files from the server
4. Try clicking "Create Event" again

**Solution B: Clear Browser Cache**
1. Press `F12` to open Developer Tools
2. Right-click the refresh button in your browser
3. Select "Empty Cache and Hard Reload"
4. Close Developer Tools
5. Try again

**Solution C: Check Console for Errors**
1. Press `F12` to open Developer Tools
2. Click the "Console" tab
3. Click the "Create Event" button
4. Look for messages starting with "createEvent function called"
5. If you see errors, note them down
6. If you see nothing, the JavaScript file hasn't loaded (go back to Solution A)

**Solution D: Disable Cache in Browser**
1. Press `F12` to open Developer Tools
2. Click the "Network" tab
3. Check the box "Disable cache"
4. Keep Developer Tools open
5. Refresh the page
6. Try clicking "Create Event"

**Solution E: Try Incognito/Private Mode**
1. Open a new Incognito/Private window
2. Go to: `http://localhost:5000/admin-login.html`
3. Login with admin credentials
4. Try creating an event
5. If it works, your regular browser has cached old files

---

## 📋 Quick Checklist

Before accessing the website, verify:

- [ ] Terminal shows: "Running on http://127.0.0.1:5000"
- [ ] No error messages in terminal
- [ ] Port 5000 is not used by another application
- [ ] Python packages are installed (`pip install -r requirements.txt`)
- [ ] You're using the correct URL: `http://localhost:5000`

---

## 🔍 Verify Server Status

### Check if server is running:
```bash
# Windows PowerShell
Test-NetConnection -ComputerName localhost -Port 5000
```

### Check server logs:
Look at your terminal where you ran `python app.py`. You should see:
```
[OK] TicketHubLive API running at http://localhost:5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## 🌐 Alternative Access Methods

### Try these URLs (all should work):
1. `http://localhost:5000`
2. `http://127.0.0.1:5000`
3. `http://0.0.0.0:5000`

### Access from another device on same network:
1. Find your computer's IP address:
   ```bash
   ipconfig
   # Look for "IPv4 Address"
   ```
2. Use: `http://YOUR_IP:5000`
   Example: `http://192.168.1.100:5000`

---

## 📱 Test the API

### Quick API Test:
Open your browser and try these URLs:

1. **Get Events:**
   ```
   http://localhost:5000/api/events
   ```
   Should show JSON with event list

2. **Get Single Event:**
   ```
   http://localhost:5000/api/events/1
   ```
   Should show JSON with event details

3. **Get Wallets:**
   ```
   http://localhost:5000/api/wallets
   ```
   Should show crypto wallet addresses

If these work, your server is running correctly!

---

## 🖥️ Browser Compatibility

Tested and working on:
- ✅ Google Chrome (Recommended)
- ✅ Microsoft Edge
- ✅ Mozilla Firefox
- ✅ Safari
- ✅ Opera

---

## 📞 Still Having Issues?

### Check these files exist:
- [ ] `app.py` - Backend server
- [ ] `models.py` - Database models
- [ ] `index.html` - Home page
- [ ] `lib/api.js` - API layer
- [ ] `requirements.txt` - Dependencies

### Verify Python version:
```bash
python --version
# Should be 3.7 or higher
```

### Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Check for port conflicts:
```bash
# Windows
netstat -ano | findstr :5000

# If something is using port 5000, kill it or use a different port
```

---

## ✅ Success Indicators

You'll know it's working when:
1. ✅ Terminal shows "Running on http://127.0.0.1:5000"
2. ✅ Browser loads the TicketHubLive home page
3. ✅ You see event cards with images
4. ✅ Category filters work
5. ✅ No console errors (F12 → Console tab)

---

## 🎯 Quick Start Commands

### Start the server:
```bash
python app.py
```

### Stop the server:
Press `Ctrl+C` in the terminal

### Restart the server:
1. Press `Ctrl+C`
2. Run `python app.py` again

---

## 📊 Server Information

**Current Status:** ✅ RUNNING

**Server Details:**
- URL: http://localhost:5000
- Port: 5000
- Debug Mode: ON
- Database: tickethub.db (SQLite)
- API Base: http://localhost:5000/api

**Admin Access:**
- URL: http://localhost:5000/admin-login.html
- Email: admin@tickethublive.com
- Password: Admin@1234

---

## 🎉 Next Steps

Once the website loads:
1. Browse events on the home page
2. Click "Buy Ticket" on any event
3. Complete a test purchase
4. Login to admin panel to approve orders
5. View your ticket with QR code

---

**Need more help?** Check these files:
- `README.md` - Complete documentation
- `QUICK_START.md` - Setup guide
- `TEST_BUTTONS.md` - Testing guide

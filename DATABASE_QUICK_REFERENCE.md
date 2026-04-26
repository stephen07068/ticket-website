# 🗄️ Database Quick Reference

## ✅ Current Status

- **Type**: SQLite (local) or PostgreSQL (production via Supabase)
- **Local File**: `tickethub.db` (SQLite)
- **Production**: Supabase PostgreSQL (cloud-hosted)
- **Status**: ✅ Auto-creates on first run
- **Git**: ✅ Database files excluded from repository (.gitignore)
- **Switching**: ✅ Automatic based on `DATABASE_URL` environment variable

## 🚀 What Happens When You Deploy

### Local Development
```
python app.py
↓
Creates: tickethub.db (in your folder)
↓
Seeds 6 demo events automatically
```

### On GitHub
```
git push
↓
tickethub.db is NOT uploaded (excluded by .gitignore)
↓
This is correct! ✅
```

### On Production Server (Render/Railway/etc)
```
Deploy from GitHub
↓
Server runs: python app.py
↓
Creates NEW tickethub.db on server
↓
Seeds demo events automatically
↓
Your production database is ready! ✅
```

## 📊 Database Contents

### Tables Created Automatically:
1. **events** - All events (concerts, sports, etc.)
2. **ticket_tiers** - Ticket types (VIP, Regular, etc.)
3. **orders** - Customer orders
4. **tickets** - Generated tickets with QR codes

### Sample Data Included:
- ✅ 6 demo events (concerts, sports, festivals)
- ✅ Multiple ticket tiers per event
- ✅ Ready to use immediately

## 🔄 Common Operations

### View Database (Local)
```bash
# Install DB Browser for SQLite
# Download: https://sqlitebrowser.org/
# Open: tickethub.db
```

### Backup Database
```bash
# Windows
copy tickethub.db backup_tickethub.db

# Mac/Linux
cp tickethub.db backup_tickethub.db
```

### Reset Database
```bash
# Windows
del tickethub.db
python app.py

# Mac/Linux
rm tickethub.db
python app.py
```

### Export Data (Before Deployment)
```python
# Run this Python script to export your data
import sqlite3
import json

conn = sqlite3.connect('tickethub.db')
cursor = conn.cursor()

# Export events
cursor.execute("SELECT * FROM events")
events = cursor.fetchall()
print("Events:", events)

# Export orders
cursor.execute("SELECT * FROM orders")
orders = cursor.fetchall()
print("Orders:", orders)

conn.close()
```

## ⚠️ Important Notes

### 1. Database is NOT in Git
- ✅ This is correct and intentional
- ✅ Each environment has its own database
- ✅ Prevents data conflicts

### 2. Production Database is Separate
- ✅ Local database: Your computer
- ✅ Production database: On server
- ✅ They are independent

### 3. Data Migration
If you have important data locally and want it in production:

**Option A: Manual Entry**
- Use admin panel to recreate events on production

**Option B: Database Upload**
- Download local `tickethub.db`
- Upload to production server (platform-specific)

**Option C: SQL Export/Import**
```bash
# Export from local
sqlite3 tickethub.db .dump > backup.sql

# Import to production (if using SQLite)
sqlite3 tickethub.db < backup.sql
```

## 🔧 Upgrade to PostgreSQL (Recommended for Production)

### When to Use PostgreSQL:
- ⬆️ Production deployment
- ⬆️ More than 1,000 orders
- ⬆️ High traffic (50+ concurrent users)
- ⬆️ Need better performance and reliability
- ⬆️ Using Supabase for event storage

### How to Set Up (Already Configured!):
Your app is already configured to support PostgreSQL! Just follow these steps:

1. **Install Dependencies** (already in requirements.txt):
   ```
   psycopg2-binary==2.9.9
   ```

2. **Set Up Supabase** (see SUPABASE_SETUP.md):
   - Create Supabase account
   - Create new project
   - Get connection string

3. **Set Environment Variable**:
   ```env
   DATABASE_URL=postgresql://postgres.xxx:password@host:6543/postgres
   SECRET_KEY=your-random-secret-key
   ```

4. **Deploy**: App automatically uses PostgreSQL when DATABASE_URL is set

### Complete Guide:
See `SUPABASE_SETUP.md` for step-by-step instructions

## ✅ Summary

### You DON'T Need To:
- ❌ Upload database to GitHub
- ❌ Configure database manually for local development
- ❌ Install database server for local development
- ❌ Set up database credentials for local development

### It Automatically:
- ✅ Creates database on first run (SQLite locally)
- ✅ Creates all tables
- ✅ Seeds demo data
- ✅ Switches to PostgreSQL when DATABASE_URL is set
- ✅ Works on any platform

### Your Database is:
- ✅ Already configured for both SQLite and PostgreSQL
- ✅ Already working locally
- ✅ Ready for production with Supabase
- ✅ Production-ready

### For Production:
- 📖 Follow `SUPABASE_SETUP.md` to set up PostgreSQL
- 🔑 Set `DATABASE_URL` and `SECRET_KEY` environment variables
- 🚀 Deploy and app automatically uses PostgreSQL

## 🎉 You're All Set!

The database is fully configured and will work automatically when you deploy. Just push to GitHub and deploy to your hosting platform!

---

**Need Help?**
- See: `DATABASE_INFO.md` for detailed SQLite information
- See: `SUPABASE_SETUP.md` for PostgreSQL setup guide
- See: `.env.example` for environment variable template
- WhatsApp: +1 (478) 233-8453
- Email: tickethublive@gmail.com

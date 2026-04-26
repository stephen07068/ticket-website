# 🚀 Supabase PostgreSQL Setup Guide

## Overview

Your TicketHubLive app is now configured to work with both:
- **SQLite** (local development - automatic, no setup needed)
- **PostgreSQL via Supabase** (production - follow steps below)

The app automatically detects which database to use based on the `DATABASE_URL` environment variable.

---

## 📋 Prerequisites

1. A Supabase account (free tier available)
2. Your app code with updated `app.py` and `requirements.txt`

---

## 🔧 Step 1: Create Supabase Project

### 1.1 Sign Up / Log In
- Go to [https://supabase.com](https://supabase.com)
- Sign up or log in with GitHub/Google

### 1.2 Create New Project
1. Click "New Project"
2. Fill in:
   - **Name**: `tickethublive` (or any name you prefer)
   - **Database Password**: Create a strong password (SAVE THIS!)
   - **Region**: Choose closest to your users (e.g., US East, EU West)
   - **Pricing Plan**: Free tier is fine to start
3. Click "Create new project"
4. Wait 2-3 minutes for setup to complete

---

## 🔗 Step 2: Get Database Connection String

### 2.1 Find Connection String
1. In your Supabase project dashboard, click "Project Settings" (gear icon)
2. Go to "Database" section
3. Scroll down to "Connection string"
4. Select "URI" tab
5. Copy the connection string that looks like:
   ```
   postgresql://postgres.xxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

### 2.2 Replace Password
- Replace `[YOUR-PASSWORD]` with the database password you created in Step 1.2
- Example:
  ```
  postgresql://postgres.abcdefghijk:MySecurePass123@aws-0-us-east-1.pooler.supabase.com:6543/postgres
  ```

---

## 🌐 Step 3: Configure Your App

### Option A: Local Development with Supabase

1. Create a `.env` file in your project root:
   ```bash
   # Windows
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
   ```

2. Edit `.env` and add your connection string:
   ```env
   DATABASE_URL=postgresql://postgres.xxxxxxxxxxxxx:YourPassword@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   SECRET_KEY=your-random-secret-key-here
   ```

3. Install python-dotenv to load .env file:
   ```bash
   pip install python-dotenv
   ```

4. Update `app.py` to load .env (add at the top):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

5. Run your app:
   ```bash
   python app.py
   ```

### Option B: Production Deployment (Render/Railway/Heroku)

1. Go to your hosting platform's dashboard
2. Find "Environment Variables" or "Config Vars" section
3. Add these variables:
   ```
   DATABASE_URL = postgresql://postgres.xxxxxxxxxxxxx:YourPassword@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   SECRET_KEY = your-random-secret-key-here
   ```
4. Deploy your app

---

## ✅ Step 4: Verify Connection

### 4.1 Check Tables Created
1. In Supabase dashboard, go to "Table Editor"
2. After running your app once, you should see these tables:
   - `events`
   - `ticket_tiers`
   - `orders`
   - `tickets`

### 4.2 Check Sample Data
1. Click on `events` table
2. You should see 6 sample events (Neon Horizon, Tech Summit, etc.)
3. If tables are empty, the app will seed data on first run

### 4.3 Test Your App
1. Open your app in browser
2. Try creating a new event from admin panel
3. Check Supabase Table Editor to see the new event

---

## 🔄 How It Works

### Automatic Database Selection

Your `app.py` now has this logic:

```python
# Get database URL from environment variable or use SQLite as fallback
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///tickethub.db')

# Fix for Supabase/Heroku postgres URL format
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

**What this means:**
- ✅ If `DATABASE_URL` environment variable exists → Use PostgreSQL (Supabase)
- ✅ If `DATABASE_URL` is not set → Use SQLite (local file)
- ✅ Automatically fixes Supabase URL format (postgres:// → postgresql://)

---

## 🗄️ Database Management

### View Data in Supabase

1. **Table Editor**: Visual interface to browse/edit data
2. **SQL Editor**: Run custom SQL queries
3. **Database**: View connection info, backups, extensions

### Backup Your Data

**Automatic Backups (Paid Plans):**
- Supabase Pro plan includes daily backups

**Manual Backup:**
1. Go to "Database" → "Backups"
2. Click "Create backup"
3. Download backup file

**Export via SQL:**
```sql
-- In Supabase SQL Editor
COPY events TO '/tmp/events.csv' CSV HEADER;
COPY orders TO '/tmp/orders.csv' CSV HEADER;
```

### Reset Database

**Option 1: Drop and Recreate Tables (via SQL Editor)**
```sql
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS ticket_tiers CASCADE;
DROP TABLE IF EXISTS events CASCADE;
```
Then restart your app to recreate tables.

**Option 2: Create New Project**
- Create a new Supabase project
- Update DATABASE_URL with new connection string

---

## 🔐 Security Best Practices

### 1. Never Commit Secrets
```bash
# Add to .gitignore (already done)
.env
*.db
```

### 2. Use Strong Passwords
- Database password: 16+ characters, mixed case, numbers, symbols
- SECRET_KEY: Generate random string (32+ characters)

### 3. Enable Row Level Security (RLS)
In Supabase dashboard:
1. Go to "Authentication" → "Policies"
2. Enable RLS for sensitive tables
3. Create policies for admin access

### 4. Use Connection Pooling
Your app already uses Supabase's connection pooler (port 6543):
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

---

## 🐛 Troubleshooting

### Issue 1: "Could not connect to database"

**Solution:**
- Check DATABASE_URL is correct
- Verify password has no special characters that need URL encoding
- Test connection in Supabase SQL Editor first

### Issue 2: "relation 'events' does not exist"

**Solution:**
```bash
# Delete local SQLite database if it exists
rm tickethub.db  # or del tickethub.db on Windows

# Restart app to create tables in PostgreSQL
python app.py
```

### Issue 3: "SSL connection required"

**Solution:**
Add `?sslmode=require` to your DATABASE_URL:
```
postgresql://...@...supabase.com:6543/postgres?sslmode=require
```

### Issue 4: "Too many connections"

**Solution:**
- Free tier has 60 connection limit
- Use connection pooler URL (port 6543, not 5432)
- Add connection pool settings (already in app.py)

### Issue 5: Password has special characters

**Solution:**
URL-encode special characters in password:
- `@` → `%40`
- `#` → `%23`
- `$` → `%24`
- `&` → `%26`

Example:
```
# Original password: MyPass@123#
# Encoded: MyPass%40123%23
postgresql://postgres.xxx:MyPass%40123%23@...
```

---

## 📊 Monitoring & Performance

### View Database Stats
1. Supabase Dashboard → "Database"
2. Check:
   - Connection count
   - Database size
   - Query performance

### Optimize Queries
```sql
-- Add indexes for better performance
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_email ON orders(email);
CREATE INDEX idx_tickets_order_id ON tickets(order_id);
```

### Monitor Logs
1. Supabase Dashboard → "Logs"
2. View:
   - Database logs
   - API logs
   - Error logs

---

## 💰 Pricing & Limits

### Free Tier Includes:
- ✅ 500 MB database space
- ✅ 2 GB bandwidth
- ✅ 50,000 monthly active users
- ✅ 60 concurrent connections
- ✅ 7 days of log retention

### When to Upgrade:
- More than 500 MB data (upgrade to Pro: $25/month)
- Need daily backups
- Need more than 60 concurrent connections
- Need point-in-time recovery

---

## 🔄 Switching Between SQLite and PostgreSQL

### Use SQLite (Local Development)
```bash
# Remove or comment out DATABASE_URL in .env
# DATABASE_URL=...

python app.py
```

### Use PostgreSQL (Production)
```bash
# Set DATABASE_URL in .env or environment variables
DATABASE_URL=postgresql://...

python app.py
```

### Migrate Data from SQLite to PostgreSQL

**Option 1: Let app reseed**
1. Switch to PostgreSQL
2. Run app (will create tables and seed sample data)
3. Manually recreate any custom events via admin panel

**Option 2: Export/Import**
```bash
# Export from SQLite
sqlite3 tickethub.db .dump > backup.sql

# Import to PostgreSQL (requires conversion)
# Use online tools or pgloader
```

---

## ✅ Checklist

- [ ] Created Supabase account
- [ ] Created new project
- [ ] Copied database connection string
- [ ] Replaced password in connection string
- [ ] Added DATABASE_URL to .env or hosting platform
- [ ] Added SECRET_KEY to .env or hosting platform
- [ ] Installed psycopg2-binary (`pip install -r requirements.txt`)
- [ ] Ran app and verified tables created
- [ ] Tested creating event from admin panel
- [ ] Verified data appears in Supabase Table Editor
- [ ] Added .env to .gitignore

---

## 📞 Support

**Supabase Help:**
- Documentation: https://supabase.com/docs
- Discord: https://discord.supabase.com
- GitHub: https://github.com/supabase/supabase

**TicketHubLive Help:**
- WhatsApp: +1 (478) 233-8453
- Email: tickethublive@gmail.com

---

## 🎉 You're All Set!

Your app now supports both local SQLite development and production PostgreSQL via Supabase. The database automatically switches based on your environment configuration.

**Next Steps:**
1. Test locally with Supabase
2. Deploy to production (Render/Railway/Heroku)
3. Monitor database usage in Supabase dashboard
4. Set up regular backups (Pro plan)

Happy coding! 🚀

# 🗄️ Database Information - TicketHubLive

## Current Setup

### Database Type: SQLite
- **File**: `tickethub.db`
- **Location**: Root directory (auto-created on first run)
- **Type**: File-based database (no server needed)

## ✅ What's Already Configured

### 1. Database is Auto-Created
When you run `python app.py` for the first time:
- ✅ Database file is created automatically
- ✅ All tables are created (Events, TicketTiers, Orders, Tickets)
- ✅ Sample data is seeded (6 demo events)

### 2. Database is in .gitignore
The `tickethub.db` file is excluded from Git because:
- ✅ Each environment should have its own database
- ✅ Prevents conflicts between local and production data
- ✅ Security (doesn't expose customer data)

### 3. Database Schema

```sql
-- Events Table
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT,
    description TEXT,
    date TEXT,
    time TEXT,
    venue TEXT,
    image_url TEXT,
    created_at TIMESTAMP
);

-- Ticket Tiers Table
CREATE TABLE ticket_tiers (
    id INTEGER PRIMARY KEY,
    event_id INTEGER,
    name TEXT,
    price REAL,
    quantity INTEGER,
    available INTEGER,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Orders Table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    event_id INTEGER,
    tier_id INTEGER,
    quantity INTEGER,
    email TEXT,
    name TEXT,
    payment_method TEXT,
    crypto_currency TEXT,
    subtotal REAL,
    service_fee REAL,
    processing_fee REAL,
    total REAL,
    status TEXT,
    tx_reference TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (tier_id) REFERENCES ticket_tiers(id)
);

-- Tickets Table
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    seat_number TEXT,
    ticket_code TEXT UNIQUE,
    qr_data TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

## 🚀 For Production Deployment

### Option 1: Keep SQLite (Simple - Good for Small Scale)

**Pros:**
- ✅ No setup needed
- ✅ Works on all hosting platforms
- ✅ Perfect for up to 10,000 orders
- ✅ Zero cost

**Cons:**
- ⚠️ Not ideal for high traffic (100+ concurrent users)
- ⚠️ File-based (can be slower for large datasets)

**How it works on hosting:**
- Database file is created automatically on the server
- Data persists between deployments (on most platforms)
- Render.com, Railway, PythonAnywhere all support SQLite

### Option 2: Upgrade to PostgreSQL (Recommended for Production)

**When to upgrade:**
- More than 1,000 orders per month
- Multiple admins accessing simultaneously
- Need better performance and reliability

**How to upgrade:**

#### Step 1: Update requirements.txt
Add this line:
```
psycopg2-binary==2.9.9
```

#### Step 2: Update app.py
Replace this line:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickethub.db'
```

With:
```python
import os
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///tickethub.db')
# Fix for Heroku/Render postgres URL
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

#### Step 3: Add PostgreSQL on your hosting platform

**Render.com:**
1. Create PostgreSQL database (free tier available)
2. Copy the "Internal Database URL"
3. Add as environment variable: `DATABASE_URL`

**Railway.app:**
1. Click "New" → "Database" → "PostgreSQL"
2. Automatically connects to your app

**Heroku:**
1. Add Heroku Postgres addon
2. Automatically sets DATABASE_URL

## 📊 Database Management

### View Database Contents (Local)

**Option 1: DB Browser for SQLite (GUI)**
1. Download: https://sqlitebrowser.org/
2. Open `tickethub.db`
3. Browse tables visually

**Option 2: Python Script**
```python
import sqlite3
conn = sqlite3.connect('tickethub.db')
cursor = conn.cursor()

# View all events
cursor.execute("SELECT * FROM events")
print(cursor.fetchall())

# View all orders
cursor.execute("SELECT * FROM orders")
print(cursor.fetchall())

conn.close()
```

**Option 3: Command Line**
```bash
sqlite3 tickethub.db
.tables
SELECT * FROM events;
SELECT * FROM orders;
.quit
```

### Backup Database

**Local Backup:**
```bash
# Windows
copy tickethub.db tickethub_backup.db

# Mac/Linux
cp tickethub.db tickethub_backup.db
```

**Production Backup (Render.com with PostgreSQL):**
```bash
# Download backup from Render dashboard
# Or use pg_dump command
```

### Reset Database

**Delete and recreate:**
```bash
# Windows
del tickethub.db
python app.py

# Mac/Linux
rm tickethub.db
python app.py
```

## 🔄 Database Migrations

Currently, the app uses simple auto-creation. For production, consider:

### Add Flask-Migrate (Optional)

**Install:**
```bash
pip install Flask-Migrate
```

**Update app.py:**
```python
from flask_migrate import Migrate

migrate = Migrate(app, db)
```

**Use migrations:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 📈 Database Scaling

### Current Capacity (SQLite)
- ✅ Up to 10,000 orders: Excellent
- ⚠️ 10,000 - 50,000 orders: Good
- ❌ 50,000+ orders: Upgrade to PostgreSQL

### Performance Tips
1. **Add indexes** (for large datasets):
```python
# In models.py, add to Order model:
__table_args__ = (
    db.Index('idx_order_status', 'status'),
    db.Index('idx_order_email', 'email'),
)
```

2. **Regular cleanup**:
```python
# Delete old rejected orders (optional)
Order.query.filter_by(status='rejected').filter(
    Order.created_at < datetime.now() - timedelta(days=30)
).delete()
```

## 🔐 Database Security

### Current Security Measures
- ✅ SQLAlchemy ORM (prevents SQL injection)
- ✅ Database file excluded from Git
- ✅ No direct SQL queries in code

### Production Security
1. **Use environment variables** for database URL
2. **Enable SSL** for PostgreSQL connections
3. **Regular backups** (daily recommended)
4. **Restrict database access** (firewall rules)

## 🆘 Common Database Issues

### Issue 1: "Database is locked"
**Solution:**
```python
# Add to app.py
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

### Issue 2: "Table doesn't exist"
**Solution:**
```bash
# Delete and recreate database
rm tickethub.db  # or del tickethub.db on Windows
python app.py
```

### Issue 3: "Database file not found on production"
**Solution:**
- Database is auto-created on first run
- Check file permissions on server
- Ensure writable directory

## 📝 Summary

### For Development (Current Setup)
- ✅ SQLite works perfectly
- ✅ No configuration needed
- ✅ Auto-creates on first run
- ✅ Already in .gitignore

### For Production (Small to Medium)
- ✅ Keep SQLite (easiest)
- ✅ Works on all platforms
- ✅ Good for up to 10,000 orders

### For Production (Large Scale)
- ⬆️ Upgrade to PostgreSQL
- ⬆️ Better performance
- ⬆️ Better for high traffic
- ⬆️ Easy to add on Render/Railway

## ✅ You're All Set!

The database is already configured and will work automatically when you deploy. No additional setup needed unless you want to upgrade to PostgreSQL later!

---

**Questions?**
- WhatsApp: +1 (478) 233-8453
- Email: tickethublive@gmail.com

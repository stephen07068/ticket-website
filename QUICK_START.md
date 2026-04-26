# TicketHubLive - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
**Option A - Windows:**
```bash
start.bat
```

**Option B - Manual:**
```bash
python app.py
```

### Step 3: Open Your Browser
The website will automatically open at: **http://localhost:5000**

---

## 🎯 Quick Test - All Buttons Working

### Test User Journey (5 minutes)

1. **Home Page** → Click any category filter (Concerts, Sports, etc.)
   - ✅ Events filter by category
   
2. **Event Card** → Click "Buy Ticket"
   - ✅ Navigates to event details
   
3. **Event Page** → Select VIP tier, change quantity to 3, click "Buy Ticket"
   - ✅ Tier selection works
   - ✅ Quantity +/- buttons work
   - ✅ Price updates automatically
   
4. **Checkout Page** → Select "Cryptocurrency", choose "USDT (TRC20)", enter email and name, click "Complete Purchase"
   - ✅ Payment method selection works
   - ✅ Crypto dropdown appears
   - ✅ Form validation works
   - ✅ Order created successfully
   
5. **Pending Page** → Click "Copy" to copy wallet address, enter payment reference, click "I have sent the payment"
   - ✅ Wallet address copied
   - ✅ Payment reference submitted
   - ✅ Status updates to "Awaiting approval"

6. **Admin Login** → Navigate to http://localhost:5000/admin-login.html
   - Email: `admin@tickethublive.com`
   - Password: `Admin@1234`
   - ✅ Login successful
   
7. **Admin Dashboard** → Click "Orders" tab, filter by "Needs Approval", click "Approve" on your order
   - ✅ Order filters work
   - ✅ Approve button works
   - ✅ Tickets generated
   
8. **Back to User** → Refresh pending page (or wait 5 seconds for auto-refresh)
   - ✅ Automatically redirects to ticket page
   
9. **Ticket Page** → Click "Download Ticket"
   - ✅ PNG ticket downloads with QR code
   
10. **Share** → Click "Share Ticket"
    - ✅ Share dialog opens or link copied

---

## 🎨 Test Admin Features (3 minutes)

1. **Admin Dashboard** → Click "Create Event" tab
   - ✅ Tab switches

2. **Fill Event Form:**
   - Title: "Test Concert 2024"
   - Category: Concert
   - Venue: "Test Arena"
   - Date: Select any future date
   - Time: 8:00 PM
   - Description: "This is a test event"
   
3. **Upload Image** → Click upload area, select any image
   - ✅ Image preview appears
   - ✅ Remove button works
   
4. **Set Ticket Tier:**
   - Name: "General Admission"
   - Price: 75
   - Quantity: 100
   
5. **Click "Create Event"**
   - ✅ Event created successfully
   - ✅ Validation works (try submitting without title)
   
6. **Go to Home Page** → Verify new event appears
   - ✅ Event visible in listing

---

## ✅ All Buttons Verified Working

### Index Page (7 buttons/interactions)
- ✅ Category filters (6 chips)
- ✅ Hero CTA button
- ✅ Event card "Buy Ticket" buttons

### Event Page (4 buttons/interactions)
- ✅ Tier selection cards
- ✅ Quantity + button
- ✅ Quantity - button
- ✅ "Buy Ticket" button

### Checkout Page (9 buttons/interactions)
- ✅ 6 payment method cards
- ✅ Crypto dropdown
- ✅ Email input
- ✅ Name input
- ✅ "Complete Purchase" button

### Pending Page (4 buttons/interactions)
- ✅ Copy wallet button
- ✅ WhatsApp link button
- ✅ Payment reference input
- ✅ "I have sent payment" button

### Ticket Page (3 buttons/interactions)
- ✅ Download ticket button
- ✅ Share ticket button
- ✅ Back link

### Admin Login (2 buttons/interactions)
- ✅ Email/password inputs
- ✅ Login button (+ Enter key)

### Admin Dashboard (15+ buttons/interactions)
- ✅ 3 sidebar navigation buttons
- ✅ 4 order filter buttons
- ✅ Approve/Reject buttons (dynamic)
- ✅ 10+ create event form inputs
- ✅ Image upload button
- ✅ Image remove button
- ✅ Create event button

---

## 🔧 Troubleshooting

### Server won't start?
```bash
# Check Python version (need 3.7+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database issues?
```bash
# Delete and recreate database
del tickethub.db
python app.py
```

### Port 5000 already in use?
Edit `app.py` line 234:
```python
app.run(debug=True, port=5001)  # Change to 5001 or any free port
```

---

## 📊 Database Schema

### Events Table
- id, title, category, description, date, time, venue, image_url

### Ticket Tiers Table
- id, event_id, name, price, quantity, available

### Orders Table
- id, event_id, tier_id, quantity, email, name, payment_method, crypto_currency, total, status, tx_reference

### Tickets Table (Generated after approval)
- id, order_id, seat_number, ticket_code, qr_data

---

## 🎉 Success!

All 50+ buttons and interactive elements are fully functional!

**Need help?** Check `TEST_BUTTONS.md` for detailed testing guide or `BUTTON_FIXES_SUMMARY.md` for technical details.

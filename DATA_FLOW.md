# 🔄 TicketHubLive - Data Flow & System Architecture

## System Overview

TicketHubLive is a full-stack ticket booking platform with:
- Frontend: HTML/CSS/JavaScript
- Backend: Python Flask REST API
- Database: SQLite (local) or PostgreSQL (production via Supabase)
- Payment: Cryptocurrency wallets + WhatsApp integration

---

## 🗄️ Database Architecture

### Database Selection (Automatic)
```
App Startup
    ↓
Check DATABASE_URL environment variable
    ↓
    ├─ If set → Use PostgreSQL (Supabase)
    └─ If not set → Use SQLite (local file)
```

### Tables & Relationships
```
events (1) ──→ (many) ticket_tiers
   ↓
   └──→ (many) orders
              ↓
              └──→ (many) tickets
```

### Schema Details

**events**
- id, title, category, description
- date, time, venue, image_url
- created_at

**ticket_tiers**
- id, event_id (FK), name
- price, quantity, available

**orders**
- id, event_id (FK), tier_id (FK)
- quantity, email, name
- payment_method, crypto_currency
- subtotal, service_fee, processing_fee, total
- status, tx_reference, created_at

**tickets**
- id, order_id (FK)
- seat_number, ticket_code (unique)
- qr_data, created_at

---

## 🔄 User Journey Flow

### 1. Browse Events (index.html)
```
User visits homepage
    ↓
GET /api/events
    ↓
Display event cards with images
    ↓
User clicks "Get Tickets"
```

### 2. View Event Details (event.html)
```
GET /api/events/:id
    ↓
Display event info + ticket tiers
    ↓
User selects tier & quantity
    ↓
Click "Proceed to Checkout"
```

### 3. Checkout (checkout.html)
```
User enters: name, email
User selects: payment method
    ↓
POST /api/checkout
    ↓
Creates order (status: pending_payment)
Reserves seats (tier.available -= quantity)
    ↓
Returns: order_id, payment instructions
    ↓
Redirect to pending.html
```

### 4. Payment Instructions (pending.html)
```
GET /api/orders/:id
    ↓
Display payment details:
  - Crypto: Show wallet address + QR code
  - Other: Show WhatsApp link
    ↓
User submits payment reference
    ↓
POST /api/payments/submit
    ↓
Updates order (status: payment_submitted)
    ↓
Shows "Awaiting admin approval" message
```

### 5. Admin Approval (admin.html)
```
Admin logs in
    ↓
POST /api/admin/login
    ↓
GET /api/admin/orders?status=payment_submitted
    ↓
Admin reviews payment proof
    ↓
POST /api/admin/approve
    ↓
Updates order (status: approved)
Generates tickets with QR codes
    ↓
User redirected to ticket-pending.html
```

### 6. Ticket Delivery (ticket-pending.html)
```
Shows "Your Ticket is On The Way!"
Timeline: Payment Received ✓ → Ticket Generation ⏳ → Delivery 📧
    ↓
After admin approval
    ↓
Redirect to ticket.html
```

### 7. View Ticket (ticket.html)
```
GET /api/tickets/:order_id
    ↓
Display ticket with:
  - Event details
  - Seat number
  - QR code
  - Event image
    ↓
User can download ticket (Canvas API)
  - Sports: Dark with trophy, sport-specific colors
  - Concert: Alternating designs (minimalist/colorful)
  - Other: Standard design with event image
```

---

## 🎨 Ticket Design System

### Design Selection Logic
```javascript
if (category === 'sports') {
    detectSportType(title)
    ↓
    Football → Black/Gold
    Basketball → Orange
    Baseball → Green
    Tennis → Blue
    Rugby → Maroon
    Hockey → Ice Blue
    Boxing → Red
    ↓
    drawSportsTicketNew()
} else if (category === 'concert') {
    if (ticketId % 2 === 0) {
        drawConcertColorful() // Purple-pink gradient
    } else {
        drawConcertMinimalist() // White with microphone
    }
} else {
    drawStandardTicketNew() // Festival, theater, conference
}
```

### Ticket Components
- Main ticket (750px) + Stub (150px) = 900px × 400px
- Event image as watermark background (15% opacity)
- Event title as large watermark text (8% opacity)
- QR code for verification
- Perforated edge between main and stub
- Sport/category-specific colors and icons

---

## 🔐 Admin Flow

### 1. Login (admin-login.html)
```
POST /api/admin/login
    ↓
Validates credentials
    ↓
Returns token
    ↓
Redirect to admin.html
```

### 2. Create Event (admin.html)
```
User fills form:
  - Title, category, description
  - Date, time, venue
  - Upload image
  - Add ticket tiers
    ↓
POST /api/admin/upload (image)
    ↓
Returns image_url
    ↓
POST /api/admin/events
    ↓
Creates event + tiers
    ↓
Event appears on homepage
```

### 3. Manage Orders (admin.html)
```
GET /api/admin/orders
    ↓
Display orders by status:
  - pending_payment
  - payment_submitted
  - approved
  - rejected
    ↓
Admin actions:
  - Approve → POST /api/admin/approve
  - Reject → POST /api/admin/reject
```

### 4. Manage Events (admin.html)
```
GET /api/admin/events
    ↓
Display all events
    ↓
DELETE /api/admin/events/:id
    ↓
Removes event (if no orders exist)
```

---

## 💳 Payment Flow

### Cryptocurrency Payment
```
User selects crypto (USDT_TRC20, USDT_ERC20, etc.)
    ↓
System displays:
  - Wallet address
  - QR code (generated on-the-fly)
  - Amount to send
    ↓
User sends payment externally
    ↓
User submits transaction reference
    ↓
Admin verifies on blockchain
    ↓
Admin approves order
```

### Other Payment Methods (PayPal, Zelle, etc.)
```
User selects payment method
    ↓
System generates WhatsApp link with:
  - Order ID
  - Event name
  - Amount
    ↓
User contacts via WhatsApp
    ↓
Admin sends payment details
    ↓
User pays
    ↓
User submits payment reference
    ↓
Admin verifies
    ↓
Admin approves order
```

---

## 🎫 Ticket Generation

### Timing
- Tickets are NOT generated at checkout
- Tickets are ONLY generated after admin approval
- This matches Ticketmaster's delivery model

### Generation Process
```
Admin clicks "Approve"
    ↓
POST /api/admin/approve
    ↓
create_tickets_for_order(order)
    ↓
For each ticket:
  - Generate seat number (SEC X, ROW Y, SEAT Z)
  - Generate unique code (THL-XXXX-XXXXXX)
  - Generate QR code (verification URL)
  - Save to database
    ↓
Return ticket data
```

### QR Code Content
```
http://localhost:5000/api/verify?ticketId=THL-0001-ABC123
    ↓
GET /api/verify?ticketId=...
    ↓
Returns:
  - valid: true/false
  - ticketId, seat, name
  - event, date
```

---

## 📁 File Structure

### Frontend
```
index.html          → Homepage (event listing)
event.html          → Event details page
checkout.html       → Payment selection
pending.html        → Payment instructions
ticket-pending.html → Waiting for ticket delivery
ticket.html         → Ticket display & download
admin-login.html    → Admin authentication
admin.html          → Admin dashboard
```

### Backend
```
app.py              → Flask API (all endpoints)
models.py           → SQLAlchemy models
lib/api.js          → Frontend API helper
```

### Configuration
```
requirements.txt    → Python dependencies
.env.example        → Environment variable template
.gitignore          → Git exclusions
Procfile            → Heroku deployment config
runtime.txt         → Python version
```

### Documentation
```
README.md                    → Main documentation
QUICK_START.md               → Quick setup guide
DATA_FLOW.md                 → This file
DATABASE_INFO.md             → SQLite details
DATABASE_QUICK_REFERENCE.md  → Database quick guide
SUPABASE_SETUP.md            → PostgreSQL setup
DEPLOYMENT.md                → Deployment guide
GITHUB_DEPLOY_STEPS.md       → GitHub instructions
DEPLOYMENT_SUMMARY.md        → Deployment summary
BUG_FIXES.md                 → Bug documentation
TROUBLESHOOTING.md           → Common issues
```

---

## 🔄 API Endpoints

### Public Endpoints
```
GET  /api/events                    → List all events
GET  /api/events/:id                → Get event details
POST /api/checkout                  → Create order
POST /api/payments/submit           → Submit payment reference
GET  /api/orders/:id                → Get order status
GET  /api/tickets/:order_id         → Get tickets (if approved)
GET  /api/verify?ticketId=...       → Verify ticket
GET  /api/wallets                   → Get crypto wallets
GET  /api/whatsapp-link             → Get WhatsApp contact link
```

### Admin Endpoints
```
POST   /api/admin/login             → Admin authentication
GET    /api/admin/orders            → List all orders
POST   /api/admin/approve           → Approve order
POST   /api/admin/reject            → Reject order
POST   /api/admin/events            → Create event
GET    /api/admin/events            → List all events
DELETE /api/admin/events/:id        → Delete event
POST   /api/admin/upload            → Upload event image
```

---

## 🌐 Environment Configuration

### Local Development
```
No environment variables needed
Uses SQLite (tickethub.db)
Default admin credentials
Sample wallet addresses
```

### Production (Recommended)
```env
DATABASE_URL=postgresql://...       # Supabase connection string
SECRET_KEY=random-secret-key        # Flask session secret
ADMIN_EMAIL=admin@domain.com        # Optional
ADMIN_PASSWORD=SecurePass123        # Optional
WHATSAPP_NUMBER=14782338453         # Optional
```

---

## 🔒 Security Features

### Input Validation
- Email format validation
- Required field checks
- Quantity limits
- Seat availability checks

### SQL Injection Prevention
- SQLAlchemy ORM (parameterized queries)
- No raw SQL in code

### Authentication
- Admin login required for sensitive operations
- Token-based session (demo implementation)

### Data Protection
- Database excluded from Git
- Environment variables for secrets
- .env files in .gitignore

---

## 📊 Order Status Flow

```
pending_payment
    ↓
payment_submitted
    ↓
    ├─→ approved → tickets generated
    └─→ rejected → seats restored
```

### Status Meanings
- **pending_payment**: Order created, awaiting payment
- **payment_submitted**: User submitted payment reference
- **approved**: Admin verified payment, tickets generated
- **rejected**: Payment invalid, order cancelled

---

## 🎯 Key Features

### Ticketmaster-Style Delivery
- ✅ Tickets not generated immediately
- ✅ User chooses delivery method (Email/WhatsApp)
- ✅ "Your ticket is on the way" message
- ✅ Timeline showing progress
- ✅ Tickets delivered after approval

### Dynamic Ticket Designs
- ✅ Sports tickets: Dark with trophy, sport-specific colors
- ✅ Concert tickets: Two alternating designs
- ✅ Event images as watermarks
- ✅ Event titles as large background text
- ✅ QR codes for verification

### Admin Dashboard
- ✅ Create events with image upload
- ✅ Manage ticket tiers
- ✅ Approve/reject orders
- ✅ View all orders by status
- ✅ Delete events (if no orders)

### Payment Flexibility
- ✅ 6 cryptocurrency options
- ✅ PayPal, Zelle, CashApp, Venmo
- ✅ WhatsApp integration
- ✅ QR codes for crypto wallets

---

## 🚀 Deployment Flow

```
Local Development
    ↓
Git commit
    ↓
Push to GitHub
    ↓
Connect to hosting platform
    ↓
Set environment variables
    ↓
Deploy
    ↓
Database auto-creates
    ↓
Sample data seeded
    ↓
Live! 🎉
```

---

## 📞 Support

- **WhatsApp**: +1 (478) 233-8453
- **Email**: tickethublive@gmail.com

---

**System Status**: ✅ Production Ready
**Last Updated**: Database configuration with Supabase PostgreSQL support

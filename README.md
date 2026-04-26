# 🎫 TicketHubLive - Complete Event Ticketing Platform

A full-stack event ticketing platform with cryptocurrency payment support, admin dashboard, and automated ticket generation.

## ✨ Features

### For Customers
- 🎭 Browse events by category (Concerts, Sports, Theater, Festivals)
- 🎟️ Select ticket tiers (VIP, Regular, etc.)
- 💳 Multiple payment methods (Crypto, PayPal, WhatsApp Pay, CashApp, Zelle, Gift Cards)
- 📱 Instant ticket delivery with QR codes
- 📥 Download tickets as PNG images
- 🔗 Share tickets via Web Share API

### For Admins
- 🔐 Secure admin portal with authentication
- 📊 Dashboard with order statistics
- ✅ Approve/reject payment submissions
- 🎨 Create events with custom banner images
- 💰 Manage ticket tiers and pricing
- 📋 Filter and search orders by status

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**
   
   **Windows:**
   ```bash
   start.bat
   ```
   
   **Mac/Linux:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   - Website: http://localhost:5000
   - Admin Portal: http://localhost:5000/admin-login.html

## 🔑 Admin Credentials

- **Email:** admin@tickethublive.com
- **Password:** Admin@1234

## 📁 Project Structure

```
tickethublive/
├── index.html              # Home page with event listings
├── event.html              # Event details and ticket selection
├── checkout.html           # Payment method selection
├── pending.html            # Payment instructions
├── ticket.html             # Confirmed ticket display
├── admin-login.html        # Admin authentication
├── admin.html              # Admin dashboard
├── lib/
│   └── api.js             # API communication layer
├── app.py                  # Flask backend server
├── models.py               # Database models
├── requirements.txt        # Python dependencies
├── start.bat               # Windows startup script
├── tickethub.db           # SQLite database (auto-created)
└── unnamed (20-26).png    # Sample event images
```

## 🎯 User Flow

1. **Browse Events** → Filter by category
2. **Select Event** → Choose ticket tier and quantity
3. **Checkout** → Select payment method and enter details
4. **Payment** → Follow instructions (crypto wallet or WhatsApp)
5. **Submit Proof** → Enter transaction reference
6. **Wait for Approval** → Admin reviews and approves
7. **Get Ticket** → Download PNG ticket with QR code

## 🛠️ Admin Flow

1. **Login** → Use admin credentials
2. **View Dashboard** → See order statistics
3. **Manage Orders** → Filter by status (Pending, Submitted, Approved)
4. **Approve/Reject** → Review payment submissions
5. **Create Events** → Add new events with images and tiers

## 💻 Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Canvas API for ticket generation
- Web Share API for sharing
- LocalStorage for checkout data
- Responsive design

### Backend
- Python 3.x
- Flask (Web framework)
- Flask-SQLAlchemy (ORM)
- Flask-CORS (Cross-origin support)
- SQLite (Database)
- qrcode + Pillow (QR code generation)

## 🔌 API Endpoints

### Public Endpoints
- `GET /api/events` - List all events
- `GET /api/events/:id` - Get event details
- `POST /api/checkout` - Create order
- `GET /api/wallets` - Get crypto wallet addresses
- `GET /api/whatsapp-link` - Get WhatsApp payment link
- `POST /api/payments/submit` - Submit payment reference
- `GET /api/orders/:id` - Get order details
- `GET /api/tickets/:id` - Get ticket details
- `GET /api/verify` - Verify ticket code

### Admin Endpoints
- `POST /api/admin/login` - Admin authentication
- `POST /api/admin/events` - Create new event
- `POST /api/admin/upload` - Upload event banner
- `GET /api/admin/orders` - List all orders
- `POST /api/admin/approve` - Approve order
- `POST /api/admin/reject` - Reject order

## 🗄️ Database Schema

### Events
- id, title, category, description, date, time, venue, image_url, created_at

### Ticket Tiers
- id, event_id, name, price, quantity, available

### Orders
- id, event_id, tier_id, quantity, email, name, payment_method, crypto_currency, subtotal, service_fee, processing_fee, total, status, tx_reference, created_at

### Tickets
- id, order_id, seat_number, ticket_code, qr_data, created_at

## 📊 Order Status Flow

1. **pending_payment** - Order created, awaiting payment
2. **payment_submitted** - Customer submitted payment proof
3. **approved** - Admin approved, tickets generated ✅
4. **rejected** - Admin rejected, seats restored ❌

## 🎨 Payment Methods

### Cryptocurrency
- USDT (TRC20, ERC20, BEP20)
- Bitcoin (BTC)
- Ethereum (ETH)

### Other Methods (via WhatsApp)
- PayPal
- WhatsApp Pay
- CashApp
- Zelle
- Gift Cards

## 🔒 Security Features

- Admin authentication required
- Session-based admin access
- Input validation on all forms
- SQL injection protection (SQLAlchemy ORM)
- CORS configuration
- Secure password handling

## 🎨 Customization

### Update Crypto Wallets
Edit `app.py` lines 18-24:
```python
WALLETS = {
    "USDT_TRC20": "YOUR_WALLET_ADDRESS",
    "USDT_ERC20": "YOUR_WALLET_ADDRESS",
    # ... etc
}
```

### Update WhatsApp Number
Edit `app.py` line 25:
```python
WHATSAPP_NUMBER = "YOUR_WHATSAPP_NUMBER"
```

### Update Admin Credentials
Edit `app.py` lines 26-27:
```python
ADMIN_EMAIL = 'your@email.com'
ADMIN_PASSWORD = 'YourPassword123'
```

### Add Sample Events
Events are auto-seeded on first run. Edit `seed_data()` function in `app.py` to customize.

## 📝 Testing

See `TEST_BUTTONS.md` for comprehensive testing guide covering all 50+ interactive elements.

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py (last line)
app.run(debug=True, port=5001)
```

### Database Issues
```bash
# Delete and recreate
rm tickethub.db  # or del tickethub.db on Windows
python app.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### QR Codes Not Generating
```bash
pip install qrcode[pil] Pillow
```

## 📚 Documentation

- `QUICK_START.md` - Fast setup guide
- `TEST_BUTTONS.md` - Complete testing checklist
- `BUTTON_FIXES_SUMMARY.md` - Technical implementation details

## ✅ All Features Working

- ✅ Event browsing and filtering
- ✅ Ticket selection and quantity adjustment
- ✅ Multiple payment methods
- ✅ Order creation and tracking
- ✅ Payment submission
- ✅ Admin approval workflow
- ✅ Ticket generation with QR codes
- ✅ Ticket download as PNG
- ✅ Ticket sharing
- ✅ Admin dashboard
- ✅ Event creation with image upload
- ✅ Order management and filtering

## 🎉 Success!

All 50+ buttons and interactive elements are fully functional and tested!

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues or questions, check the documentation files or review the code comments.

---

**Built with ❤️ using Flask, SQLAlchemy, and Vanilla JavaScript**

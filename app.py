from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import text
from models import db, Event, TicketTier, Order, Ticket
import uuid, datetime, os, io, base64, urllib.parse
import sys

# Enable logging
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False
    logger.warning("QR code library not available")

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# ── DATABASE CONFIG (Supabase PostgreSQL Support) ─────────────────────────────
# Get database URL from environment variable (for Supabase) or use SQLite as fallback
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: Use PostgreSQL
    logger.info("Using PostgreSQL database")
    # Fix for Supabase/Heroku postgres URL format
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        logger.info("Fixed postgres:// to postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
else:
    # Local development: Use SQLite
    logger.info("Using SQLite database (local development)")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tickethub.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tickethub-secret-2024')
db.init_app(app)

# ── PAYMENT CONFIG ────────────────────────────────────────────────────────────
WALLETS = {
    "USDT_TRC20": "TQQheXpmZQYtrFPJ27Lqf2jazv1RDXCeTr",
    "USDT_ERC20": "0x30ed522d237e2f4a78b9b61b4a5464195d308685",
    "USDT_BEP20": "0x30ed522d237e2f4a78b9b61b4a5464195d308685",
    "ETH":        "0x30ed522d237e2f4a78b9b61b4a5464195d308685",
    "BTC":        "bc1py8rpkfjgjaj8n7kwjh6accghgh2u62z4stjgytmspw4q7z3lkczscgk7ds",
}
WHATSAPP_NUMBER = "14782338453"
ADMIN_EMAIL     = 'admin@tickethublive.com'
ADMIN_PASSWORD  = 'Admin@1234'

# ── HELPERS ───────────────────────────────────────────────────────────────────
def generate_qr_base64(data: str) -> str:
    if not QR_AVAILABLE:
        return ''
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ''

def create_tickets_for_order(order: Order) -> list:
    """Generate tickets only after admin approval. Called ONLY from admin_approve."""
    tier = TicketTier.query.get(order.tier_id) if order.tier_id else None
    tier_name = tier.name if tier else "GA"
    
    if '|' in tier_name:
        parts = tier_name.split('|')
        section = parts[0] if len(parts) > 0 and parts[0] else "GA"
        row = parts[1] if len(parts) > 1 and parts[1] else ""
        seats_str = parts[2] if len(parts) > 2 and parts[2] else ""
        
        start_seat = 1
        if '-' in seats_str:
            try:
                start_seat = int(seats_str.split('-')[0].strip())
            except:
                pass
        elif seats_str.isdigit():
            start_seat = int(seats_str)
            
        base_seat = f"SEC {section}"
        if row:
            base_seat += f", ROW {row}"
            
        results = []
        for i in range(order.quantity):
            seat = f"{base_seat}, SEAT {start_seat + i}"
            code = f"THL-{order.id:04d}-{uuid.uuid4().hex[:6].upper()}"
            verify = f"http://localhost:5000/api/verify?ticketId={code}"
            qr_data = generate_qr_base64(verify)
            ticket = Ticket(order_id=order.id, seat_number=seat, ticket_code=code, qr_data=qr_data)
            db.session.add(ticket)
            results.append({'seat': seat, 'code': code})
            
        return results

    if "SEC" in tier_name.upper() or "ROW" in tier_name.upper():
        base_seat = tier_name
    else:
        section = (order.id * 10) % 100 + 100
        row = chr(65 + (order.id % 26))
        base_seat = f"SEC {section}, ROW {row}"

    results = []
    for i in range(order.quantity):
        seat = f"{base_seat}, SEAT {i + 1}"
        code = f"THL-{order.id:04d}-{uuid.uuid4().hex[:6].upper()}"
        verify = f"http://localhost:5000/api/verify?ticketId={code}"
        qr_data = generate_qr_base64(verify)
        ticket = Ticket(order_id=order.id, seat_number=seat, ticket_code=code, qr_data=qr_data)
        db.session.add(ticket)
        results.append({'seat': seat, 'code': code})
    return results

def build_whatsapp_link(order: Order, event: Event) -> str:
    msg = (
        f"Hi, I want to pay for my ticket via {order.payment_method}.\n\n"
        f"Order ID: #{order.id}\n"
        f"Event: {event.title if event else 'N/A'}\n"
        f"Amount: ${order.total:.2f}\n\n"
        f"Please send me your payment details."
    )
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

# ── SEED ─────────────────────────────────────────────────────────────────────
def seed_data():
    if Event.query.count() > 0:
        return
    events = [
        {"title": "Neon Horizon World Tour",      "category": "Concert",    "description": "An electrifying world tour featuring chart-topping artists and stunning light shows.", "date": "Oct 24, 2024", "time": "8:00 PM",  "venue": "Starlight Arena, LA",           "image_url": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=800&q=80", "tiers": [{"name": "Floor Left", "price": 299.00, "qty": 10}, {"name": "Section 101", "price": 250.00, "qty": 14}, {"name": "Section 102", "price": 129.00, "qty": 8}]},
        {"title": "Neon Dreams World Tour 2024",  "category": "Concert",    "description": "Experience the magic of Neon Dreams live on stage with a full orchestra.",              "date": "Nov 15, 2024", "time": "7:30 PM",  "venue": "Madison Square Garden, NY",      "image_url": "https://images.unsplash.com/photo-1540039155732-68ee23e15b51?auto=format&fit=crop&w=800&q=80", "tiers": [{"name": "Section 103", "price": 299.00, "qty": 6}, {"name": "Section 104", "price": 99.00,  "qty": 20}]},
        {"title": "Summer Solstice Music Festival","category": "Festival",   "description": "A three-day outdoor music festival celebrating the longest day of the year.",          "date": "Jun 21, 2025", "time": "12:00 PM", "venue": "Golden Gate Park, SF",           "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80", "tiers": [{"name": "Floor Right", "price": 150.00, "qty": 1000},{"name": "General Admission", "price": 60.00, "qty": 3000}]},
        {"title": "Tech Summit 2024",             "category": "Conference", "description": "The premier technology conference bringing together the brightest minds in tech.",       "date": "Dec 5, 2024",  "time": "9:00 AM",  "venue": "Moscone Center, SF",             "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80", "tiers": [{"name": "Section 101",  "price": 500.00, "qty": 20},  {"name": "Section 102",    "price": 199.00, "qty": 800}]},
        {"title": "Championship Finals 2024",     "category": "Sports",     "description": "Watch the ultimate showdown between the top teams of the season.",                      "date": "Dec 18, 2024", "time": "6:00 PM",  "venue": "SoFi Stadium, LA",               "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80", "tiers": [{"name": "Floor Left",     "price": 350.00, "qty": 50},  {"name": "Section 104",       "price": 75.00,  "qty": 2000}]},
        {"title": "Broadway Night: Hamilton",     "category": "Theater",    "description": "The award-winning Broadway musical Hamilton returns for a limited run.",                "date": "Jan 10, 2025", "time": "8:00 PM",  "venue": "Richard Rodgers Theatre, NY",    "image_url": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=800&q=80", "tiers": [{"name": "Floor Right",     "price": 249.00, "qty": 200}, {"name": "Section 103",        "price": 149.00, "qty": 300}]},
    ]
    for e in events:
        ev = Event(title=e['title'], category=e['category'], description=e['description'],
                   date=e['date'], time=e['time'], venue=e['venue'], image_url=e['image_url'])
        db.session.add(ev)
        db.session.flush()
        for t in e['tiers']:
            db.session.add(TicketTier(event_id=ev.id, name=t['name'],
                                      price=t['price'], quantity=t['qty'], available=t['qty']))
    db.session.commit()
    print("[OK] Sample data seeded.")

# ── STATIC ────────────────────────────────────────────────────────────────────
@app.route('/')
def serve_index():
    return send_from_directory(basedir, 'index.html')

# ── CLEAN URL SHORTCUTS (no .html needed) ─────────────────────────────────────
@app.route('/admin')
def serve_admin_login():
    return send_from_directory(basedir, 'admin-login.html')

@app.route('/admin/dashboard')
def serve_admin_dashboard():
    return send_from_directory(basedir, 'admin.html')

@app.route('/events')
def serve_events():
    return send_from_directory(basedir, 'index.html')

@app.route('/event')
def serve_event():
    return send_from_directory(basedir, 'event.html')

@app.route('/checkout')
def serve_checkout():
    return send_from_directory(basedir, 'checkout.html')

@app.route('/pending')
def serve_pending():
    return send_from_directory(basedir, 'pending.html')

@app.route('/ticket')
def serve_ticket():
    return send_from_directory(basedir, 'ticket.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if filename.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    try:
        return send_from_directory(basedir, filename)
    except Exception:
        return send_from_directory(basedir, 'index.html')

# ── EVENTS ────────────────────────────────────────────────────────────────────
@app.route('/api/events', methods=['GET'])
def get_events():
    category = request.args.get('category', '')
    q        = request.args.get('q', '')
    query    = Event.query
    if category: query = query.filter(Event.category.ilike(f'%{category}%'))
    if q:        query = query.filter(Event.title.ilike(f'%{q}%'))
    return jsonify([e.to_dict() for e in query.all()])

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    return jsonify(Event.query.get_or_404(event_id).to_dict(include_tiers=True))

@app.route('/api/admin/events', methods=['POST'])
def create_event():
    data = request.get_json()
    if not data: return jsonify({'error': 'No data'}), 400
    ev = Event(title=data.get('title',''), category=data.get('category','Concert'),
               description=data.get('description',''), date=data.get('date',''),
               time=data.get('time',''), venue=data.get('venue',''), image_url=data.get('image_url',''))
    db.session.add(ev); db.session.flush()
    for t in data.get('tiers', []):
        db.session.add(TicketTier(event_id=ev.id, name=t.get('name',''),
            price=float(t.get('price',0)), quantity=int(t.get('quantity',0)),
            available=int(t.get('quantity',0)), view_image=t.get('view_image','')))
    db.session.commit()
    return jsonify({'message': 'Event created', 'event_id': ev.id}), 201

@app.route('/api/admin/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    if 'image_url' in data:
        event.image_url = data['image_url']
    if 'title' in data:
        event.title = data['title']
    if 'venue' in data:
        event.venue = data['venue']
    if 'date' in data:
        event.date = data['date']
    if 'time' in data:
        event.time = data['time']
    if 'description' in data:
        event.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Event updated', 'event_id': event.id})

# ── IMAGE UPLOAD ──────────────────────────────────────────────────────────────
@app.route('/api/admin/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    # Sanitize filename and save
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        return jsonify({'error': 'Invalid file type'}), 400
    filename = f"event_{uuid.uuid4().hex[:8]}{ext}"
    filepath = os.path.join(basedir, filename)
    file.save(filepath)
    return jsonify({'image_url': filename, 'message': 'Image uploaded successfully'}), 201

# ── WALLETS & WHATSAPP ────────────────────────────────────────────────────────
@app.route('/api/wallets', methods=['GET'])
def get_wallets():
    return jsonify(WALLETS)

@app.route('/api/whatsapp-link', methods=['GET'])
def get_whatsapp_link():
    order_id = request.args.get('order_id','')
    method   = request.args.get('method', 'PayPal')
    order    = Order.query.get(order_id) if order_id else None
    event    = Event.query.get(order.event_id) if order else None
    if order:
        link = build_whatsapp_link(order, event)
    else:
        msg  = f"Hi, I'd like to pay via {method}. Please send payment details."
        link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
    return jsonify({'link': link, 'whatsapp_number': WHATSAPP_NUMBER})

# ── CHECKOUT (creates order only — NO ticket yet) ─────────────────────────────
@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    if not data: return jsonify({'error': 'No data'}), 400

    event_id        = data.get('event_id')
    tier_id         = data.get('tier_id')
    quantity        = int(data.get('quantity', 1))
    email           = data.get('email', '').strip()
    name            = data.get('name', '').strip()
    payment_method  = data.get('payment_method', 'cryptocurrency')
    crypto_currency = data.get('crypto_currency', 'USDT_TRC20')

    if not email or not name:
        return jsonify({'error': 'Email and name are required'}), 400

    event = Event.query.get(event_id)
    if not event: return jsonify({'error': 'Event not found'}), 404

    tier = TicketTier.query.get(tier_id)
    if not tier or tier.event_id != event_id:
        return jsonify({'error': 'Invalid ticket tier'}), 400

    if tier.available < quantity:
        return jsonify({'error': f'Only {tier.available} seats left'}), 400

    tier.available -= quantity  # Reserve seats

    service_fee    = round(quantity * 12.25, 2)
    processing_fee = round(quantity * 2.75, 2)
    subtotal       = round(tier.price * quantity, 2)
    total          = round(subtotal + service_fee + processing_fee, 2)

    order = Order(
        event_id=event_id, tier_id=tier_id, quantity=quantity,
        email=email, name=name, payment_method=payment_method,
        crypto_currency=crypto_currency, subtotal=subtotal,
        service_fee=service_fee, processing_fee=processing_fee,
        total=total, status='pending_payment'   # ← NO ticket created here
    )
    db.session.add(order)
    db.session.commit()

    # Build payment instructions for frontend
    if payment_method == 'cryptocurrency':
        wallet = WALLETS.get(crypto_currency, WALLETS['USDT_TRC20'])
        instructions = {'type': 'crypto', 'currency': crypto_currency,
                        'wallet': wallet, 'amount': total}
    else:
        instructions = {'type': 'whatsapp', 'method': payment_method,
                        'whatsapp_link': build_whatsapp_link(order, event),
                        'whatsapp_number': WHATSAPP_NUMBER}

    return jsonify({
        'order_id': order.id, 'status': 'pending_payment',
        'event': event.title, 'date': event.date, 'time': event.time,
        'venue': event.venue, 'total': total, 'quantity': quantity,
        'payment_instructions': instructions,
    }), 201

# ── PAYMENT SUBMISSION ────────────────────────────────────────────────────────
@app.route('/api/payments/submit', methods=['POST'])
def submit_payment():
    data = request.get_json()
    order = Order.query.get(data.get('order_id'))
    if not order: return jsonify({'error': 'Order not found'}), 404
    if order.status not in ('pending_payment', 'payment_submitted'):
        return jsonify({'error': 'Cannot update this order'}), 400
    order.status       = 'payment_submitted'
    order.tx_reference = data.get('tx_reference', '').strip()
    db.session.commit()
    return jsonify({'message': 'Payment reference submitted. Awaiting admin approval.',
                    'status': 'payment_submitted'})

# ── ORDERS ────────────────────────────────────────────────────────────────────
@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    event = Event.query.get(order.event_id)
    tier  = TicketTier.query.get(order.tier_id) if order.tier_id else None
    result = {
        'order_id': order.id, 'status': order.status,
        'event': event.title if event else '', 'date': event.date if event else '',
        'time': event.time if event else '', 'venue': event.venue if event else '',
        'tier': tier.name if tier else '', 'quantity': order.quantity,
        'total': order.total, 'payment_method': order.payment_method,
        'crypto_currency': order.crypto_currency,
        'email': order.email, 'name': order.name,
        'tx_reference': order.tx_reference,
        'created_at': order.created_at.isoformat() if order.created_at else '',
    }
    if order.status == 'approved':
        result['tickets'] = [t.to_dict() for t in Ticket.query.filter_by(order_id=order_id).all()]
    return jsonify(result)

# ── TICKETS ───────────────────────────────────────────────────────────────────
@app.route('/api/tickets/<int:order_id>', methods=['GET'])
def get_ticket(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != 'approved':
        return jsonify({'status': order.status,
                        'message': 'Ticket not yet issued. Awaiting payment approval.',
                        'order_id': order_id}), 202
    event   = Event.query.get(order.event_id)
    tickets = Ticket.query.filter_by(order_id=order_id).all()
    return jsonify({
        'order_id': order.id, 'status': 'approved',
        'event': event.title if event else '', 'date': event.date if event else '',
        'time': event.time if event else '', 'venue': event.venue if event else '',
        'image_url': event.image_url if event else '',
        'category': event.category if event else '',
        'email': order.email, 'name': order.name, 'total': order.total,
        'tickets': [t.to_dict() for t in tickets],
    })

@app.route('/api/verify', methods=['GET'])
def verify_ticket():
    code   = request.args.get('ticketId', '').strip()
    ticket = Ticket.query.filter_by(ticket_code=code).first()
    if not ticket: return jsonify({'valid': False, 'message': 'Invalid ticket'}), 404
    order  = Order.query.get(ticket.order_id)
    event  = Event.query.get(order.event_id) if order else None
    return jsonify({'valid': True, 'ticketId': ticket.ticket_code,
                    'seat': ticket.seat_number, 'name': order.name if order else '',
                    'event': event.title if event else '', 'date': event.date if event else ''})

# ── ADMIN ─────────────────────────────────────────────────────────────────────
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data.get('email','').strip().lower() == ADMIN_EMAIL and data.get('password','').strip() == ADMIN_PASSWORD:
        return jsonify({'message': 'Login successful', 'token': 'admin-demo-token-2024'})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/admin/orders', methods=['GET'])
def admin_get_orders():
    status_filter = request.args.get('status', '')
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter: query = query.filter(Order.status == status_filter)
    result = []
    for o in query.all():
        ev   = Event.query.get(o.event_id)
        tier = TicketTier.query.get(o.tier_id) if o.tier_id else None
        result.append({
            'order_id': o.id, 'status': o.status, 'name': o.name, 'email': o.email,
            'event': ev.title if ev else '', 'tier': tier.name if tier else '',
            'quantity': o.quantity, 'total': o.total,
            'payment_method': o.payment_method, 'crypto_currency': o.crypto_currency,
            'tx_reference': o.tx_reference,
            'created_at': o.created_at.isoformat() if o.created_at else '',
        })
    return jsonify(result)

@app.route('/api/admin/approve', methods=['POST'])
def admin_approve():
    data  = request.get_json()
    order = Order.query.get(data.get('order_id'))
    if not order: return jsonify({'error': 'Order not found'}), 404
    if order.status == 'approved': return jsonify({'error': 'Already approved'}), 400
    order.status = 'approved'
    tickets = create_tickets_for_order(order)  # ← Tickets generated HERE ONLY
    db.session.commit()
    return jsonify({'message': f'Approved. {len(tickets)} ticket(s) generated.',
                    'order_id': order.id, 'tickets': tickets})

@app.route('/api/admin/reject', methods=['POST'])
def admin_reject():
    data  = request.get_json()
    order = Order.query.get(data.get('order_id'))
    if not order: return jsonify({'error': 'Order not found'}), 404
    if order.status in ('approved', 'rejected'):
        return jsonify({'error': f'Order already {order.status}'}), 400
    order.status = 'rejected'
    tier = TicketTier.query.get(order.tier_id)
    if tier: tier.available += order.quantity  # Restore seats
    db.session.commit()
    return jsonify({'message': f'Order #{order.id} rejected. Seats restored.'})

@app.route('/api/admin/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    # Only block deletion if there are ACTIVE orders (not rejected ones)
    active_orders = Order.query.filter(
        Order.event_id == event_id,
        Order.status.in_(['pending_payment', 'payment_submitted', 'approved'])
    ).all()
    if active_orders:
        return jsonify({'error': f'Cannot delete event with {len(active_orders)} active order(s). Reject all orders first.'}), 400
    # Safe to delete: cascade delete all tickets and orders for this event
    for order in Order.query.filter_by(event_id=event_id).all():
        Ticket.query.filter_by(order_id=order.id).delete()
        db.session.delete(order)
    TicketTier.query.filter_by(event_id=event_id).delete()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': f'Event "{event.title}" deleted successfully'})

@app.route('/api/admin/events', methods=['GET'])
def get_admin_events():
    events = Event.query.order_by(Event.created_at.desc()).all()
    return jsonify([e.to_dict(include_tiers=True) for e in events])

# ── ENTRY ─────────────────────────────────────────────────────────────────────
def fix_image_urls():
    """Fix any events that still have local filenames instead of proper image URLs."""
    IMAGE_MAP = {
        'unnamed (20).png': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=800&q=80',
        'unnamed (21).png': 'https://images.unsplash.com/photo-1540039155732-68ee23e15b51?auto=format&fit=crop&w=800&q=80',
        'unnamed (22).png': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=800&q=80',
        'unnamed (23).png': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80',
        'unnamed (24).png': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80',
        'unnamed (25).png': 'https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?auto=format&fit=crop&w=800&q=80',
    }
    fixed = 0
    events = Event.query.all()
    for ev in events:
        # Fix known local filenames
        if ev.image_url in IMAGE_MAP:
            ev.image_url = IMAGE_MAP[ev.image_url]
            fixed += 1
        # Fix any other local filenames (not starting with http)
        elif ev.image_url and not ev.image_url.startswith('http'):
            ev.image_url = 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=800&q=80'
            fixed += 1
    if fixed > 0:
        db.session.commit()
        logger.info(f"Fixed image URLs for {fixed} event(s)")

def force_update_event_images():
    """Force-apply curated images to specific events by title.
    Add entries here to update any event's image on the next deploy/restart.
    """
    CURATED = {
        # Event 1: Neon Horizon World Tour — vivid concert stage with crowd
        'Neon Horizon World Tour': 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80',
    }
    updated = 0
    for title, new_url in CURATED.items():
        ev = Event.query.filter(Event.title.ilike(title)).first()
        if ev and ev.image_url != new_url:
            ev.image_url = new_url
            updated += 1
    if updated > 0:
        db.session.commit()
        logger.info(f"force_update_event_images: updated {updated} event(s)")

def init_db():
    """Initialize database tables and seed data"""
    try:
        logger.info("Initializing database...")
        db.create_all()
        logger.info("Database tables created")
        
        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE ticket_tiers ADD COLUMN view_image VARCHAR(500) DEFAULT ''"))
                conn.commit()
            logger.info("Migrated ticket_tiers: Added view_image column")
        except Exception:
            pass
            
        fix_image_urls()          # Fix broken local image filenames first
        seed_data()               # Seed sample events if DB is empty
        force_update_event_images()  # Apply curated image overrides
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

# Initialize database when app starts (for gunicorn)
with app.app_context():
    init_db()

# For local development only
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting TicketHubLive API on port {port} (development mode)")
    app.run(host='0.0.0.0', debug=True, port=port)

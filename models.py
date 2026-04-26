from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = 'events'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    category    = db.Column(db.String(50), default='Concert')
    description = db.Column(db.Text, default='')
    date        = db.Column(db.String(50), default='')
    time        = db.Column(db.String(50), default='')
    venue       = db.Column(db.String(200), default='')
    image_url   = db.Column(db.String(500), default='')
    created_at  = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    tiers  = db.relationship('TicketTier', backref='event', lazy=True, cascade='all, delete')
    orders = db.relationship('Order', backref='event', lazy=True)

    def to_dict(self, include_tiers=False):
        d = {
            'id': self.id, 'title': self.title, 'category': self.category,
            'description': self.description, 'date': self.date, 'time': self.time,
            'venue': self.venue, 'image_url': self.image_url,
        }
        if include_tiers:
            d['tiers'] = [t.to_dict() for t in self.tiers]
        else:
            prices = [t.price for t in self.tiers]
            d['min_price'] = min(prices) if prices else 0
        return d


class TicketTier(db.Model):
    __tablename__ = 'ticket_tiers'
    id        = db.Column(db.Integer, primary_key=True)
    event_id  = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    name      = db.Column(db.String(100), nullable=False)
    price     = db.Column(db.Float, nullable=False)
    quantity  = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price,
                'quantity': self.quantity, 'available': self.available}


class Order(db.Model):
    __tablename__ = 'orders'
    id              = db.Column(db.Integer, primary_key=True)
    event_id        = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    tier_id         = db.Column(db.Integer, nullable=True)
    quantity        = db.Column(db.Integer, default=1)
    email           = db.Column(db.String(200), nullable=False)
    name            = db.Column(db.String(200), nullable=False)
    payment_method  = db.Column(db.String(50), default='cryptocurrency')
    crypto_currency = db.Column(db.String(20), default='USDT_TRC20')
    subtotal        = db.Column(db.Float, default=0)
    service_fee     = db.Column(db.Float, default=0)
    processing_fee  = db.Column(db.Float, default=0)
    total           = db.Column(db.Float, default=0)
    # pending_payment | payment_submitted | approved | rejected
    status          = db.Column(db.String(30), default='pending_payment')
    tx_reference    = db.Column(db.String(500), default='')
    created_at      = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    tickets = db.relationship('Ticket', backref='order', lazy=True, cascade='all, delete')


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id          = db.Column(db.Integer, primary_key=True)
    order_id    = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    seat_number = db.Column(db.String(100), default='')
    ticket_code = db.Column(db.String(50), unique=True, nullable=False)
    qr_data     = db.Column(db.Text, default='')   # base64 PNG data URI
    created_at  = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'seat': self.seat_number,
                'code': self.ticket_code, 'qr_data': self.qr_data}

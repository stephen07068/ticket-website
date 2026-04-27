/**
 * TicketHubLive – API Helper
 * All fetch calls to the Flask backend go through this file.
 * Base URL auto-detects local dev vs. same-origin production.
 */
const API_BASE = 'http://localhost:5000';

const API = {
  /* ─── EVENTS ─────────────────────────────────── */

  /** GET /api/events?category=&q= */
  async getEvents(category = '', q = '') {
    const params = new URLSearchParams();
    if (category) params.set('category', category);
    if (q)        params.set('q', q);
    const url = `${API_BASE}/api/events${params.toString() ? '?' + params : ''}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch events');
    const data = await res.json();
    // Normalise shape: map backend fields → frontend expectations
    return data.map(e => ({
      id:           e.id,
      title:        e.title,
      category:     (e.category || '').toLowerCase(),
      date:         e.date,
      time:         e.time,
      venue:        e.venue,
      description:  e.description,
      image:        e.image_url || '',
      ticket_price: e.min_price ?? e.ticket_price ?? 0,
    }));
  },

  /** GET /api/events/:id */
  async getEvent(id) {
    const res = await fetch(`${API_BASE}/api/events/${id}`);
    if (!res.ok) throw new Error('Event not found');
    const e = await res.json();
    return {
      id:          e.id,
      title:       e.title,
      category:    (e.category || '').toLowerCase(),
      date:        e.date,
      time:        e.time,
      venue:       e.venue,
      description: e.description,
      image:       e.image_url || '',
      ticket_price: e.tiers && e.tiers.length ? e.tiers[0].price : 0,
      tiers:       e.tiers || [],
    };
  },

  /* ─── CHECKOUT ────────────────────────────────── */

  /** POST /api/checkout */
  async checkout(payload) {
    const res = await fetch(`${API_BASE}/api/checkout`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Checkout failed');
    return data;
  },

  /* ─── PAYMENTS & ORDERS ─────────────────────── */

  async getWallets() {
    const res = await fetch(`${API_BASE}/api/wallets`);
    if (!res.ok) throw new Error('Failed to fetch wallets');
    return res.json();
  },

  async getWhatsappLink(orderId, method) {
    const res = await fetch(`${API_BASE}/api/whatsapp-link?order_id=${orderId}&method=${encodeURIComponent(method)}`);
    if (!res.ok) throw new Error('Failed to fetch WhatsApp link');
    return res.json();
  },

  async submitPayment(orderId, txReference) {
    const res = await fetch(`${API_BASE}/api/payments/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: orderId, tx_reference: txReference })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to submit payment');
    return data;
  },

  async getOrder(orderId) {
    const res = await fetch(`${API_BASE}/api/orders/${orderId}`);
    if (!res.ok) throw new Error('Order not found');
    return res.json();
  },

  /* ─── TICKETS ─────────────────────────────────── */

  async getTicket(orderId) {
    const res = await fetch(`${API_BASE}/api/tickets/${orderId}`);
    const data = await res.json();
    // Return the response directly so the frontend can check `data.status`
    return data;
  },

  async verifyTicket(ticketId) {
    const res = await fetch(`${API_BASE}/api/verify?ticketId=${encodeURIComponent(ticketId)}`);
    return res.json();
  },

  /* ─── ADMIN ───────────────────────────────────── */

  async adminLogin(email, password) {
    const res = await fetch(`${API_BASE}/api/admin/login`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Login failed');
    return data;
  },

  async createEvent(payload) {
    const res = await fetch(`${API_BASE}/api/admin/events`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Could not create event');
    return data;
  },

  async getAdminOrders(status = '') {
    const res = await fetch(`${API_BASE}/api/admin/orders${status ? '?status=' + status : ''}`);
    if (!res.ok) throw new Error('Failed to fetch orders');
    return res.json();
  },

  async adminApprove(orderId) {
    const res = await fetch(`${API_BASE}/api/admin/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: orderId })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to approve');
    return data;
  },

  async adminReject(orderId) {
    const res = await fetch(`${API_BASE}/api/admin/reject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: orderId })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to reject');
    return data;
  },

  async getAdminEvents() {
    const res = await fetch(`${API_BASE}/api/admin/events`);
    if (!res.ok) throw new Error('Failed to fetch events');
    return res.json();
  },

  async deleteEvent(eventId) {
    const res = await fetch(`${API_BASE}/api/admin/events/${eventId}`, {
      method: 'DELETE'
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to delete event');
    return data;
  }
};

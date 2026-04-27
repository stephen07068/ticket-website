from app import app, init_db
import logging

logging.basicConfig(level=logging.INFO)

print("Forcing database initialization...")
with app.app_context():
    try:
        init_db()
        print("✅ Database tables created and seeded successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

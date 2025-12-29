import sys
import os

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models.user_model import User
from models.announcement_model import Announcement
from models.upload_model import Upload

app = create_app()

with app.app_context():
    db.create_all()
    
    # Check if admin exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        print("Creating default admin user...")
        # Mobile number '0000000000' for default admin
        admin = User(full_name='Admin User', email='admin@cse.edu', mobile_number='0000000000', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created (email: admin@cse.edu, mobile: 0000000000, password: admin123)")
    else:
        # Force update password to ensure it is correct
        admin.set_password('admin123')
        db.session.commit()
        print("Admin user exists. Password reset to: admin123")

    print("Database initialized successfully!")

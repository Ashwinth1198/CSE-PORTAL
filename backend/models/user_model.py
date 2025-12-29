from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# We will initialize db in the main app or a extensions file to avoid circular imports, 
# but for this structure let's follow a pattern where models might expect db from an extensions file.
# However, since we don't have an extensions.py yet, let's create a local db instance in app.py or 
# assume a cleaner pattern. 
# Best practice: create a separate 'extensions.py' or similar. 
# Given the empty folders, I'll implicitly create a shared db instance here or in app.py.
# To keep it simple and avoid import errors, I'll use the 'db' from a new extensions module I'll create, 
# or just put it in a common place. 
# Let's create `d:/cse/extensions.py` first to hold the `db` object to avoid circular imports.

from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    faculty_id = db.Column(db.String(50), unique=True, nullable=True)
    registration_number = db.Column(db.String(50), unique=True, nullable=True)
    year = db.Column(db.String(10), nullable=True)
    semester = db.Column(db.String(10), nullable=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='student') # 'admin' or 'student'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

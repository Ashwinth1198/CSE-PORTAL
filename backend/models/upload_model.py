from datetime import datetime
from extensions import db

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False) # 'material' or 'video'
    year = db.Column(db.String(10), nullable=False, default='1') # '1', '2', '3', '4' for academic years
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)


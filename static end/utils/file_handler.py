import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import time

def save_file(file, upload_type='misc'):
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        # Prepend timestamp to ensure uniqueness
        filename = f"{int(time.time())}_{original_filename}"
        
        # Ensure directory exists
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_type)
        os.makedirs(path, exist_ok=True)
        
        file_path = os.path.join(path, filename)
        file.save(file_path)
        return filename
    return None

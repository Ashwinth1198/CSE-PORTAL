from flask import Blueprint, render_template, send_from_directory, current_app
from flask_login import login_required, current_user
from models.announcement_model import Announcement
from models.upload_model import Upload
import os

student = Blueprint('student', __name__)

@student.route('/student/dashboard')
@login_required
def dashboard():
    announcement_count = Announcement.query.count()
    material_count = Upload.query.filter_by(file_type='material').count()
    video_count = Upload.query.filter_by(file_type='video').count()
    
    # Get recent announcements (last 5)
    recent_announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
    
    return render_template('student/dashboard.html', 
                           announcement_count=announcement_count,
                           material_count=material_count,
                           video_count=video_count,
                           recent_announcements=recent_announcements)

@student.route('/student/announcements')
@login_required
def announcements():
    all_announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('student/announcements.html', announcements=all_announcements)

@student.route('/student/materials')
@login_required
def materials():
    materials = Upload.query.filter_by(file_type='material').order_by(Upload.upload_date.desc()).all()
    return render_template('student/materials.html', materials=materials)

@student.route('/student/videos')
@login_required
def videos():
    videos = Upload.query.filter_by(file_type='video').order_by(Upload.upload_date.desc()).all()
    return render_template('student/videos.html', videos=videos)

@student.route('/uploads/<type>/<filename>')
@login_required
def download_file(type, filename):
    # Ensure type is valid to prevent directory traversal
    if type not in ['material', 'video']:
        return "Access denied", 403
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], type), filename)

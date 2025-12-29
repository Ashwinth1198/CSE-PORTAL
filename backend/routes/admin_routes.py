from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from utils.decorators import admin_required
from models.announcement_model import Announcement
from models.upload_model import Upload
from models.user_model import User
from extensions import db
from utils.file_handler import save_file

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    student_count = User.query.filter_by(role='student').count()
    faculty_count = User.query.filter_by(role='admin').count()
    announcement_count = Announcement.query.count()
    material_count = Upload.query.filter_by(file_type='material').count()
    video_count = Upload.query.filter_by(file_type='video').count()
    
    # Get recent announcements (last 5)
    recent_announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           student_count=student_count, 
                           faculty_count=faculty_count,
                           announcement_count=announcement_count,
                           material_count=material_count,
                           video_count=video_count,
                           recent_announcements=recent_announcements)

@admin.route('/admin/announcements', methods=['GET', 'POST'])
@login_required
@admin_required
def announcements():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            new_announcement = Announcement(title=title, content=content)
            db.session.add(new_announcement)
            db.session.commit()
            flash('Announcement created!', 'success')
        else:
            flash('Title and Content are required', 'danger')
        return redirect(url_for('admin.announcements'))
    
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', announcements=announcements)

@admin.route('/admin/uploads', methods=['GET', 'POST'])
@login_required
@admin_required
def uploads():
    if request.method == 'POST':
        file = request.files.get('file')
        file_type = request.form.get('type') # 'material' or 'video'
        year = request.form.get('year', '1') # Academic year 1-4
        
        if file and file_type and year:
            try:
                filename = save_file(file, upload_type=file_type)
                if filename:
                    new_upload = Upload(filename=filename, original_name=file.filename, file_type=file_type, year=year)
                    db.session.add(new_upload)
                    db.session.commit()
                    flash('File uploaded successfully', 'success')
                else:
                    flash('Invalid file or upload failed', 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred during upload: {str(e)}', 'danger')
        else:
            flash('File, Type and Year are required', 'danger')
        return redirect(url_for('admin.uploads'))

    # Get all uploads grouped by year for display
    all_uploads = Upload.query.order_by(Upload.upload_date.desc()).all()
    return render_template('admin/upload.html', uploads=all_uploads)


@admin.route('/admin/users')
@login_required
@admin_required
def users():
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)

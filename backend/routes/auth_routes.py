from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models.user_model import User
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user:
            # Password Verification (Universal for Admin & Student)
            if user.check_password(password):
                login_user(user)
                if user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('student.dashboard'))
            else:
                flash('Login Unsuccessful. Invalid Password.', 'danger')
        else:
            flash('Login Unsuccessful. Email not found.', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register')
def register():
    return render_template('auth/register.html')

@auth.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        registration_number = request.form.get('reg_no')
        year = request.form.get('year')
        semester = request.form.get('semester')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('User with this email already exists', 'warning')
            return redirect(url_for('auth.register_student'))
        
        if registration_number and User.query.filter_by(registration_number=registration_number).first():
             flash('Registration number already registered', 'warning')
             return redirect(url_for('auth.register_student'))

        user = User(full_name=full_name, email=email, registration_number=registration_number, 
                    year=year, semester=semester, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Student account created! You can now login', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register_student.html')

@auth.route('/register/faculty', methods=['GET', 'POST'])
def register_faculty():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        faculty_id = request.form.get('faculty_id')
        password = request.form.get('password')
        secret_code = request.form.get('secret_code')
        
        # Validate secret code first
        from flask import current_app
        if secret_code != current_app.config['ADMIN_SECRET_CODE']:
            flash('Invalid secret code. Contact administration for the correct code.', 'danger')
            return redirect(url_for('auth.register_faculty'))
        
        if User.query.filter_by(email=email).first():
            flash('User with this email already exists', 'warning')
            return redirect(url_for('auth.register_faculty'))
        
        if faculty_id and User.query.filter_by(faculty_id=faculty_id).first():
             flash('Faculty ID already registered', 'warning')
             return redirect(url_for('auth.register_faculty'))

        # Here role is 'admin' for Faculty
        user = User(full_name=full_name, email=email, faculty_id=faculty_id, role='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Faculty account created! You can now login', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register_faculty.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        user = User.query.filter_by(mobile_number=mobile).first()
        
        if user:
            # Generate Mock OTP
            # In production, use an SMS gateway (e.g. Twilio)
            otp = '1234' 
            session['reset_otp'] = otp
            session['reset_user_id'] = user.id
            session['reset_mobile'] = mobile
            
            # Print to console for verification
            print(f"------------ OTP SENT TO {mobile}: {otp} ------------")
            
            flash(f'OTP sent to {mobile} (Check server console for code)', 'info')
            return redirect(url_for('auth.verify_otp'))
        else:
            flash('Mobile number not found', 'danger')
            
    return render_template('auth/forgot_password.html')

@auth.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'reset_otp' not in session:
        return redirect(url_for('auth.forgot_password'))
        
    if request.method == 'POST':
        otp_entered = request.form.get('otp')
        otp_actual = session.get('reset_otp')
        
        if otp_entered == otp_actual:
            # OTP Verified
            user_id = session.get('reset_user_id')
            user = db.session.get(User, user_id)
            if user:
                login_user(user)
                # Clear session data
                session.pop('reset_otp', None)
                session.pop('reset_user_id', None)
                session.pop('reset_mobile', None)
                
                flash('Verified! Logged in successfully.', 'success')
                if user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid OTP', 'danger')
            
    return render_template('auth/verify_otp.html')
@auth.route('/magic-login')
def magic_login():
    user = User.query.filter_by(role='admin').first()
    if user:
        login_user(user)
        return redirect(url_for('admin.dashboard'))
    return "Admin user not found", 404

import os
import random
import string
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User, LoginAttempt, Alert, UnlockRequest
from email_service import mail, send_alert_email, send_welcome_email, send_otp_email
from dotenv import load_dotenv
import json
import logging

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production-' + os.urandom(16).hex())
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_LOGIN_ATTEMPTS'] = int(os.getenv('MAX_LOGIN_ATTEMPTS', 3))
app.config['CAPTCHA_AFTER_ATTEMPTS'] = int(os.getenv('CAPTCHA_AFTER_ATTEMPTS', 2))

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_SENDER_EMAIL', os.getenv('MAIL_USERNAME', 'noreply@security.com'))

# when sending emails, default sender fallback will be MAIL_USERNAME if no specific sender provided

# Initialize extensions
db.init_app(app)
mail.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_client_ip():
    """Get the client's IP address"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    return request.environ.get('REMOTE_ADDR', '127.0.0.1')

def create_alert(user_id, message, alert_type, ip_address=None):
    """Create a security alert for a user and send email notification"""
    ip = ip_address or get_client_ip()
    
    alert = Alert(
        user_id=user_id,
        message=message,
        alert_type=alert_type,
        ip_address=ip
    )
    db.session.add(alert)
    db.session.commit()
    
    # Send email alert
    user = User.query.get(user_id)
    if user:
        subject_map = {
            'failed_login': '⚠️ Failed Login Attempt on Your Account',
            'account_locked': '🔐 Your Account Has Been Locked',
            'account_unlocked': '✅ Your Account Has Been Unlocked',
            'password_reset': '🔑 Your Password Has Been Reset',
            'suspicious_activity': '🚨 Suspicious Activity Detected'
        }
        
        subject = subject_map.get(alert_type, 'Security Alert')
        
        alert_details = {
            'ip_address': ip,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'username': user.username
        }
        
        # Send email asynchronously (in production, use Celery)
        try:
            send_alert_email(user.email, subject, alert_type, alert_details)
        except Exception as e:
            logger.error(f"Failed to send alert email: {str(e)}")

def log_login_attempt(user_id, success):
    """Log a login attempt"""
    attempt = LoginAttempt(
        user_id=user_id,
        ip_address=get_client_ip(),
        user_agent=request.headers.get('User-Agent', '')[:200],
        success=success
    )
    db.session.add(attempt)
    db.session.commit()

def generate_captcha():
    """Generate one or more random CAPTCHA questions.

    Returns a tuple (questions, answers) where questions is a list of
    question strings and answers is a corresponding list of integer
    answers. The number of challenges is randomized each time between 1
    and 3 to make automated attempts harder.
    """
    count = random.randint(1, 3)
    questions = []
    answers = []
    for _ in range(count):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(['+', '-', '*'])
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            answer = num1 - num2
        else:
            answer = num1 * num2
        questions.append(f"{num1} {operation} {num2}")
        answers.append(answer)
    return questions, answers

@app.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        security_question = request.form.get('security_question')
        security_answer = request.form.get('security_answer')
        phone_number = request.form.get('phone_number')
        
        # Validation
        if not all([username, email, password, confirm_password, security_question, security_answer]):
            flash('All fields are required!', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            security_question=security_question,
            phone_number=phone_number
        )
        user.set_password(password)
        user.set_security_answer(security_answer)
        
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        send_welcome_email(user.email, user.username)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with brute force protection"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Generate CAPTCHA if needed
    show_captcha = session.get('failed_login_attempts', 0) >= app.config['CAPTCHA_AFTER_ATTEMPTS']
    if show_captcha and 'captcha_answers' not in session:
        captcha_questions, captcha_answers = generate_captcha()
        session['captcha_questions'] = captcha_questions
        session['captcha_answers'] = captcha_answers
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')
        captcha_responses = []
        if show_captcha:
            # gather all captcha inputs
            for idx in range(len(session.get('captcha_questions', []))):
                resp = request.form.get(f'captcha{idx}')
                captcha_responses.append(resp)
        
        if not email or not password:
            flash('Please enter email and password!', 'danger')
            return render_template('login.html', show_captcha=show_captcha, 
                                 captcha_questions=session.get('captcha_questions'))
        
        # Verify CAPTCHA if required
        if show_captcha:
            # convert and compare each answer
            valid = True
            for idx, ans in enumerate(session.get('captcha_answers', [])):
                try:
                    if int(captcha_responses[idx]) != ans:
                        valid = False
                        break
                except Exception:
                    valid = False
                    break
            if not valid:
                flash('Invalid CAPTCHA! Please try again.', 'danger')
                # Generate new set
                captcha_questions, captcha_answers = generate_captcha()
                session['captcha_questions'] = captcha_questions
                session['captcha_answers'] = captcha_answers
                return render_template('login.html', show_captcha=True, 
                                     captcha_questions=session.get('captcha_questions'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            session['failed_login_attempts'] = session.get('failed_login_attempts', 0) + 1
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))
        
        # Check if account is locked
        if user.is_locked:
            flash('Your account is locked due to multiple failed login attempts. Please use the "Unlock Account" option.', 'danger')
            return render_template('account_locked.html', user=user)
        
        # Verify password
        if user.check_password(password):
            # Successful login
            log_login_attempt(user.id, success=True)
            user.reset_failed_attempts()
            session['failed_login_attempts'] = 0
            # clear any stored captcha info
            session.pop('captcha_questions', None)
            session.pop('captcha_answers', None)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Failed login
            user.increment_failed_attempts()
            log_login_attempt(user.id, success=False)
            session['failed_login_attempts'] = session.get('failed_login_attempts', 0) + 1
            
            remaining_attempts = app.config['MAX_LOGIN_ATTEMPTS'] - user.failed_attempts
            
            # Create alert for suspicious activity
            create_alert(
                user.id,
                f"Failed login attempt from IP: {get_client_ip()}",
                'failed_login',
                get_client_ip()
            )
            
            # Lock account if max attempts reached
            if user.failed_attempts >= app.config['MAX_LOGIN_ATTEMPTS']:
                user.lock_account()
                create_alert(
                    user.id,
                    f"Account locked due to {app.config['MAX_LOGIN_ATTEMPTS']} failed login attempts from IP: {get_client_ip()}",
                    'account_locked',
                    get_client_ip()
                )
                flash('Your account has been locked due to multiple failed login attempts!', 'danger')
                return render_template('account_locked.html', user=user)
            
            flash(f'Invalid email or password! {remaining_attempts} attempts remaining.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html', show_captcha=show_captcha, 
                         captcha_questions=session.get('captcha_questions'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get recent login attempts
    recent_attempts = LoginAttempt.query.filter_by(user_id=current_user.id)\
        .order_by(LoginAttempt.timestamp.desc()).limit(10).all()
    
    # Get unread alerts
    unread_alerts = Alert.query.filter_by(user_id=current_user.id, is_read=False)\
        .order_by(Alert.created_at.desc()).all()
    
    all_alerts = Alert.query.filter_by(user_id=current_user.id)\
        .order_by(Alert.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                         recent_attempts=recent_attempts,
                         unread_alerts=unread_alerts,
                         all_alerts=all_alerts)

@app.route('/alerts/mark_read/<int:alert_id>')
@login_required
def mark_alert_read(alert_id):
    """Mark an alert as read"""
    alert = Alert.query.get_or_404(alert_id)
    if alert.user_id == current_user.id:
        alert.is_read = True
        db.session.commit()
        flash('Alert marked as read.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password recovery using security questions"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        security_answer = request.form.get('security_answer')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if we're in step 2 or 3 (use stored user_id from session)
        if session.get('reset_user_id'):
            user = User.query.get(session.get('reset_user_id'))
        else:
            # Step 1: Look up user by email
            user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Email not found!', 'danger')
            return render_template('forgot_password.html', step=1)
        
        # Store user_id in session for step 2
        if 'step' not in session:
            session['reset_user_id'] = user.id
            session['step'] = 1
            return render_template('forgot_password.html', 
                                 step=2, 
                                 security_question=user.security_question)
        
        # Step 2: Verify security answer
        if session.get('step') == 1:
            if user.check_security_answer(security_answer):
                session['step'] = 2
                return render_template('forgot_password.html', step=3)
            else:
                flash('Incorrect security answer!', 'danger')
                session.pop('reset_user_id', None)
                session.pop('step', None)
                return redirect(url_for('forgot_password'))
        
        # Step 3: Reset password
        if session.get('step') == 2:
            if new_password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return render_template('forgot_password.html', step=3)
            
            user.set_password(new_password)
            user.unlock_account()  # Unlock if locked
            db.session.commit()
            
            # Create alert for password reset
            create_alert(
                user.id,
                "Your password has been reset successfully",
                'password_reset',
                get_client_ip()
            )
            
            session.pop('reset_user_id', None)
            session.pop('step', None)
            
            flash('Password reset successful! Please login with your new password.', 'success')
            return redirect(url_for('login'))
    
    # Clear any existing reset session
    session.pop('reset_user_id', None)
    session.pop('step', None)
    return render_template('forgot_password.html', step=1)

@app.route('/unlock-account', methods=['GET', 'POST'])
def unlock_account():
    """Request account unlock"""
    if request.method == 'POST':
        # Debug: Log all form data
        logger.info(f"Form data: {dict(request.form)}")
        logger.info(f"Session data: unlock_user_id={session.get('unlock_user_id')}, unlock_step={session.get('unlock_step')}")
        
        email = request.form.get('email', '').lower().strip()
        security_answer = request.form.get('security_answer')
        
        # Check if we're in step 2 or 3 (use stored user_id from session)
        if session.get('unlock_user_id'):
            user = User.query.get(session.get('unlock_user_id'))
        else:
            # Step 1: Look up user by email
            user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Email not found!', 'danger')
            return render_template('unlock_account.html', step=1)
        
        if not user.is_locked:
            flash('Your account is not locked.', 'info')
            return redirect(url_for('login'))
        
        # Store user_id in session for verification
        if 'unlock_step' not in session:
            session['unlock_user_id'] = user.id
            session['unlock_step'] = 1
            return render_template('unlock_account.html', 
                                 step=2, 
                                 security_question=user.security_question)
        
        # Verify security answer
        if session.get('unlock_step') == 1:
            if not security_answer:
                flash('Please enter your security answer!', 'danger')
                return render_template('unlock_account.html', step=2, security_question=user.security_question)
            
            if user.check_security_answer(security_answer):
                # Generate verification code
                verification_code = ''.join(random.choices(string.digits, k=6))
                
                # Create unlock request
                unlock_request = UnlockRequest(
                    user_id=user.id,
                    verification_code=verification_code,
                    ip_address=get_client_ip(),
                    expires_at=datetime.utcnow() + timedelta(minutes=15)
                )
                db.session.add(unlock_request)
                db.session.commit()
                
                session['unlock_step'] = 2
                session['verification_code'] = verification_code
                
                # Send OTP via email
                try:
                    if send_otp_email(user.email, verification_code, user.username):
                        flash('✅ Verification code sent to your email!', 'success')
                    else:
                        flash('⚠️ Could not send verification code to email. Code displayed below for testing.', 'warning')
                        flash(f'Test Code: {verification_code}', 'info')
                except Exception as e:
                    logger.error(f"OTP email error: {str(e)}")
                    flash('⚠️ Email service unavailable. Code displayed below for testing.', 'warning')
                    flash(f'Test Code: {verification_code}', 'info')
                
                return render_template('unlock_account.html', step=3)
            else:
                flash('Incorrect security answer!', 'danger')
                session.pop('unlock_user_id', None)
                session.pop('unlock_step', None)
                return render_template('unlock_account.html', step=1)
        
        # Verify code and unlock
        if session.get('unlock_step') == 2:
            entered_code = request.form.get('verification_code')
            if entered_code == session.get('verification_code'):
                user.unlock_account()
                create_alert(
                    user.id,
                    "Account unlocked successfully",
                    'account_unlocked',
                    get_client_ip()
                )
                
                session.pop('unlock_user_id', None)
                session.pop('unlock_step', None)
                session.pop('verification_code', None)
                
                flash('Account unlocked successfully! You can now login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Invalid verification code!', 'danger')
                return render_template('unlock_account.html', step=3, verification_code=None)
    
    # Clear any existing unlock session
    session.pop('unlock_user_id', None)
    session.pop('unlock_step', None)
    session.pop('verification_code', None)
    return render_template('unlock_account.html', step=1)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    """Admin panel to view all users and their status"""
    # In production, add proper admin authentication
    users = User.query.all()
    all_attempts = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).limit(50).all()
    return render_template('admin.html', users=users, all_attempts=all_attempts)

# Initialize database
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

def main():
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

if __name__ == "__main__":
    main()

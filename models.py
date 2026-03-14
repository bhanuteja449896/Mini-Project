from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Personal details for password recovery
    security_question = db.Column(db.String(200))
    security_answer_hash = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    
    # Face authentication data (stores encoded face data as string)
    face_encoding = db.Column(db.Text)
    
    # Account status
    is_locked = db.Column(db.Boolean, default=False)
    failed_attempts = db.Column(db.Integer, default=0)
    last_failed_attempt = db.Column(db.DateTime)
    locked_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    login_attempts = db.relationship('LoginAttempt', backref='user', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def set_security_answer(self, answer):
        """Hash and set security answer"""
        self.security_answer_hash = generate_password_hash(answer.lower())
    
    def check_security_answer(self, answer):
        """Check if provided security answer matches hash"""
        if not answer:
            return False
        return check_password_hash(self.security_answer_hash, answer.lower())
    
    def lock_account(self):
        """Lock the user account"""
        self.is_locked = True
        self.locked_at = datetime.utcnow()
        db.session.commit()
    
    def unlock_account(self):
        """Unlock the user account and reset failed attempts"""
        self.is_locked = False
        self.failed_attempts = 0
        self.locked_at = None
        self.last_failed_attempt = None
        db.session.commit()
    
    def increment_failed_attempts(self):
        """Increment failed login attempts"""
        self.failed_attempts += 1
        self.last_failed_attempt = datetime.utcnow()
        db.session.commit()
    
    def reset_failed_attempts(self):
        """Reset failed login attempts after successful login"""
        self.failed_attempts = 0
        self.last_failed_attempt = None
        self.last_login = datetime.utcnow()
        db.session.commit()


class LoginAttempt(db.Model):
    """Track all login attempts for security monitoring"""
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)  # Support IPv6
    user_agent = db.Column(db.String(200))
    success = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LoginAttempt {self.ip_address} - {"Success" if self.success else "Failed"}>'


class Alert(db.Model):
    """Store security alerts for users"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50))  # 'failed_login', 'account_locked', 'suspicious_activity'
    ip_address = db.Column(db.String(45))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Alert {self.alert_type} for user {self.user_id}>'


class UnlockRequest(db.Model):
    """Track account unlock requests"""
    __tablename__ = 'unlock_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    verification_code = db.Column(db.String(6), nullable=False)
    ip_address = db.Column(db.String(45))
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User', backref='unlock_requests')
    
    def __repr__(self):
        return f'<UnlockRequest for user {self.user_id}>'

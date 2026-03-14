"""
Email notification service for security alerts
"""
import os
from flask_mail import Mail, Message
import logging

logger = logging.getLogger(__name__)

mail = Mail()


def send_alert_email(user_email, subject, alert_type, alert_details):
    """
    Send security alert emails to users
    
    Args:
        user_email: User's email address
        subject: Email subject
        alert_type: Type of alert (failed_login, account_locked, account_unlocked, password_reset)
        alert_details: Dictionary with details like IP address, timestamp, etc.
    """
    try:
        sender_email = os.getenv('MAIL_SENDER_EMAIL', os.getenv('MAIL_USERNAME', 'noreply@security.com'))
        sender_name = os.getenv('MAIL_SENDER_NAME', 'Security Alert')
        
        # Build email body based on alert type
        body = build_email_body(alert_type, alert_details)
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=body,
            sender=(sender_name, sender_email)
        )
        
        # Send email
        mail.send(msg)
        logger.info(f"Alert email sent to {user_email} - Type: {alert_type}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {str(e)}")
        return False


def build_email_body(alert_type, details):
    """
    Build HTML email body based on alert type
    """
    ip_address = details.get('ip_address', 'Unknown')
    timestamp = details.get('timestamp', '')
    username = details.get('username', 'User')
    
    # Common header and footer
    header = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
            .header {{ background: #2563eb; color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ padding: 20px; background: #f9fafb; }}
            .alert-box {{ padding: 15px; margin: 15px 0; border-radius: 5px; }}
            .alert-danger {{ background: #fee2e2; border-left: 4px solid #ef4444; color: #991b1b; }}
            .alert-warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; color: #78350f; }}
            .alert-success {{ background: #d1fae5; border-left: 4px solid #22c55e; color: #065f46; }}
            .details {{ background: white; padding: 10px; border-radius: 5px; margin: 10px 0; }}
            .detail-item {{ padding: 5px 0; }}
            .detail-label {{ font-weight: bold; color: #2563eb; }}
            .action-buttons {{ text-align: center; margin: 20px 0; }}
            .btn {{ display: inline-block; padding: 10px 20px; margin: 5px; border-radius: 5px; text-decoration: none; }}
            .btn-primary {{ background: #2563eb; color: white; }}
            .btn-warning {{ background: #f59e0b; color: white; }}
            .footer {{ background: #f3f4f6; padding: 15px; text-align: center; font-size: 12px; color: #666; border-radius: 0 0 5px 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🔒 Security Alert</h2>
            </div>
            <div class="content">
    """
    
    footer = """
            </div>
            <div class="footer">
                <p>This is an automated security alert. If this wasn't you, please secure your account immediately.</p>
                <p>&copy; 2026 Security System | All rights reserved</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Build alert-specific content
    if alert_type == "failed_login":
        content = f"""
                <h3>⚠️ Failed Login Attempt</h3>
                <div class="alert-box alert-warning">
                    <p>A login attempt was made on your account with an incorrect password.</p>
                    <div class="details">
                        <div class="detail-item">
                            <span class="detail-label">Username:</span> {username}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">IP Address:</span> {ip_address}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Time:</span> {timestamp}
                        </div>
                    </div>
                    <p><strong>If this was you:</strong> No action needed.</p>
                    <p><strong>If this wasn't you:</strong> Your account may be under attack. Change your password immediately.</p>
                </div>
        """
        
    elif alert_type == "account_locked":
        content = f"""
                <h3>🔐 Account Locked</h3>
                <div class="alert-box alert-danger">
                    <p>Your account has been locked after multiple failed login attempts.</p>
                    <div class="details">
                        <div class="detail-item">
                            <span class="detail-label">Username:</span> {username}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">IP Address:</span> {ip_address}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Time:</span> {timestamp}
                        </div>
                    </div>
                    <p style="color: #991b1b; font-weight: bold;">Your account is now locked for security.</p>
                    <div class="action-buttons">
                        <a href="http://localhost:5000/unlock-account" class="btn btn-warning">🔓 Unlock Your Account</a>
                    </div>
                    <p>You can unlock your account by answering your security question and entering a verification code.</p>
                </div>
        """
        
    elif alert_type == "account_unlocked":
        content = f"""
                <h3>✅ Account Unlocked</h3>
                <div class="alert-box alert-success">
                    <p>Your account has been successfully unlocked!</p>
                    <div class="details">
                        <div class="detail-item">
                            <span class="detail-label">Username:</span> {username}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Time:</span> {timestamp}
                        </div>
                    </div>
                    <p>You can now log in to your account with your credentials.</p>
                    <div class="action-buttons">
                        <a href="http://localhost:5000/login" class="btn btn-primary">📝 Login to Your Account</a>
                    </div>
                </div>
        """
        
    elif alert_type == "password_reset":
        content = f"""
                <h3>🔑 Password Reset</h3>
                <div class="alert-box alert-success">
                    <p>Your password has been successfully reset!</p>
                    <div class="details">
                        <div class="detail-item">
                            <span class="detail-label">Username:</span> {username}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Time:</span> {timestamp}
                        </div>
                    </div>
                    <p>Please log in with your new password.</p>
                    <div class="action-buttons">
                        <a href="http://localhost:5000/login" class="btn btn-primary">📝 Login with New Password</a>
                    </div>
                </div>
        """
    
    else:
        content = f"""
                <h3>Security Alert</h3>
                <div class="alert-box alert-warning">
                    <p>A security event has occurred on your account:</p>
                    <div class="details">
                        <div class="detail-item">
                            <span class="detail-label">Event:</span> {alert_type}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">IP Address:</span> {ip_address}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Time:</span> {timestamp}
                        </div>
                    </div>
                </div>
        """
    
    return header + content + footer


def send_welcome_email(user_email, username):
    """
    Send welcome email to new users
    """
    try:
        sender_email = os.getenv('MAIL_SENDER_EMAIL', os.getenv('MAIL_USERNAME', 'noreply@security.com'))
        sender_name = os.getenv('MAIL_SENDER_NAME', 'Security System')
        
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2563eb; color: white; padding: 20px; border-radius: 5px; text-align: center; }}
                .content {{ background: #f9fafb; padding: 20px; margin: 15px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Welcome to Security System! 🔒</h2>
                </div>
                <div class="content">
                    <h3>Welcome, {username}!</h3>
                    <p>Your account has been created successfully.</p>
                    <p>Your account is now protected by our advanced security features including:</p>
                    <ul>
                        <li>🔐 Brute force attack protection</li>
                        <li>🔒 Automatic account lockout after failed attempts</li>
                        <li>✅ CAPTCHA verification</li>
                        <li>📍 IP address logging</li>
                        <li>🚨 Real-time security alerts</li>
                    </ul>
                    <p>Login to your dashboard: <a href="http://localhost:5000/login">Login Here</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject="Welcome to Security System",
            recipients=[user_email],
            html=body,
            sender=(sender_name, sender_email)
        )
        
        mail.send(msg)
        logger.info(f"Welcome email sent to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
        return False


def send_otp_email(user_email, otp_code, username="User"):
    """
    Send OTP (One-Time Password) verification code via email
    
    Args:
        user_email: User's email address
        otp_code: The OTP verification code
        username: User's username for personalization
    """
    try:
        sender_email = os.getenv('MAIL_SENDER_EMAIL', os.getenv('MAIL_USERNAME', 'noreply@security.com'))
        sender_name = os.getenv('MAIL_SENDER_NAME', 'Security System')
        
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f3f4f6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .card {{ background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .header h2 {{ margin: 0; font-size: 24px; }}
                .content {{ padding: 30px; }}
                .otp-box {{ 
                    background: #f0f4ff; 
                    border: 2px solid #667eea; 
                    border-radius: 8px; 
                    padding: 20px; 
                    text-align: center; 
                    margin: 20px 0;
                }}
                .otp-code {{ 
                    font-size: 32px; 
                    font-weight: bold; 
                    letter-spacing: 5px; 
                    color: #667eea;
                    font-family: monospace;
                }}
                .otp-expiry {{ 
                    color: #ef4444; 
                    font-size: 14px; 
                    margin-top: 10px;
                    font-weight: bold;
                }}
                .info-text {{ color: #666; font-size: 14px; line-height: 1.6; }}
                .warning {{ 
                    background: #fef3c7; 
                    border: 1px solid #f59e0b; 
                    border-radius: 5px; 
                    padding: 12px; 
                    margin: 15px 0;
                    color: #78350f;
                }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #e5e7eb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <div class="header">
                        <h2>🔐 Your Verification Code</h2>
                    </div>
                    <div class="content">
                        <p class="info-text">Hi {username},</p>
                        <p class="info-text">You requested to unlock your account. Use the verification code below to complete the process:</p>
                        
                        <div class="otp-box">
                            <div class="otp-code">{otp_code}</div>
                            <div class="otp-expiry">⏱️ Valid for 15 minutes</div>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important Security Note:</strong> Never share this code with anyone. Our staff will never ask for this code.
                        </div>
                        
                        <p class="info-text">If you did not request this code, you can safely ignore this email. Your account remains secure.</p>
                    </div>
                    <div class="footer">
                        <p>&copy; 2026 Security System | All rights reserved</p>
                        <p>If you need help, contact our support team</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject="🔐 Your Account Unlock Verification Code",
            recipients=[user_email],
            html=body,
            sender=(sender_name, sender_email)
        )
        
        mail.send(msg)
        logger.info(f"OTP email sent to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email to {user_email}: {str(e)}")
        return False

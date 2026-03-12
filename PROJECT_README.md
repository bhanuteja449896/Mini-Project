# Brute Force Attack Simulation and Prevention System

A comprehensive web-based security system that demonstrates brute force attack protection mechanisms using Flask and Python.

## 🔒 Features

### Security Features
1. **User Authentication**: Secure login system with password hashing
2. **Account Lockout**: Automatic account locking after 3 failed login attempts
3. **CAPTCHA Verification**: One or more random math CAPTCHA challenges appear after 2 failed attempts to prevent automated attacks
4. **IP Address Logging**: All login attempts are logged with IP addresses for security monitoring
5. **Security Alerts**: Real-time alerts for suspicious activities
6. **Password Recovery**: Forgot password feature with security question verification
7. **Account Unlock**: Multi-step account unlock process with verification
8. **Rate Limiting**: Limited number of login attempts to prevent brute force attacks
9. **Login Attempt Tracking**: Complete history of all login attempts

### User Features
- User Registration with security questions
- Secure Dashboard showing:
  - Account status
  - Failed login attempts
  - Security alerts
  - Login history
- Admin Panel to monitor all users and activities

## 🛠️ Technologies Used

- **Python 3.x** - Main programming language
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database for storing user data
- **Flask-Login** - User session management
- **Werkzeug** - Password hashing and security
- **HTML5 & CSS3** - Frontend design
- **Font Awesome** - Icons

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd /workspaces/Mini-Project
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## 📖 Usage Guide

### For Users

#### 1. Registration
- Click "Register Now" on the login page
- Fill in all required fields:
  - Username
  - Email
  - Password
  - Security Question and Answer (for account recovery)
  - Phone Number (optional)
- Click "Register"

#### 2. Login
- Enter your username and password
- If you fail 2 attempts, one or more random CAPTCHAs will appear
- After 3 failed attempts, your account will be locked

#### 3. Dashboard
- View your account status
- Check failed login attempts
- Read security alerts
- View login history with IP addresses

#### 4. Forgot Password
- Click "Forgot Password?" on login page
- Follow the 3-step process:
  1. Enter your email
  2. Answer your security question
  3. Set a new password

#### 5. Unlock Account
- If your account is locked, click "Unlock Account"
- Follow the verification process:
  1. Enter your email
  2. Answer your security question
  3. Enter the verification code (displayed on screen)

### For Administrators

#### Admin Panel
- Access the admin panel at: `http://localhost:5000/admin`
- View all registered users
- Monitor account statuses (Active/Locked)
- Track all login attempts across the system
- View statistics on users and security

## 🔐 Security Mechanisms

### Brute Force Prevention
1. **Maximum 3 login attempts** before account lockout
2. **CAPTCHA** requirement after 2 failed attempts (multiple random questions may be shown)
3. **IP address logging** for all attempts
4. **Automatic alerts** for suspicious activities

### Password Security
- Passwords are hashed using **Werkzeug's scrypt** algorithm
- Security answers are also hashed
- No plain text credentials stored in database

### Account Recovery
- Multi-step verification process
- Security questions
- Verification codes (in production, sent via SMS/Email)

## 📊 Database Schema

### Users Table
- id, username, email, password_hash
- security_question, security_answer_hash
- is_locked, failed_attempts
- last_login, created_at

### LoginAttempts Table
- id, user_id, ip_address, user_agent
- success (boolean)
- timestamp

### Alerts Table
- id, user_id, message, alert_type
- ip_address, is_read
- created_at

### UnlockRequests Table
- id, user_id, verification_code
- ip_address, is_used
- created_at, expires_at

## 🧪 Testing the System

### Test Brute Force Protection
1. Register a new account
2. Try to login with wrong password 3 times
3. Observe:
   - CAPTCHA appears after 2 attempts
   - Account locks after 3 attempts
   - Alerts are generated
   - IP address is logged

### Test Account Recovery
1. Lock an account (3 failed attempts)
2. Use "Unlock Account" feature
3. Verify with security question
4. Enter verification code
5. Account should be unlocked

### Test Password Reset
1. Click "Forgot Password"
2. Follow the recovery process
3. New password should work

## 📁 Project Structure

```
Mini-Project/
├── main.py                 # Main Flask application
├── models.py               # Database models
├── requirements.txt        # Python dependencies
├── devserver.sh           # Development server script
├── README.md              # This file
├── security_system.db     # SQLite database (created on first run)
└── src/
    ├── templates/         # HTML templates
    │   ├── base.html
    │   ├── login.html
    │   ├── register.html
    │   ├── dashboard.html
    │   ├── forgot_password.html
    │   ├── unlock_account.html
    │   ├── account_locked.html
    │   └── admin.html
    └── static/            # Static files
        └── css/
            └── style.css  # Stylesheet
```

## 🔄 Workflow Diagram

```
User Registration → Account Created
         ↓
Login Attempt → Success → Dashboard
         ↓
    Failure → Increment Failed Attempts
         ↓
   2 Failures → Show CAPTCHA
         ↓
   3 Failures → Lock Account → Send Alert
         ↓
Unlock Account → Verify Identity → Account Unlocked
```

## 🎯 Key Features Demonstration

### Feature 1: Account Lockout
- System monitors login attempts
- Locks account after 3 failures
- Sends alert with IP address

### Feature 2: CAPTCHA
- Math-based CAPTCHA with a random number of problems each time
- Appears after 2 failed attempts
- Prevents automated attacks

### Feature 3: IP Logging
- Every login attempt logged
- IP address recorded
- Visible in dashboard and admin panel

### Feature 4: Security Alerts
- Real-time alerts for:
  - Failed login attempts
  - Account lockouts
  - Suspicious activities
- Displayed in user dashboard

### Feature 5: Account Recovery
- Forgot password with security questions
- Account unlock with verification
- Multi-step verification process

## 🛡️ Security Best Practices Implemented

1. ✅ Password hashing (scrypt algorithm)
2. ✅ Session management with Flask-Login
3. ✅ CSRF protection (Flask built-in)
4. ✅ SQL injection prevention (SQLAlchemy ORM)
5. ✅ Rate limiting on login attempts
6. ✅ Secure session cookies
7. ✅ IP address logging
8. ✅ Account lockout mechanism
9. ✅ CAPTCHA verification
10. ✅ Security alerts system

## 📝 Notes

- This is a **demonstration system** for educational purposes
- In production, add:
  - Email/SMS integration for verification codes
  - Face recognition feature (placeholder in current version)
  - More sophisticated CAPTCHA (reCAPTCHA)
  - Rate limiting middleware
  - HTTPS enforcement
  - Session timeout
  - Two-factor authentication

## 🤝 Contributing

This is a mini project for educational purposes. Feel free to:
- Add more security features
- Improve the UI/UX
- Add more verification methods
- Implement email/SMS integration

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as a Mini Project for Brute Force Attack Simulation and Prevention

## 🎓 Learning Outcomes

By studying this project, you will learn:
1. How brute force attacks work
2. Prevention mechanisms against such attacks
3. User authentication best practices
4. Security alert systems
5. IP address logging and tracking
6. Account recovery mechanisms
7. CAPTCHA implementation
8. Flask web application development
9. Database design for security systems
10. Frontend security UI/UX design

---

**Remember**: Security is not a feature, it's a continuous process! 🔒

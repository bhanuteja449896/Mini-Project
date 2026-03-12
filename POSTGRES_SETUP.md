# 🚀 PostgreSQL + Email Integration Setup Guide

## ✅ What's Been Updated

### 1. **Database Migration: SQLite → PostgreSQL**
- Changed from SQLite to Neon PostgreSQL
- Connection string stored in `.env`
- All tables will be created automatically on first run

### 2. **Email Alerts System**
- Welcome email on registration
- Failed login attempt alerts
- Account locked alerts
- Account unlocked alerts
- Password reset alerts
- Beautiful HTML email templates

### 3. **Environment Configuration**
- All secrets in `.env` file (excluded from git)
- Database URL
- Email configuration
- Flask settings
- Security parameters

---

## 📋 Setup Instructions

### Step 1: Install New Dependencies

```bash
pip install -r requirements.txt
```

**New packages added:**
- `psycopg2-binary` - PostgreSQL driver
- `Flask-Mail` - Email sending
- `python-dotenv` - Environment variable management

### Step 2: Verify `.env` File

Check that `.env` file exists with these values:

```
DATABASE_URL=postgresql://neondb_owner:npg_dHaQZlA2Ok9p@ep-purple-sun-ad2g4gu5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

✅ Database configuration is **already filled**

❌ **Email configuration** (you can fill these later):
```
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-specific-password
```

### Step 3: Test Database Connection

Before running the app, test if PostgreSQL is working:

```bash
python test_db_connection.py
```

Expected output:
```
🔌 Testing PostgreSQL Connection...
============================================================
📍 Connecting to database...
✅ PostgreSQL Connection: SUCCESS
============================================================
```

If this fails, check:
- Internet connection is stable
- DATABASE_URL is correct in `.env`
- Neon database is active and not suspended

### Step 4: Run the Application

```bash
python main.py
```

Expected output:
```
Database initialized successfully!
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

---

## 📧 Email Configuration (For Later)

### Option 1: Using Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select: "Mail" and "Windows Computer"
   - Generate a 16-character password
   - Copy this password

3. **Update `.env` file:**
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx  (the 16-char password)
   ```

### Option 2: Using Other SMTP Servers

Update `.env` with your provider's SMTP details:
```
MAIL_SERVER=smtp.provider.com
MAIL_PORT=587
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
```

### When Email is Configured

**Alerts will be sent for:**
- ✅ Failed login attempts
- ✅ Account lockout
- ✅ Account unlock
- ✅ Password reset
- ✅ Welcome email on registration

---

## 🗄️ Database Features

### Automatic Table Creation

On first run, these tables are created automatically:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    ... security fields ...
)

CREATE TABLE login_attempts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    ip_address VARCHAR(45) NOT NULL,
    success BOOLEAN,
    timestamp DATETIME,
    ... other fields ...
)

CREATE TABLE alerts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    message TEXT NOT NULL,
    alert_type VARCHAR(50),
    ip_address VARCHAR(45),
    is_read BOOLEAN,
    created_at DATETIME
)

CREATE TABLE unlock_requests (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    verification_code VARCHAR(6),
    ip_address VARCHAR(45),
    is_used BOOLEAN,
    created_at DATETIME,
    expires_at DATETIME
)
```

### Query Data from PostgreSQL

Connect to your Neon database:

```bash
psql postgresql://neondb_owner:npg_dHaQZlA2Ok9p@ep-purple-sun-ad2g4gu5-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
```

Common queries:

```sql
-- View all users
SELECT id, username, email, is_locked, failed_attempts FROM users;

-- View login attempts
SELECT * FROM login_attempts ORDER BY timestamp DESC LIMIT 50;

-- View alerts for specific user
SELECT * FROM alerts WHERE user_id = 1 ORDER BY created_at DESC;

-- Check unlock requests
SELECT * FROM unlock_requests WHERE is_used = false;
```

---

## 🔒 Security Configuration in `.env`

```
MAX_LOGIN_ATTEMPTS=3          # Lockout after 3 failures
CAPTCHA_AFTER_ATTEMPTS=2      # CAPTCHA after 2 failures
UNLOCK_TOKEN_EXPIRY=15        # Verification code valid for 15 minutes
```

Change these values to test different scenarios.

---

## 📊 Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |
| `FLASK_ENV` | Environment mode | `development` |
| `SECRET_KEY` | Session encryption | `your-secret-key` |
| `MAIL_SERVER` | SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USE_TLS` | Use TLS encryption | `True` |
| `MAIL_USERNAME` | Email account | `user@gmail.com` |
| `MAIL_PASSWORD` | Email password | `app-password` |
| `MAIL_SENDER_EMAIL` | From address (defaults to your MAIL_USERNAME if not set) | `your-gmail-email@gmail.com` |
| `MAIL_SENDER_NAME` | From name | `Security Alert` |

---

## 🧪 Testing Workflow

### 1. Test Database (No Email)

- Register account
- Check tables in Neon database
- Verify alerts are created in `alerts` table
- ✅ Database writes are working

### 2. Test with Email

- Update `MAIL_USERNAME` and `MAIL_PASSWORD` in `.env`
- Restart the app
- Register new account
  - ✅ Should receive welcome email
- Try failed login 3 times
  - ✅ Should receive failed attempt emails
  - ✅ Should receive account locked email
- Unlock account
  - ✅ Should receive account unlocked email

---

## 🐛 Troubleshooting

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "No module named 'Flask-Mail'"
```bash
pip install Flask-Mail
```

### Error: "DATABASE_URL not found"
- Check `.env` file exists in project root
- Verify DATABASE_URL is set correctly
- Restart the application

### Error: "SMTP Authentication Failed"
- Verify MAIL_USERNAME and MAIL_PASSWORD
- Check if 2FA is enabled on Gmail
- Generate new App Password
- Wait a minute after changing .env (Flask might cache it)

### PostgreSQL Connection Fails
```bash
python test_db_connection.py
```

Check:
- Internet connection
- Neon database is active
- DATABASE_URL is not expired
- No firewall blocking PostgreSQL

---

## 📝 Important Notes

### About Credentials in `.env`

✅ **SAFE:**
- `.env` is in `.gitignore` and never committed to git
- Only you see these credentials
- Different for development/production

⚠️ **IMPORTANT FOR PRODUCTION:**
- Use **different** database credentials
- Use **secure** SMTP or email service
- Store secrets in environment variables, not `.env`
- Use environment-specific .env files

### Email Templates

Email templates are generated dynamically in `email_service.py`:
- Beautiful HTML designs
- Color-coded by alert type
- Includes security information
- Links back to account

---

## 🚀 Quick Start Command

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test database (optional but recommended)
python test_db_connection.py

# 3. Run the app
python main.py

# 4. Open browser
# http://localhost:5000
```

---

## 📞 Support

If you encounter issues:

1. Check `.env` file exists
2. Run `python test_db_connection.py`
3. Check Flask error logs in terminal
4. Verify internet connection
5. Check if database credentials are correct

---

## 🎯 Next Steps

1. ✅ Install requirements
2. ✅ Test database connection
3. ✅ Run the application
4. 🔲 (Later) Configure email settings in `.env`
5. 🔲 (Later) Test email alerts
6. 🔲 (Later) Deploy to production with different credentials

---

**Your system is now ready for PostgreSQL database storage and email alerts!** 🎉

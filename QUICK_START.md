# 🚀 QUICK START GUIDE

## Your Brute Force Protection System is READY!

### ✅ Application Status
- **Status**: Running Successfully
- **URL**: http://localhost:5000
- **Database**: Created (security_system.db)

---

## 🎯 How to Test the System

### 1. Open the Application
Open your web browser and go to:
```
http://localhost:5000
```

You'll be automatically redirected to the login page.

---

### 2. Register a New Account

**Step-by-step:**
1. Click **"Register Now"** button
2. Fill in the registration form:
   - **Username**: testuser
   - **Email**: testuser@example.com
   - **Password**: Test@123
   - **Confirm Password**: Test@123
   - **Phone Number**: +1234567890 (optional)
   - **Security Question**: Select any question
   - **Security Answer**: Enter an answer (remember this!)
3. Click **"Register"**

✅ You should see: "Registration successful! Please login."

---

### 3. Test Normal Login

1. Enter your username and password
2. Click **"Login"**

✅ You should be redirected to the **Dashboard**

**Dashboard Features:**
- Account status (Active/Locked)
- Failed login attempts counter
- Unread security alerts
- Recent login history with IP addresses
- Security tips

---

### 4. Test Brute Force Protection 🔒

**This is the MAIN FEATURE - Let's test it!**

1. **Logout** from your account
2. Try to login with **WRONG password** (attempt 1)
   - You'll see: "Invalid username or password! 2 attempts remaining."

3. Try again with **WRONG password** (attempt 2)
   - You'll see: "Invalid username or password! 1 attempts remaining."
   - **CAPTCHA appears!** (One or more math questions, e.g., "What is 5 + 3?" and "What is 2 * 4?")

4. Answer the CAPTCHA and try **WRONG password** again (attempt 3)
   - 🔒 **ACCOUNT LOCKED!**
   - You'll see the **Account Locked** page

**What Happened:**
- ✅ Account locked after 3 failed attempts
- ✅ One or more randomized CAPTCHAs shown after 2 attempts
- ✅ IP address logged
- ✅ Security alerts created

---

### 5. View Security Alerts

Before unlocking, let's check alerts:
1. Login with **correct password** (if you have another account)
2. Go to Dashboard
3. View **"Unread Security Alerts"** section
4. You'll see alerts about:
   - Failed login attempts
   - Account lockout
   - IP addresses of attempts

---

### 6. Test Account Unlock Feature 🔓

**From the Account Locked page:**

1. Click **"Unlock Account"** option

2. **Step 1**: Enter your email
   - Enter: testuser@example.com
   - Click "Continue"

3. **Step 2**: Answer security question
   - Enter your security answer
   - Click "Verify"

4. **Step 3**: Enter verification code
   - A 6-digit code will be displayed (in production, sent via SMS/Email)
   - Copy and enter the code
   - Click "Unlock Account"

✅ **Success!** Account is now unlocked!

**What Happened:**
- ✅ Identity verified using security question
- ✅ Verification code generated
- ✅ Failed attempts counter reset
- ✅ Alert created for account unlock

---

### 7. Test Password Reset Feature 🔑

1. Go to login page
2. Click **"Forgot Password?"**

3. **Step 1**: Enter your email
4. **Step 2**: Answer your security question
5. **Step 3**: Set new password

✅ Password reset successful!

---

### 8. View Admin Panel (Monitor All Users) 👨‍💼

Access the admin panel:
```
http://localhost:5000/admin
```

**Admin Panel Shows:**
- All registered users
- Account statuses (Active/Locked)
- Failed attempt counts
- Last login times
- All login attempts (all users)
- IP addresses and timestamps
- User agent information
- Overall statistics

---

## 📊 What to Look For (Demonstrating Features)

### Feature 1: Brute Force Prevention ✅
- After 3 wrong passwords → Account locked
- Maximum attempts enforced
- Cannot login even with correct password when locked

### Feature 2: CAPTCHA ✅
- Appears after 2 failed attempts
- Must solve math problem
- Prevents automated attacks

### Feature 3: IP Address Logging ✅
- Every login attempt logged
- IP address recorded
- Visible in dashboard and admin panel

### Feature 4: Security Alerts ✅
- Failed login attempts generate alerts
- Account lockout creates alert
- Alerts show IP addresses
- Mark alerts as read

### Feature 5: Account Recovery ✅
- Forgot password with security questions
- Account unlock with verification
- Identity verification required

### Feature 6: Rate Limiting ✅
- Only 3 attempts allowed
- Account automatically locked
- Manual unlock required

---

## 🎨 Pages You Can Explore

1. **Login Page** - `/login`
2. **Register Page** - `/register`
3. **Dashboard** - `/dashboard` (requires login)
4. **Forgot Password** - `/forgot-password`
5. **Unlock Account** - `/unlock-account`
6. **Admin Panel** - `/admin` (requires login)

---

## 🔍 Database Contents

The system created a SQLite database: `security_system.db`

**Tables:**
- `users` - User accounts and security info
- `login_attempts` - All login attempts with IP addresses
- `alerts` - Security alerts for users
- `unlock_requests` - Account unlock requests

You can inspect the database using:
```bash
sqlite3 security_system.db
.tables
SELECT * FROM users;
SELECT * FROM login_attempts;
```

---

## 💡 Testing Scenarios

### Scenario 1: Multiple Failed Attempts
1. Try wrong password 3 times
2. Observe CAPTCHA after attempt 2
3. Account locks after attempt 3
4. Check dashboard for alerts

### Scenario 2: Unlock After Lockout
1. Lock account (3 wrong passwords)
2. Use unlock feature
3. Answer security question
4. Enter verification code
5. Login successfully

### Scenario 3: Password Reset
1. Go to forgot password
2. Complete verification
3. Set new password
4. Login with new password

### Scenario 4: Monitor from Admin
1. Create multiple accounts
2. Make some failed attempts
3. Lock some accounts
4. View everything in admin panel

---

## 🛑 To Stop the Server

Press `Ctrl + C` in the terminal where the server is running

---

## 📝 Key Configuration

In `main.py`:
```python
MAX_LOGIN_ATTEMPTS = 3           # Lockout after 3 failures
CAPTCHA_AFTER_ATTEMPTS = 2       # Show CAPTCHA after 2 failures
```

You can modify these values to test different scenarios!

---

## 🎓 Project Features Summary

✅ User registration with security questions
✅ Secure login with password hashing
✅ Brute force attack prevention
✅ Account lockout after max attempts
✅ CAPTCHA verification
✅ IP address logging
✅ Security alerts system
✅ Account recovery (forgot password)
✅ Account unlock with verification
✅ User dashboard with statistics
✅ Admin panel for monitoring
✅ Beautiful responsive UI

---

## 📚 Next Steps

1. Test all features mentioned above
2. Create multiple user accounts
3. Test the brute force protection
4. Check the admin panel
5. Review the security alerts
6. Inspect the database
7. Customize the configuration

---

## 🎉 Congratulations!

Your **Brute Force Attack Simulation and Prevention System** is fully functional!

All features are working:
- ✅ Attack simulation
- ✅ Prevention mechanisms
- ✅ Monitoring and logging
- ✅ User security features
- ✅ Admin capabilities

**Enjoy testing and learning about security! 🔒**

./venv/bin/python rss_checker.py

## Multi-user Setup

Owner must run first to create db with correct permissions:
```
chmod 777 /path/to/serverdemo
./venv/bin/python rss_checker.py
```

Other users can then run normally. Only the owner can change db permissions - this is a Linux limitation, not a bug.

## Gmail App Password Setup (for send_email.py)

### Step 1: Enable 2-Step Verification
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Under "How you sign in to Google", click **2-Step Verification**
3. Follow prompts to enable with your phone number

### Step 2: Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords) (requires 2-Step Verification)
2. Enter a custom name (e.g., "Python Email Script")
3. Click **Create**
4. Copy the 16-character password shown (you won't see it again)

### Step 3: Use in Script
Replace `your_app_password` in `send_email.py` with the 16-character password (no spaces).

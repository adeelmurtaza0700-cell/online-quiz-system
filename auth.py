import random
from email_validator import validate_email, EmailNotValidError
from database import get_conn

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email):
    otp = generate_otp()
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT id FROM users WHERE email=?", (email,))
    user = c.fetchone()

    if user:
        c.execute("UPDATE users SET otp=? WHERE email=?", (otp, email))
    else:
        c.execute("INSERT INTO users (email, otp, role) VALUES (?, ?, ?)", (email, otp, "student"))

    conn.commit()
    return otp  # In real system you send via SMTP — here we display it.

def verify_otp(email, otp):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, role FROM users WHERE email=? AND otp=?", (email, otp))
    return c.fetchone()

import bcrypt
from database import execute_query, fetch_one

# --- Register User ---
def register_user(name, email, password, role):
    # Check if email already exists
    existing_user = fetch_one("SELECT * FROM users WHERE email=%s", (email,))
    if existing_user:
        return False, "Email already registered. Try logging in."

    # Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        execute_query(
            "INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s)",
            (name, email, hashed, role)
        )
        return True, "User registered successfully!"
    except Exception as e:
        return False, f"Database error: {str(e)}"

# --- Login User ---
def login_user(email, password):
    user = fetch_one("SELECT * FROM users WHERE email=%s", (email,))
    if not user:
        return None, "Email not found. Please register."

    if bcrypt.checkpw(password.encode(), user['password'].encode()):
        return user, "Login successful!"
    else:
        return None, "Incorrect password."

# --- Update User ---
def update_user(user_id, name=None, email=None, password=None):
    # Hash new password if provided
    if password:
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    execute_query(
        "UPDATE users SET name=COALESCE(%s,name), email=COALESCE(%s,email), password=COALESCE(%s,password) WHERE id=%s",
        (name, email, password, user_id)
    )

# --- Delete User ---
def delete_user(user_id):
    execute_query("DELETE FROM users WHERE id=%s", (user_id,))

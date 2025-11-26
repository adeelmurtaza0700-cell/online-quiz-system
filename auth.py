import bcrypt
from database import execute_query, fetch_one

def register_user(name,email,password,role):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        execute_query(
            "INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s)",
            (name,email,hashed,role)
        )
        return True
    except:
        return False

def login_user(email,password):
    user = fetch_one("SELECT * FROM users WHERE email=%s",(email,))
    if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
        return user
    return None

def update_user(user_id,name=None,email=None,password=None):
    if password:
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    execute_query(
        "UPDATE users SET name=COALESCE(%s,name), email=COALESCE(%s,email), password=COALESCE(%s,password) WHERE id=%s",
        (name,email,password,user_id)
    )

def delete_user(user_id):
    execute_query("DELETE FROM users WHERE id=%s",(user_id,))

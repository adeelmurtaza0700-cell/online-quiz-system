import bcrypt
from database import create_user, get_user

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def signup(username, password, role):
    hashed = hash_password(password).decode()
    return create_user(username, hashed, role)

def login(username, password):
    res = get_user(username)
    if res.data:
        user = res.data[0]
        if verify_password(password, user['password'].encode()):
            return user
    return None

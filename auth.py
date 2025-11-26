import streamlit as st
from database import SessionLocal, User
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(name, email, password, role="student"):
    db = SessionLocal()
    hashed = hash_password(password)
    user = User(name=name, email=email, password=hashed, role=role)
    db.add(user)
    db.commit()
    db.close()

def login_user(email, password):
    db = SessionLocal()
    user = db.query(User).filter(User.email==email).first()
    db.close()
    if user and verify_password(password, user.password):
        return user
    return None

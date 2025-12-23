"""
Authentication service for nihaal_price_tracker
"""
import sqlite3
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "price_tracker.db"

def add_user(username: str, password: str) -> bool:
    """Add a new user with hashed password."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        hashed_pw = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username: str, password: str) -> Optional[int]:
    """Authenticate user and return user id if valid."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[1], password):
        return user[0]
    return None

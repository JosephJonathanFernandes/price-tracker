"""
Product management service for nihaal_price_tracker
"""
import sqlite3
from typing import List, Tuple

DB_NAME = "price_tracker.db"

def add_product(user_id: int, url: str, target_price: float) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO products (user_id, url, target_price) VALUES (?, ?, ?)", (user_id, url, target_price))
    conn.commit()
    conn.close()

def get_products(user_id: int) -> List[Tuple[int, str, float]]:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, url, target_price FROM products WHERE user_id=?", (user_id,))
    products = c.fetchall()
    conn.close()
    return products

def remove_product(product_id: int) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

"""
Streamlit UI entrypoint for nihaal_price_tracker
"""
import streamlit as st
from fake_useragent import UserAgent
from src.db.db_init import init_db
from src.auth.auth_service import add_user, authenticate_user
from src.products.product_service import add_product, get_products, remove_product
from src.products.price_fetcher import fetch_price
from src.notifications.email_service import send_mail
from src.notifications.sms_service import send_sms
import matplotlib.pyplot as plt
import io
import requests
from bs4 import BeautifulSoup
from src.config.settings import *

init_db()

st.title("Flipkart Price Tracker")

# Authentication
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

auth_mode = st.sidebar.radio("Authentication", ["Login", "Sign Up"])
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if auth_mode == "Sign Up":
    if st.sidebar.button("Sign Up"):
        if add_user(username, password):
            st.sidebar.success("User registered. Please log in.")
        else:
            st.sidebar.error("Username already exists.")
elif auth_mode == "Login":
    if st.sidebar.button("Login"):
        user_id = authenticate_user(username, password)
        if user_id:
            st.session_state["user_id"] = user_id
            st.sidebar.success("Logged in!")
        else:
            st.sidebar.error("Invalid credentials.")

# Main app for logged-in users
if st.session_state["user_id"]:
    st.subheader(f"Welcome, {username}!")
    st.text("Add a product to track:")
    url = st.text_input("Product URL")
    target_price = st.number_input("Target Price", min_value=0.0, step=1.0)
    if st.button("Add Product"):
        if url and target_price:
            add_product(st.session_state["user_id"], url, target_price)
            st.success("Product added!")
        else:
            st.warning("Please enter both URL and target price.")

    st.subheader("Your Tracked Products")
    products = get_products(st.session_state["user_id"])

    # Simple in-memory price history
    if "price_history" not in st.session_state:
        st.session_state["price_history"] = {}

    for pid, purl, pprice in products:
        st.write(f"URL: {purl}")
        st.write(f"Target Price: {pprice}")
        ua = UserAgent()
        headers = {"User-Agent": ua.random}
        if st.button(f"Check Price for {purl}"):
            with st.spinner("Fetching price..."):
                try:
                    title, price = fetch_price(purl, headers)
                    st.write(f"Product name: {title}")
                    st.write(f"Current price: {price}")
                    # Try to fetch product image
                    response = requests.get(purl, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    img_url = None
                    img_tag = soup.find('img')
                    if img_tag and img_tag.get('src'):
                        img_url = img_tag['src']
                    if img_url:
                        st.image(img_url, caption=title, use_column_width=True)
                    # Update price history
                    if pid not in st.session_state["price_history"]:
                        st.session_state["price_history"][pid] = []
                    st.session_state["price_history"][pid].append(price)
                    # Show price history chart
                    if len(st.session_state["price_history"][pid]) > 1:
                        fig, ax = plt.subplots()
                        ax.plot(st.session_state["price_history"][pid], marker='o')
                        ax.set_title(f"Price History for {title}")
                        ax.set_xlabel("Check #")
                        ax.set_ylabel("Price (Rs)")
                        buf = io.BytesIO()
                        fig.savefig(buf, format="png")
                        st.image(buf)
                    if price <= pprice:
                        try:
                            # Send email notification to the logged-in user
                            send_mail(purl, title, username)
                            send_sms(f"Price dropped for {title}: {price}Rs\n{purl}")
                            st.success(f"Price dropped to {price}Rs. Email and SMS notification sent.")
                        except Exception as notify_err:
                            st.error(f"Price dropped, but notification failed: {notify_err}")
                    else:
                        st.info(f"Price is {price}Rs. Still higher than target price.")
                except requests.exceptions.RequestException as req_err:
                    st.error(f"Network error: {req_err}")
                except ValueError as val_err:
                    st.error(f"Data error: {val_err}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        if st.button(f"Remove {purl}"):
            remove_product(pid)
            st.success("Product removed.")

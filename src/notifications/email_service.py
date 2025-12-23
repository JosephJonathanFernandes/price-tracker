"""
Email notification service for nihaal_price_tracker
"""
import smtplib
import os
from email.message import EmailMessage

def send_mail(url: str, product_name: str, user_email: str) -> None:
    src_email = os.getenv("EMAIL")
    passwd = os.getenv("EMAIL_PASSWORD")
    if not src_email or not passwd:
        raise ValueError("Email credentials not set in environment variables.")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user=src_email, password=passwd)
    subject = "Hey! The price just dropped"
    body = f"Product: {product_name}\n\nFlipkart link: {url}"
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        from_addr=src_email,
        to_addrs=user_email,
        msg=message
    )
    server.quit()

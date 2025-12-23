"""
SMS notification service for nihaal_price_tracker
"""
import os
from twilio.rest import Client

def send_sms(message: str, to_number: str = None) -> None:
    sid = os.getenv("TWILIO_SID")
    token = os.getenv("TWILIO_TOKEN")
    from_number = os.getenv("TWILIO_NUMBER")
    user_phone = os.getenv("USER_PHONE")
    if not sid or not token or not from_number:
        raise ValueError("Twilio credentials not set in environment variables.")
    client = Client(sid, token)
    to_number = to_number or user_phone
    if not to_number:
        raise ValueError("Recipient phone number not set.")
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )

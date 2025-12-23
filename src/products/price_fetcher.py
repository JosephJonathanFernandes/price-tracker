"""
Price fetching logic for nihaal_price_tracker
"""
import requests
from bs4 import BeautifulSoup
from typing import Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_price(url: str, headers: dict) -> Tuple[str, float]:
    logger.info(f"Fetching price for URL: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Failed to retrieve page, status code {response.status_code}")
        raise Exception(f"Failed to retrieve page, status code {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Title selectors fallback
    title_selectors = [
        {"class": "VU-ZEz"},
        {"class": "B_NuCI"},
        {"class": "yhB1nd"},
    ]
    p_title = None
    for sel in title_selectors:
        el = soup.find(attrs=sel)
        if el:
            p_title = el.get_text(strip=True)
            break
    if not p_title:
        h1 = soup.find("h1")
        p_title = h1.get_text(strip=True) if h1 else soup.title.string if soup.title else "Title not found"

    # Price selectors fallback
    price_selectors = [
        {"class": "Nx9bqj CxhGGd"},
        {"class": "_30jeq3 _16Jk6d"},
        {"class": "_16Jk6d"},
    ]
    p_price = None
    for sel in price_selectors:
        el = soup.find(attrs=sel)
        if el:
            p_price = el.get_text(strip=True)
            break
    if not p_price:
        price_candidates = soup.find_all(text=lambda t: "₹" in t)
        for candidate in price_candidates:
            try:
                price = candidate.replace(",", "").replace("₹", "").strip()
                float(price)
                p_price = price
                break
            except Exception:
                continue
    if not p_price:
        logger.error("Price not found")
        raise Exception("Price not found")

    try:
        final_price = float(p_price)
    except ValueError:
        logger.error("Could not parse price value.")
        raise Exception("Could not parse price value.")

    logger.info(f"Fetched price: {final_price}")
    return p_title, final_price

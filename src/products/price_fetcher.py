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
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        p_title_element = soup.find(attrs={"class": "VU-ZEz"})
        p_title = p_title_element.get_text(strip=True) if p_title_element else "Title not found"
        p_price_element = soup.find(attrs={"class": "Nx9bqj CxhGGd"})
        p_price = p_price_element.get_text(strip=True) if p_price_element else "Price not found"
        p_price = p_price.replace(",", "").replace("\u20b9", "")
        try:
            final_price = float(p_price)
        except ValueError:
            logger.error("Could not parse price value.")
            raise Exception("Could not parse price value.")
        logger.info(f"Fetched price: {final_price}")
        return p_title, final_price
    else:
        logger.error(f"Failed to retrieve page, status code {response.status_code}")
        raise Exception(f"Failed to retrieve page, status code {response.status_code}")

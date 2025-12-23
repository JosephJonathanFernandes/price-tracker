"""
FastAPI layer for nihaal_price_tracker
"""
from fastapi import FastAPI, HTTPException
from src.products.price_fetcher import fetch_price

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/fetch_price")
def api_fetch_price(url: str):
    from fake_useragent import UserAgent
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    try:
        title, price = fetch_price(url, headers)
        return {"title": title, "price": price}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

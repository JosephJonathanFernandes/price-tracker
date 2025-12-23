# Nihaal Price Tracker

![CI](https://github.com/yourusername/nihaal_price_tracker/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![License](https://img.shields.io/github/license/yourusername/nihaal_price_tracker)

## Problem Statement
Track product prices on Flipkart and notify users when prices drop below a target. Designed for security, modularity, and professional open-source standards.

## Architecture
- **Streamlit UI**: User authentication, product management, dashboard
- **src/**: Core logic (auth, products, notifications, db, config)
- **config/**: Environment and settings
- **tests/**: Unit and integration tests
- **docs/**: Architecture, contributing, changelog, security

## Tech Stack
- Python 3.9+
- Streamlit
- SQLite
- Twilio (SMS)
- SMTP (Email)
- Requests, BeautifulSoup
- dotenv, werkzeug (security)

## Setup
1. Clone the repo
2. `cd nihaal_price_tracker`
3. Create `.env` from `.env.example` and fill in credentials
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `streamlit run src/app.py`

## Usage
- Sign up and log in
- Add product URLs and target prices
- Get notified by email/SMS when price drops

## Value
- Modular, secure, and production-ready
- Easy to extend and maintain
- Recruiter- and reviewer-friendly

## Testing
- Run all tests: `python -m unittest discover tests`
- Coverage goal: 90%+

## Linting & Formatting
- Use `flake8` for linting
- Use `black` for formatting
- Recommended: pre-commit hooks

## CI/CD
- See `.github/workflows/ci.yml` for GitHub Actions pipeline example

## Documentation
- See `docs/` for architecture, contributing, changelog, and security policies


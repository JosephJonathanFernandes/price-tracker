# Architecture Overview

## Problem Statement
Track product prices on Flipkart and notify users when prices drop below a target.

## High-Level Architecture
- **Streamlit UI**: User authentication, product management, and dashboard
- **Core Logic (src/)**: Price fetching, notification, business logic
- **Database (SQLite)**: User and product storage
- **Notification**: Email (SMTP) and SMS (Twilio)
- **Configuration**: Environment variables and config files

## Key Modules
- `src/auth/`: Authentication logic
- `src/products/`: Product tracking logic
- `src/notifications/`: Email/SMS notification logic
- `src/db/`: Database access layer

## Data Flow
1. User signs up/logs in
2. Adds product URL and target price
3. System fetches price, stores product, and checks for price drops
4. Notifies user via email/SMS if price drops

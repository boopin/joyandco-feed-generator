# 🛍️ Joy & Co Product Feed Generator

Automated system to generate product feeds for Google Shopping and Meta (Facebook/Instagram) Ads.

## Features
- Scrapes product data from https://joyandco.com/products
- Generates two CSVs: `google_product_feed.csv` and `meta_product_feed.csv`
- Daily auto-updates via GitHub Actions
- Streamlit GUI for manual download and preview

## How to Use
1. Clone the repo
2. Run locally with Streamlit:
```
streamlit run streamlit_app.py
```
3. GitHub Actions will auto-run `auto_scraper.py` every 24 hours
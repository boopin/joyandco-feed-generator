import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re

# === Scraper Logic ===
BASE_URL = "https://joyandco.com"
PRODUCTS_PAGE = f"{BASE_URL}/products"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_all_product_links():
    product_links = set()
    page = 1
    while True:
        url = f"{PRODUCTS_PAGE}?page={page}"
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.select('.product-card a')
        if not items:
            break
        for item in items:
            href = item.get('href')
            if href and '/product/' in href:
                product_links.add(BASE_URL + href)
        page += 1
    return list(product_links)

def scrape_product_page(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        title = soup.select_one('h1.product-title').get_text(strip=True)
        description = soup.select_one('div.product-description').get_text(strip=True)
        price = soup.select_one('span.price').get_text(strip=True)
        image = soup.select_one('img.product-main-image')['src']
        product_id = re.findall(r'-(\\w+)$', url)[0] if '-' in url else url.split('/')[-1]
        return {
            'id': product_id,
            'title': title,
            'description': description,
            'link': url,
            'image_link': image,
            'price': f"{price} AED",
            'availability': 'in stock',
            'brand': 'Joy & Co',
            'condition': 'new',
            'google_product_category': 'Home & Garden > Decor > Candles & Candle Holders',
            'identifier_exists': 'FALSE',
            'gtin': '',
            'mpn': ''
        }
    except Exception as e:
        st.error(f"Error parsing {url}: {e}")
        return None

def run_scraper():
    links = get_all_product_links()
    data = [scrape_product_page(link) for link in links]
    return [d for d in data if d is not None]

# === Streamlit App ===
st.set_page_config(page_title="🛍️ Joy & Co Product Feed Generator")
st.title("🛍️ Product Feed Generator & Viewer")
st.markdown("Click the button below to scrape product data and generate updated feeds:")

if st.button("🚀 Run Scraper Now"):
    with st.spinner("Scraping product pages..."):
        products = run_scraper()

        # Create Google Feed
        df_google = pd.DataFrame(products)[[
            'id', 'title', 'description', 'link', 'image_link', 'price',
            'availability', 'brand', 'condition', 'google_product_category', 'identifier_exists'
        ]]
        st.success("✅ Google Product Feed generated!")
        st.dataframe(df_google)
        st.download_button("⬇️ Download Google Feed", df_google.to_csv(index=False), "google_product_feed.csv")

        # Create Meta Feed
        df_meta = pd.DataFrame(products)[[
            'id', 'title', 'description', 'availability', 'condition', 'price',
            'link', 'image_link', 'brand', 'gtin', 'mpn'
        ]]
        st.success("✅ Meta Product Feed generated!")
        st.dataframe(df_meta)
        st.download_button("⬇️ Download Meta Feed", df_meta.to_csv(index=False), "meta_product_feed.csv")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

BASE_URL = "https://joyandco.com"
PRODUCTS_PAGE = f"{BASE_URL}/products"

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def get_all_product_links():
    product_links = set()
    page = 1
    while True:
        url = f"{PRODUCTS_PAGE}?page={page}"
        res = requests.get(url, headers=headers)
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
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        title = soup.select_one('h1.product-title').get_text(strip=True)
        description = soup.select_one('div.product-description').get_text(strip=True)
        price = soup.select_one('span.price').get_text(strip=True)
        image = soup.select_one('img.product-main-image')['src']
        product_id = re.findall(r'-(\w+)$', url)[0] if '-' in url else url.split('/')[-1]
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
        print(f"Error parsing {url}: {e}")
        return None

def save_csvs(products):
    os.makedirs("feeds", exist_ok=True)
    df_google = pd.DataFrame(products)[[
        'id', 'title', 'description', 'link', 'image_link', 'price',
        'availability', 'brand', 'condition', 'google_product_category', 'identifier_exists']]
    df_google.to_csv("feeds/google_product_feed.csv", index=False)

    df_meta = pd.DataFrame(products)[[
        'id', 'title', 'description', 'availability', 'condition', 'price',
        'link', 'image_link', 'brand', 'gtin', 'mpn']]
    df_meta.to_csv("feeds/meta_product_feed.csv", index=False)

if __name__ == "__main__":
    links = get_all_product_links()
    data = [scrape_product_page(link) for link in links]
    clean_data = [d for d in data if d is not None]
    save_csvs(clean_data)
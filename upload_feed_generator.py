import streamlit as st
import pandas as pd

st.set_page_config(page_title="🛍️ Product Feed Uploader")

st.title("🛍️ Upload Your Product List to Generate Feeds")
st.markdown("""
Upload your exported product CSV file. It should contain at least the following columns:
- `id`
- `title`
- `description`
- `link` (product URL)
- `image_link` (main product image URL)
- `price`
- `stock`
- `brand` (optional)

We'll use this to generate:
- ✅ Google Shopping Feed
- ✅ Meta (Facebook/Instagram) Product Feed
""")

uploaded_file = st.file_uploader("📁 Upload your product CSV file", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    st.success(f"✅ Uploaded {uploaded_file.name} with {len(df)} products")

    required_columns = ["id", "title", "description", "link", "image_link", "price", "stock"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"Missing required columns. Found columns: {list(df.columns)}")
    else:
        df['availability'] = df['stock'].apply(lambda x: 'in stock' if x > 0 else 'out of stock')
        df['brand'] = df.get('brand', 'Joy & Co')
        df['condition'] = 'new'
        df['google_product_category'] = "Home & Garden > Decor > Candles & Candle Holders"
        df['identifier_exists'] = 'FALSE'
        df['gtin'] = ''
        df['mpn'] = ''

        st.subheader("🎯 Google Shopping Feed")
        df_google = df[[
            'id', 'title', 'description', 'link', 'image_link', 'price',
            'availability', 'brand', 'condition', 'google_product_category', 'identifier_exists'
        ]]
        st.dataframe(df_google)
        st.download_button("⬇️ Download Google Feed", df_google.to_csv(index=False), "google_product_feed.csv")

        st.subheader("📦 Meta Product Feed")
        df_meta = df[[
            'id', 'title', 'description', 'availability', 'condition', 'price',
            'link', 'image_link', 'brand', 'gtin', 'mpn'
        ]]
        st.dataframe(df_meta)
        st.download_button("⬇️ Download Meta Feed", df_meta.to_csv(index=False), "meta_product_feed.csv")
import streamlit as st
import pandas as pd

st.set_page_config(page_title="🛍️ Product Feed Generator")

st.title("🛍️ Upload Your Product List to Generate Google & Meta Feeds")
st.markdown("""
Upload your `.xlsx` file exported from the CMS. This app will clean it and generate:
- ✅ Google Shopping Feed
- ✅ Meta (Facebook/Instagram) Product Feed
""")

uploaded_file = st.file_uploader("📁 Upload Excel file (e.g., 'In_house-product-list.xlsx')", type=["xlsx"])

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file, header=None, skiprows=1)

        df = pd.DataFrame({
            'id': df_raw[4],
            'title': df_raw[3],
            'description': df_raw[5],
            'link': '',  # Can be constructed from id or slug if needed
            'image_link': df_raw[2],
            'price': df_raw[12].astype(str).str.replace("AED", "").str.strip() + " AED",
            'stock': df_raw[18].apply(lambda x: 1 if str(x).strip().lower() == "active" else 0),
            'brand': df_raw[10]
        })

        df['availability'] = df['stock'].apply(lambda x: 'in stock' if x > 0 else 'out of stock')
        df['condition'] = 'new'
        df['google_product_category'] = "Home & Garden > Decor > Candles & Candle Holders"
        df['identifier_exists'] = 'FALSE'
        df['gtin'] = ''
        df['mpn'] = ''

        st.success(f"✅ Parsed {len(df)} products from uploaded file")

        # Google Feed
        st.subheader("🎯 Google Shopping Feed")
        df_google = df[[
            'id', 'title', 'description', 'link', 'image_link', 'price',
            'availability', 'brand', 'condition', 'google_product_category', 'identifier_exists'
        ]]
        st.dataframe(df_google)
        st.download_button("⬇️ Download Google Feed", df_google.to_csv(index=False), "google_product_feed.csv")

        # Meta Feed
        st.subheader("📦 Meta Product Feed")
        df_meta = df[[
            'id', 'title', 'description', 'availability', 'condition', 'price',
            'link', 'image_link', 'brand', 'gtin', 'mpn'
        ]]
        st.dataframe(df_meta)
        st.download_button("⬇️ Download Meta Feed", df_meta.to_csv(index=False), "meta_product_feed.csv")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

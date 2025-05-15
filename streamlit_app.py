import streamlit as st
import pandas as pd

st.set_page_config(page_title="🛍️ Joy & Co Product Feed Generator")
st.title("🛍️ Product Feed Viewer")
st.markdown("Use the buttons below to download the latest product feeds.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Google Product Feed")
    try:
        df_google = pd.read_csv("feeds/google_product_feed.csv")
        st.dataframe(df_google)
        st.download_button("⬇️ Download Google Feed", df_google.to_csv(index=False), "google_product_feed.csv")
    except:
        st.warning("Google product feed not found.")

with col2:
    st.subheader("Meta Product Feed")
    try:
        df_meta = pd.read_csv("feeds/meta_product_feed.csv")
        st.dataframe(df_meta)
        st.download_button("⬇️ Download Meta Feed", df_meta.to_csv(index=False), "meta_product_feed.csv")
    except:
        st.warning("Meta product feed not found.")
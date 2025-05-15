# Run Scraper
if st.button("🚀 Run Scraper Now"):
    with st.spinner("Scraping product pages..."):
        products = run_scraper()

        if not products:
            st.error("❌ No products scraped. Check HTML structure or page access.")
        else:
            # Debug preview
            st.write("✅ Scraped data preview:", products[0])

            try:
                df_google = pd.DataFrame(products)[[
                    'id', 'title', 'description', 'link', 'image_link', 'price',
                    'availability', 'brand', 'condition', 'google_product_category', 'identifier_exists'
                ]]
                st.success("✅ Google Product Feed generated!")
                st.dataframe(df_google)
                st.download_button("⬇️ Download Google Feed", df_google.to_csv(index=False), "google_product_feed.csv")
            except KeyError as e:
                st.error(f"Missing column in Google feed generation: {e}")

            try:
                df_meta = pd.DataFrame(products)[[
                    'id', 'title', 'description', 'availability', 'condition', 'price',
                    'link', 'image_link', 'brand', 'gtin', 'mpn'
                ]]
                st.success("✅ Meta Product Feed generated!")
                st.dataframe(df_meta)
                st.download_button("⬇️ Download Meta Feed", df_meta.to_csv(index=False), "meta_product_feed.csv")
            except KeyError as e:
                st.error(f"Missing column in Meta feed generation: {e}")

# 🛍️ Joy & Co Product Feed Generator

This Streamlit app allows you to upload a CSV product export from your eCommerce platform and instantly generate:

- ✅ Google Shopping Feed
- ✅ Meta (Facebook/Instagram) Product Feed

---

## 📦 Features

- Drag & drop CSV or Excel upload
- Auto-generate `google_product_feed.csv`
- Auto-generate `meta_product_feed.csv`
- Download buttons for one-click export

---

## 📁 How to Use

1. **Export** your product list from your CMS or backend.
2. **Upload** the file in the app.
3. **Download** Google and Meta Shopping feed CSVs.

---

## ✅ Required Columns in CSV

Your uploaded file must include at least:

- `id` (unique product ID)
- `title`
- `description`
- `link` (product page URL)
- `image_link` (main image URL)
- `price` (numeric or string)
- `stock` (0 or more)
- `brand` (optional)

> 📄 Use the sample file below to get started.

---

## 🧪 Test File

Use this [sample template CSV](sample_product_upload_template.csv) to test the app or format your own product list.

---

## 🚀 Live App

Deployed on Streamlit Cloud:  
👉 [[https://joyco-feed-generator-v2.streamlit.app](https://joyco-feed-generator-v2.streamlit.app)

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas

---

## ✨ Example Screenshot

![screenshot](https://via.placeholder.com/900x500?text=Product+Feed+Generator+App)

---

## 📥 Contact

Made by [Your Agency / Team Name]  
📧 Email: you@example.com

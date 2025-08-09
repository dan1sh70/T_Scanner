# streamlit_app.py

import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="🧪 Testosterone Risk Scanner", layout="centered")

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton > button {
        background-color: #00897B;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
    }
    .stMetric {
        font-size: 1.2rem;
    }
    .risk-safe {color: green;}
    .risk-low {color: orange;}
    .risk-high {color: red;}
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Testosterone Risk Scanner")
st.markdown("Scan any product by barcode or image and check for hormone-disrupting ingredients.")

tab1, tab2 = st.tabs(["📦 Barcode Scan", "🖼️ Image Scan"])

# --- 📦 Barcode Tab ---
with tab1:
    barcode = st.text_input("Enter Product Barcode")
    if st.button("🔍 Scan Barcode"):
        if barcode.strip():
            with st.spinner("Scanning product..."):
                try:
                    res = requests.post(f"http://127.0.0.1:8000/scan/barcode", params={"barcode": barcode})
                    if res.status_code == 200:
                        data = res.json()
                        st.success(f"**🧾 Product:** {data['productName']}")
                        st.metric("Risk Score", f"{data['tscore']} / 100")
                        st.markdown(f"**Risk Level:** `{data['riskLevel']}`")

                        if data["badIngredients"]:
                            st.markdown("---")
                            st.warning("⚠️ Risky Ingredients Detected")
                            for item in data["badIngredients"]:
                                st.markdown(f"""
                                - **{item['name'].title()}**  
                                  ‣ *Category:* {item['category']}  
                                  ‣ *Penalty:* `{item['penalty']}`
                                """)
                        else:
                            st.success("✅ No harmful ingredients found.")
                    else:
                        st.error("❌ Product not found or API error.")
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
        else:
            st.warning("Please enter a barcode.")

# --- 🖼️ Image Tab ---
with tab2:
    uploaded_image = st.file_uploader("Upload Ingredient Label (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_image and st.button("📸 Scan Image"):
        with st.spinner("Extracting ingredients via OCR..."):
            try:
                files = {"image": (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)}
                res = requests.post("http://127.0.0.1:8000/scan/image", files=files)

                if res.status_code == 200:
                    data = res.json()
                    st.success(f"**🧾 Source:** {data['productName']}")
                    st.metric("Risk Score", f"{data['tscore']} / 100")
                    st.markdown(f"**Risk Level:** `{data['riskLevel']}`")

                    if data["badIngredients"]:
                        st.markdown("---")
                        st.warning("⚠️ Risky Ingredients Found")
                        for item in data["badIngredients"]:
                            st.markdown(f"""
                            - **{item['name'].title()}**  
                              ‣ *Category:* {item['category']}  
                              ‣ *Penalty:* `{item['penalty']}`
                            """)
                    else:
                        st.success("✅ No harmful ingredients found.")
                else:
                    st.error("❌ Failed to extract from image.")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

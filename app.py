import streamlit as st
from PIL import Image
import requests
import base64
import io

# ==========================
# KONFIGURASI
# ==========================

API_KEY = st.secrets["ROBOFLOW_API_KEY"]

URL = "https://serverless.roboflow.com/dindas-workspace-ksvfg/workflows/deteksi-kesalahan-sambungan-kayi-vdeteksi-kesalahan-sambungan-kayi-2-yolo11n-t1-logic"

st.set_page_config(
    page_title="AI Deteksi Sambungan Kayu",
    page_icon="🪵",
    layout="centered"
)

st.title("🪵 AI Deteksi Kualitas Sambungan Kayu")

uploaded_file = st.file_uploader(
    "Upload Foto",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, use_container_width=True)

    if st.button("Analisis"):

        buffered = io.BytesIO()

        image.save(buffered, format="JPEG")

        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        payload = {
            "api_key": API_KEY,
            "inputs": {
                "image": {
                    "type": "base64",
                    "value": img_base64
                }
            }
        }

        with st.spinner("Menganalisis..."):

            response = requests.post(
                URL,
                json=payload,
                headers={
                    "Content-Type": "application/json"
                }
            )

        st.write("Status:", response.status_code)

        if response.status_code == 200:

            st.success("Berhasil")

            st.json(response.json())

        else:

            st.error("Gagal")

            st.code(response.text)

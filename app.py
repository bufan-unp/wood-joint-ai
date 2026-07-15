import streamlit as st
from PIL import Image
import requests
import tempfile

# ==========================
# KONFIGURASI
# ==========================

API_KEY = st.secrets["5O16BkW40azXbHovpDWZ"]

WORKFLOW_URL = (
    "https://serverless.roboflow.com/"
    "dindas-workspace-ksvfg/workflows/"
    "deteksi-kesalahan-sambungan-kayi-vdeteksi-kesalahan-sambungan-kayi-2-yolo11n-t1-logic"
)

st.set_page_config(
    page_title="AI Deteksi Sambungan Kayu",
    page_icon="🪵",
    layout="centered"
)

st.title("🪵 AI Deteksi Kualitas Sambungan Kayu")

st.write(
    "Upload foto sambungan kayu kemudian klik analisis untuk mendeteksi kualitas sambungan menggunakan Artificial Intelligence."
)

uploaded_file = st.file_uploader(
    "Pilih Foto",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Foto yang diupload",
        use_container_width=True
    )

    if st.button("Analisis"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:

            image.save(tmp.name)

            with open(tmp.name, "rb") as img_file:

                files = {
                    "image": img_file
                }

                data = {
                    "api_key": API_KEY
                }

                with st.spinner("Sedang menganalisis..."):

                    response = requests.post(
                        WORKFLOW_URL,
                        files=files,
                        data=data
                    )

        if response.status_code == 200:

            result = response.json()

            st.success("Analisis selesai")

            st.subheader("Hasil Deteksi")

            st.json(result)

        else:

            st.error("Analisis gagal")

            st.write("Status Code :", response.status_code)

            st.code(response.text)

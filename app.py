import streamlit as st
from inference_sdk import InferenceHTTPClient
from PIL import Image
import tempfile

# ==========================
# GANTI API KEY DI SINI
# ==========================

API_KEY = "5O16BkW40azXbHovpDWZ"

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY
)

st.set_page_config(page_title="AI Deteksi Sambungan Kayu", layout="centered")

st.title("🪵 AI Deteksi Kualitas Sambungan Kayu")
st.write("Silakan foto atau upload sambungan kayu.")

uploaded_file = st.file_uploader(
    "Pilih Foto",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Foto yang diupload", use_container_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)

        with st.spinner("Menganalisis..."):

            result = client.run_workflow(
                workspace_name="dindas-workspace-ksvfg",
                workflow_id="deteksi-kesalahan-sambungan-kayi-vdeteksi-kesalahan-sambungan-kayi-2-yolo11n-t1-logic",
                images={
                    "image": tmp.name
                }
            )

    st.subheader("Hasil Deteksi")

    st.json(result)

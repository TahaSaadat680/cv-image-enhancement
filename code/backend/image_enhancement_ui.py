# code/image_enhancement_ui.py
import streamlit as st
import os
from functions import process_and_save_all
from PIL import Image

# Output directories
OUTPUT_IMAGES_DIR = "output_images"
OUTPUT_HISTS_DIR = "output_histograms"

st.set_page_config(page_title="🩺 Medical Image Enhancement", layout="wide")
st.title("🩺 Medical Image Enhancement Tool")
st.markdown("Enhance medical scans using **Gamma Correction, Contrast Stretching, and Combined Contrast→Gamma**.")

# Sidebar controls
st.sidebar.header("⚙️ Enhancement Settings")

# Gamma slider
gamma = st.sidebar.slider("Gamma value", 0.1, 3.0, 0.5, step=0.1)

# Contrast Stretching controls
st.sidebar.subheader("Contrast Stretching Parameters")
r1 = st.sidebar.slider("r1 (input breakpoint)", 0, 255, 70, step=5)
s1 = st.sidebar.slider("s1 (output value at r1)", 0, 255, 0, step=5)
r2 = st.sidebar.slider("r2 (input breakpoint)", 0, 255, 140, step=5)
s2 = st.sidebar.slider("s2 (output value at r2)", 0, 255, 255, step=5)

# File uploader
uploaded_file = st.file_uploader("📂 Upload a medical image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    input_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Show original image
    st.subheader("🖼️ Original Image")
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    # Process button
    if st.button("🚀 Enhance Image"):
        st.info("Processing... Please wait.")
        outputs = process_and_save_all(
            input_path, OUTPUT_IMAGES_DIR, OUTPUT_HISTS_DIR,
            gamma=gamma, r1=r1, s1=s1, r2=r2, s2=s2
        )

        st.success("✅ Enhancement completed!")

        # Display results in columns
        st.subheader("🔍 Enhanced Images")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(outputs["gamma_img"], caption=f"Gamma Correction (γ={gamma})", use_container_width=True)

        with col2:
            st.image(outputs["contrast_img"], caption=f"Contrast Stretching (r1={r1}, r2={r2})", use_container_width=True)

        with col3:
            st.image(outputs["combined_img"], caption=f"Contrast → Gamma (γ={gamma})", use_container_width=True)

        # Expanders for histograms
        with st.expander("📊 Show Histograms"):
            h0, h1, h2, h3 = st.columns(4)
            with h0:
                st.image(outputs["original_hist"], caption="Original Histogram", use_container_width=True)
            with h1:
                st.image(outputs["gamma_hist"], caption="Gamma Histogram", use_container_width=True)
            with h2:
                st.image(outputs["contrast_hist"], caption="Contrast Histogram", use_container_width=True)
            with h3:
                st.image(outputs["combined_hist"], caption="Combined Histogram", use_container_width=True)

        # Download buttons
        st.subheader("⬇️ Download Results")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button("Download Gamma Image", open(outputs["gamma_img"], "rb"), file_name="gamma_result.jpg")
        with col_d2:
            st.download_button("Download Contrast Image", open(outputs["contrast_img"], "rb"), file_name="contrast_result.jpg")
        with col_d3:
            st.download_button("Download Combined Image", open(outputs["combined_img"], "rb"), file_name="combined_result.jpg")

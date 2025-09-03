# image_enhancement_ui.py
import streamlit as st
import os
from functions import process_and_save_all
from PIL import Image
import time

# Output directories
OUTPUT_IMAGES_DIR = "output_images"
OUTPUT_HISTS_DIR = "output_histograms"

# Page configuration with modern theme
st.set_page_config(
    page_title="Medical Image Enhancement",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Card-like containers */
    .upload-card, .controls-card, .results-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
        margin-bottom: 1.5rem;
    }
    
    /* Upload area styling */
    .upload-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border: 2px dashed #667eea;
        text-align: center;
    }
    
    /* Controls styling */
    .controls-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    }
    
    /* Results container */
    .results-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    
    /* Image containers */
    .image-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        margin: 0.25rem;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: scale(1.05);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Info messages */
    .stSuccess, .stInfo {
        border-radius: 10px;
        border-left: 5px solid #11998e;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 0.5rem;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🩺 Medical Image Enhancement</h1>
    <p>Advanced image processing for medical imaging analysis</p>
</div>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    # Upload Section
    st.markdown("""
    <div class="upload-card">
        <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">📁 Upload Medical Image</h3>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPEG, PNG"
    )
    
    if uploaded_file is not None:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(uploaded_file, caption="📋 Original Medical Image", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # File info
        st.info(f"📊 **File Details:**\n- Name: {uploaded_file.name}\n- Size: {uploaded_file.size / 1024:.1f} KB")

with col2:
    # Controls Section
    st.markdown("""
    <div class="controls-card">
        <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">⚙️ Enhancement Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Gamma slider with better styling
    gamma = st.slider(
        "🔆 Gamma Correction Value",
        min_value=0.1,
        max_value=3.0,
        value=0.5,
        step=0.1,
        help="Lower values brighten the image, higher values darken it"
    )
    
    # Display gamma value with styling
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: #667eea; margin: 0;">Current Gamma</h4>
        <h2 style="color: #333; margin: 0.5rem 0;">{gamma}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhancement explanation
    with st.expander("ℹ️ About Enhancement Techniques"):
        st.markdown("""
        **🔍 Histogram Equalization**: Improves contrast by redistributing pixel intensities
        
        **🌟 Gamma Correction**: Adjusts brightness and contrast non-linearly
        
        **🔄 Combined Method**: Applies histogram equalization followed by gamma correction
        """)

# Processing Section
if uploaded_file is not None:
    st.markdown("---")
    
    # Center the enhance button
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        enhance_button = st.button("🚀 Enhance Image", use_container_width=True)
    
    if enhance_button:
        # Save uploaded file temporarily
        input_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Initializing enhancement process...")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        status_text.text("📊 Applying histogram equalization...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        status_text.text("🌟 Applying gamma correction...")
        progress_bar.progress(80)
        
        # Process the image
        outputs = process_and_save_all(input_path, OUTPUT_IMAGES_DIR, OUTPUT_HISTS_DIR, gamma=gamma)
        
        progress_bar.progress(100)
        status_text.text("✅ Enhancement completed successfully!")
        time.sleep(1)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Success message
        st.success("🎉 Image enhancement completed successfully!")
        
        # Results Section
        st.markdown("""
        <div class="results-card">
            <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem;">📈 Enhancement Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Display results in tabs for better organization
        tab1, tab2, tab3 = st.tabs(["🔍 Histogram Equalization", "🌟 Gamma Correction", "🔄 Combined Method"])
        
        with tab1:
            col_img, col_hist = st.columns(2)
            with col_img:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(outputs["hist_eq_img"], caption="Histogram Equalization Result", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_hist:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(outputs["hist_eq_hist"], caption="Histogram Distribution", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            col_img, col_hist = st.columns(2)
            with col_img:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(outputs["gamma_img"], caption=f"Gamma Correction (γ={gamma})", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_hist:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(outputs["gamma_hist"], caption="Histogram Distribution", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            col_img, col_hist = st.columns(2)
            with col_img:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(outputs["combined_img"], caption=f"Combined Method (γ={gamma})", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_hist:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(outputs["combined_hist"], caption="Histogram Distribution", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Download section
        st.markdown("---")
        st.markdown("### 💾 Download Enhanced Images")
        
        download_col1, download_col2, download_col3 = st.columns(3)
        
        with download_col1:
            with open(outputs["hist_eq_img"], "rb") as file:
                st.download_button(
                    "📊 Download Histogram EQ",
                    file,
                    file_name="histogram_equalization.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
        
        with download_col2:
            with open(outputs["gamma_img"], "rb") as file:
                st.download_button(
                    "🌟 Download Gamma Corrected",
                    file,
                    file_name="gamma_corrected.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
        
        with download_col3:
            with open(outputs["combined_img"], "rb") as file:
                st.download_button(
                    "🔄 Download Combined",
                    file,
                    file_name="combined_enhancement.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🩺 Medical Image Enhancement Tool | Built with Streamlit</p>
    <p style="font-size: 0.9rem;">For research and educational purposes</p>
</div>
""", unsafe_allow_html=True)
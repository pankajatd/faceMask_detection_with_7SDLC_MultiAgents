"""
Application: AI Face Mask Detection & Safety Compliance Dashboard
Framework: Streamlit
Author: Software Engineer Subagent
Status: Production Ready (Task 4 - Updated with Stateful Benchmark Tabs)
"""

import io
import os
import sys
import numpy as np
import cv2
from PIL import Image
import streamlit as st

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import validate_image_bytes, convert_bgr_to_rgb
from src.detector import load_face_detector, detect_and_classify_frame


# Page Configuration
st.set_page_config(
    page_title="AI Face Mask Detection & Safety Compliance",
    page_icon="😷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-green { color: #10B981; }
    .metric-red { color: #EF4444; }
    .metric-blue { color: #3B82F6; }
    .metric-purple { color: #8B5CF6; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_detector():
    """Initializes and caches the face detector model in memory."""
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
    return load_face_detector(models_dir)


def render_sidebar(detector):
    """Renders dashboard sidebar controls and metadata."""
    st.sidebar.markdown("### ⚙️ System Controls")
    
    # Input Mode Selector
    mode = st.sidebar.radio(
        "Choose Input Mode:",
        ["🖼️ Photo Analysis Mode", "📷 Live Camera Snapshot"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎚️ Detection Sensitivity")
    
    # Confidence Slider
    confidence_threshold = st.sidebar.slider(
        "Face Detection Confidence Threshold",
        min_value=0.40,
        max_value=0.95,
        value=0.55,
        step=0.05,
        help="Minimum confidence score required for facial bounding box proposal."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧠 AI Engine Status")
    
    if detector.model_type == "dnn_caffe":
        st.sidebar.success("✅ **Primary DL SSD (ResNet-10)** Active")
        st.sidebar.caption("High-accuracy CNN with multi-angle, profile, and tilt resistance.")
    else:
        st.sidebar.warning("⚠️ **OpenCV Haar Cascade** Active (Fallback)")
        st.sidebar.caption("Running lightweight geometric fallback detector.")
        
    st.sidebar.markdown("---")
    st.sidebar.caption("Face Mask Detection System v1.0.0 | SDLC Agent Framework")
    
    return mode, confidence_threshold


def render_metrics_cards(total_faces: int, masked: int, unmasked: int):
    """Renders summary KPI cards."""
    compliance_rate = (masked / total_faces * 100) if total_faces > 0 else 100.0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Faces</div>
            <div class="metric-value metric-blue">{total_faces}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Masks Worn (Compliant)</div>
            <div class="metric-value metric-green">{masked}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">No Mask (Non-Compliant)</div>
            <div class="metric-value metric-red">{unmasked}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        rate_color = "metric-green" if compliance_rate >= 80 else ("metric-purple" if compliance_rate >= 50 else "metric-red")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Compliance Rate</div>
            <div class="metric-value {rate_color}">{compliance_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)


def enhance_low_res_image(image_rgb: np.ndarray, min_dimension: int = 550) -> np.ndarray:
    """
    Automatically upscales and sharpens low-resolution images to eliminate pixelation.
    Applies high-fidelity Lanczos-4 interpolation and subtle unsharp masking.
    """
    if image_rgb is None:
        return image_rgb
    h, w = image_rgb.shape[:2]
    if max(h, w) < min_dimension:
        scale = min_dimension / float(max(h, w))
        new_w = int(round(w * scale))
        new_h = int(round(h * scale))
        upscaled = cv2.resize(image_rgb, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        gaussian = cv2.GaussianBlur(upscaled, (0, 0), 1.5)
        enhanced = cv2.addWeighted(upscaled, 1.25, gaussian, -0.25, 0)
        return enhanced
    return image_rgb


def process_and_display(image_rgb: np.ndarray, detector, confidence_threshold: float, filename_prefix: str = "detection"):
    """Runs inference and displays detection output, metrics, and download options."""
    # Ensure image is crisp and not pixelated
    image_rgb = enhance_low_res_image(image_rgb)

    with st.spinner("Analyzing frame with ResNet-10 SSD face detector and mask classifier..."):
        res = detect_and_classify_frame(
            image=image_rgb,
            detector=detector,
            confidence_threshold=confidence_threshold
        )

    # 1. KPI Cards
    render_metrics_cards(res["total_faces"], res["masked_count"], res["unmasked_count"])
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Side-by-Side Visual Comparison
    col_orig, col_annot = st.columns(2)
    with col_orig:
        st.markdown("##### 📷 Original Frame")
        st.image(image_rgb, use_container_width=True)
    with col_annot:
        st.markdown("##### 🎯 Detection & Classification Result")
        st.image(res["annotated_image"], use_container_width=True)

    # 3. Download Button
    annotated_bgr = cv2.cvtColor(res["annotated_image"], cv2.COLOR_RGB2BGR)
    success, buffer = cv2.imencode(".jpg", annotated_bgr)
    if success:
        st.download_button(
            label="📥 Download Annotated Image (.jpg)",
            data=buffer.tobytes(),
            file_name=f"{filename_prefix}_annotated.jpg",
            mime="image/jpeg",
            use_container_width=True
        )

    # 4. Detailed Detection Roster Table
    if res["results"]:
        with st.expander(f"📋 View Detailed Face Detections Log ({len(res['results'])} detected)", expanded=True):
            table_data = []
            for idx, r in enumerate(res["results"], start=1):
                box = r["box"]
                status_icon = "🟢 COMPLIANT" if r["label"] == "Mask" else "🔴 NON-COMPLIANT"
                table_data.append({
                    "Face #": idx,
                    "Status": status_icon,
                    "Classification": r["label"],
                    "Confidence": f"{r['confidence'] * 100:.1f}%",
                    "Bounding Box (X1, Y1, X2, Y2)": f"({box[0]}, {box[1]}, {box[2]}, {box[3]})",
                    "Face Box Size": f"{box[2]-box[0]}x{box[3]-box[1]} px"
                })
            st.dataframe(table_data, use_container_width=True)
    else:
        st.info("ℹ️ No human faces detected in this image. Try adjusting the confidence threshold slider in the sidebar if faces are far away.")


def main():
    # Header Banner
    st.markdown('<div class="main-header">😷 AI Face Mask Detection & Safety Compliance Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated real-time face localization, protective mask verification, and safety metric auditing.</div>', unsafe_allow_html=True)

    # Load detector
    detector = get_detector()

    # Sidebar
    mode, confidence_threshold = render_sidebar(detector)

    if mode == "🖼️ Photo Analysis Mode":
        tab_samples, tab_upload = st.tabs([
            "⚡ Pre-Tested Demo Samples", 
            "📁 Upload Your Own Photo"
        ])

        sample_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tests", "test_images", "user_uploads")
        samples_dict = {
            "Two Nurses (Putting on Gloves)": os.path.join(sample_base, "two_nurses_gloves.jpg"),
            "Medical Team in Scrubs": os.path.join(sample_base, "medical_team.jpg"),
            "Doctor in Blue Scrubs": os.path.join(sample_base, "doctor_blue_scrubs.jpg"),
            "Side Profile (Black Fabric Mask)": os.path.join(sample_base, "side_profile_black_mask.jpg"),
            "White N95 Mask (Compliant)": os.path.join(sample_base, "white_n95_mask.jpg"),
            "Unmasked Portrait (Non-Compliant)": os.path.join(sample_base, "unmasked_person.jpg")
        }

        # --- TAB 1: PRE-TESTED SAMPLES ---
        with tab_samples:
            st.markdown("#### ⚡ 1-Click Demo Samples")
            st.caption("Select any benchmark sample below to instantly run AI face and mask analysis in high definition:")

            selected_sample_name = st.pills(
                label="Choose a demo photo to inspect:",
                options=list(samples_dict.keys()),
                default="Two Nurses (Putting on Gloves)"
            )

            if selected_sample_name and selected_sample_name in samples_dict:
                sample_path = samples_dict[selected_sample_name]
                bgr_img = cv2.imread(sample_path)
                if bgr_img is not None:
                    image_rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
                    safe_prefix = selected_sample_name.lower().replace(" ", "_").replace("(", "").replace(")", "")
                    st.info(f"🔍 Currently viewing: **{selected_sample_name}**")
                    process_and_display(image_rgb, detector, confidence_threshold, filename_prefix=safe_prefix)
                else:
                    st.error(f"Could not load image at path: {sample_path}")

        # --- TAB 2: CUSTOM UPLOAD ---
        with tab_upload:
            st.markdown("#### 📁 Upload Custom Photo")
            st.caption("Upload your own custom image (.jpg, .jpeg, .png) to verify mask compliance:")

            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=["jpg", "jpeg", "png"],
                key="custom_file_uploader",
                help="Select an image from your computer to inspect mask compliance."
            )

            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                if not validate_image_bytes(file_bytes):
                    st.error("❌ The uploaded file is corrupt or is not a valid image format. Please upload a standard JPG or PNG.")
                else:
                    nparr = np.frombuffer(file_bytes, np.uint8)
                    bgr_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    if bgr_img is not None:
                        image_rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
                        image_name = uploaded_file.name.rsplit(".", 1)[0]
                        process_and_display(image_rgb, detector, confidence_threshold, filename_prefix=image_name)
            else:
                st.markdown("""
                <div style="background-color: #F8FAFC; border-radius: 8px; padding: 28px; text-align: center; color: #64748B; border: 1px dashed #CBD5E1; margin-top: 15px;">
                    <p style="font-size: 1.15rem; font-weight: 500; margin-bottom: 6px;">Drag and drop a photo here, or browse from your computer</p>
                    <p style="font-size: 0.85rem; color: #94A3B8; margin: 0;">Supports high-resolution portraits, multi-person crowds, and angled profiles.</p>
                </div>
                """, unsafe_allow_html=True)

    elif mode == "📷 Live Camera Snapshot":
        st.markdown("#### 📷 Live Camera Snapshot Mode")
        st.caption("Capture a live frame using your connected webcam to run real-time compliance verification.")

        camera_photo = st.camera_input("Take a photo to test mask compliance")

        if camera_photo is not None:
            photo_bytes = camera_photo.read()
            if validate_image_bytes(photo_bytes):
                nparr = np.frombuffer(photo_bytes, np.uint8)
                bgr_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if bgr_img is not None:
                    image_rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
                    process_and_display(image_rgb, detector, confidence_threshold, filename_prefix="webcam_snapshot")
            else:
                st.error("❌ Failed to read frame from webcam input.")


if __name__ == "__main__":
    main()

"""
Professional Weapon Surveillance Dashboard
Real-time AI-powered threat detection with alert storage
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import tempfile
import time
from datetime import datetime
import importlib

# ✅ MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Weapon Surveillance AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ WhatsApp Alert Import (after set_page_config)
try:
    from whatsapp_alert import weapon_detected_alert
    WHATSAPP_ENABLED = True
except ImportError:
    WHATSAPP_ENABLED = False
    st.warning("⚠️ WhatsApp alerts disabled - whatsapp_alert module not found")

# ================== ALERT CONFIG ==================
CLIENT_WHATSAPP_NUMBER = "+917396795949"
ALERT_COOLDOWN_SECONDS = 60
ALERTS_FOLDER = "alerts"

# Create alerts folder if it doesn't exist
os.makedirs(ALERTS_FOLDER, exist_ok=True)

# ================== ENHANCED CSS ==================
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Main Container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Header Styling */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        animation: slideDown 0.6s ease-out;
    }
    
    .hero-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Control Panel */
    .control-panel {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Slider */
    .stSlider {
        padding: 1rem 0;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3);
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Alert Box */
    .alert-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
        animation: pulse 2s infinite;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
    }
    
    /* Stats Card */
    .stats-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stats-card h3 {
        color: #667eea;
        font-size: 1.8rem;
        margin: 0;
    }
    
    .stats-card p {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin: 0.25rem 0 0 0;
    }
    
    /* Animations */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    /* Image Display */
    .stImage {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Labels */
    label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ MODEL LOADER ------------------
def load_security_engine(model_path):
    ultra = importlib.import_module("ultralytics")
    ModelLoader = getattr(ultra, "YOLO")
    return ModelLoader(model_path)

MODEL_PATH = "weapon_detector_v1.pt"
CAMERA_ID_DEFAULT = "CAM-1"
CLASS_NAMES = [
    "Automatic Rifle", "Bazooka", "Grenade Launcher", "Handgun",
    "Knife", "Shotgun", "SMG", "Sniper", "Sword"
]
DEFAULT_CONF = 0.35
DISPLAY_FPS = 10

@st.cache_resource(show_spinner=False)
def load_model_cached(path):
    return load_security_engine(path)

# ------------------ UTIL FUNCTIONS ------------------
def save_detection_image(img_bgr, detected_objects, camera_id):
    """Save detection image to alerts folder"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        weapons_str = "_".join([obj.replace(" ", "-") for obj in detected_objects[:2]])
        filename = f"{camera_id}_{timestamp}_{weapons_str}.jpg"
        filepath = os.path.join(ALERTS_FOLDER, filename)
        cv2.imwrite(filepath, img_bgr)
        return filepath
    except Exception as e:
        st.error(f"Failed to save image: {str(e)}")
        return None

def draw_boxes(img_bgr, boxes, scores, classes, names):
    img = img_bgr.copy()
    for (x1, y1, x2, y2), sc, cls in zip(boxes, scores, classes):
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        label = f"{names[int(cls)]} {sc:.2f}"
        
        # Label background
        (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(img, (x1, y1 - label_h - 10), (x1 + label_w, y1), (0, 0, 255), -1)
        cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return img

def run_model_on_frame(model, frame_bgr, conf_thr):
    result = model(frame_bgr, conf=conf_thr, verbose=False)[0]
    boxes, scores, classes = [], [], []
    if result.boxes is not None:
        for b, c, k in zip(
            result.boxes.xyxy.cpu().numpy(),
            result.boxes.conf.cpu().numpy(),
            result.boxes.cls.cpu().numpy()
        ):
            boxes.append(b)
            scores.append(float(c))
            classes.append(int(k))
    return boxes, scores, classes

# ------------------ HEADER ------------------
st.markdown("""
<div class="hero-header">
    <h1>🛡️ Advanced Weapon Surveillance System</h1>
    <p>Real-time AI-powered threat detection & automated alerts</p>
</div>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "cam_on" not in st.session_state:
    st.session_state.cam_on = False
if "last_whatsapp_alert" not in st.session_state:
    st.session_state.last_whatsapp_alert = 0
if "total_detections" not in st.session_state:
    st.session_state.total_detections = 0

# ------------------ MAIN UI ------------------
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Control Panel")
    conf = st.slider("🎯 Confidence Threshold", 0.05, 0.99, DEFAULT_CONF, 0.01)
    camera_id = st.text_input("📹 Camera ID", CAMERA_ID_DEFAULT)
    
    st.markdown("### 📊 Statistics")
    st.markdown(f"""
    <div class="stats-card">
        <h3>{st.session_state.total_detections}</h3>
        <p>Total Detections</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show saved alerts count
    alert_files = os.listdir(ALERTS_FOLDER) if os.path.exists(ALERTS_FOLDER) else []
    st.markdown(f"""
    <div class="stats-card">
        <h3>{len(alert_files)}</h3>
        <p>Saved Alerts</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col1:
    tabs = st.tabs(["📹 Live Webcam", "🖼️ Image Upload", "🎬 Video Upload"])
    
    # Load model
    try:
        model = load_model_cached(MODEL_PATH)
    except Exception as e:
        st.error(f"❌ Failed to load model: {str(e)}")
        st.stop()

    # ================= LIVE WEBCAM =================
    with tabs[0]:
        col_start, col_stop = st.columns(2)
        with col_start:
            start = st.button("▶️ Start Camera", use_container_width=True)
        with col_stop:
            stop = st.button("⏹️ Stop Camera", use_container_width=True)
        
        if start:
            st.session_state.cam_on = True
        if stop:
            st.session_state.cam_on = False
        
        placeholder = st.empty()
        
        if st.session_state.cam_on:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ Cannot access webcam")
                st.session_state.cam_on = False
            else:
                last = 0
                while st.session_state.cam_on:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    if time.time() - last < 1 / DISPLAY_FPS:
                        continue
                    last = time.time()
                    
                    boxes, scores, classes = run_model_on_frame(model, frame, conf)
                    annotated = draw_boxes(frame, boxes, scores, classes, CLASS_NAMES)
                    
                    detected_objects = []
                    confidence_scores = []
                    for s, c in zip(scores, classes):
                        if s >= conf:
                            detected_objects.append(CLASS_NAMES[c])
                            confidence_scores.append(s)
                    
                    if detected_objects:
                        now = time.time()
                        if now - st.session_state.last_whatsapp_alert > ALERT_COOLDOWN_SECONDS:
                            # Save detection image
                            saved_path = save_detection_image(annotated, detected_objects, camera_id)
                            
                            # Send WhatsApp alert
                            if WHATSAPP_ENABLED:
                                weapon_detected_alert(
                                    client_number=CLIENT_WHATSAPP_NUMBER,
                                    camera_id=camera_id,
                                    detected_objects=detected_objects,
                                    confidence_scores=confidence_scores
                                )
                            
                            st.session_state.last_whatsapp_alert = now
                            st.session_state.total_detections += 1
                    
                    placeholder.image(annotated[:, :, ::-1], channels="RGB")
                
                cap.release()

    # ================= IMAGE UPLOAD =================
    with tabs[1]:
        img_file = st.file_uploader("📤 Upload Image", ["jpg", "png", "jpeg"])
        if img_file:
            img = Image.open(img_file).convert("RGB")
            arr = np.array(img)[:, :, ::-1]
            
            boxes, scores, classes = run_model_on_frame(model, arr, conf)
            annotated = draw_boxes(arr, boxes, scores, classes, CLASS_NAMES)
            
            detected_objects = []
            confidence_scores = []
            for s, c in zip(scores, classes):
                if s >= conf:
                    detected_objects.append(CLASS_NAMES[c])
                    confidence_scores.append(s)
            
            if detected_objects:
                st.markdown(f'<div class="alert-box">🚨 THREAT DETECTED: {", ".join(detected_objects)}</div>', unsafe_allow_html=True)
                
                # Save detection image
                saved_path = save_detection_image(annotated, detected_objects, camera_id)
                if saved_path:
                    st.markdown(f'<div class="success-message">✅ Alert saved: {os.path.basename(saved_path)}</div>', unsafe_allow_html=True)
                
                # Send WhatsApp alert
                if WHATSAPP_ENABLED:
                    weapon_detected_alert(
                        client_number=CLIENT_WHATSAPP_NUMBER,
                        camera_id=camera_id,
                        detected_objects=detected_objects,
                        confidence_scores=confidence_scores
                    )
                
                st.session_state.total_detections += 1
            
            st.image(annotated[:, :, ::-1])

    # ================= VIDEO UPLOAD =================
    with tabs[2]:
        video_file = st.file_uploader("📤 Upload Video", ["mp4", "avi", "mkv"])
        if video_file:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(video_file.read())
            tfile.close()
            
            cap = cv2.VideoCapture(tfile.name)
            stframe = st.empty()
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                boxes, scores, classes = run_model_on_frame(model, frame, conf)
                annotated = draw_boxes(frame, boxes, scores, classes, CLASS_NAMES)
                
                detected_objects = []
                confidence_scores = []
                for s, c in zip(scores, classes):
                    if s >= conf:
                        detected_objects.append(CLASS_NAMES[c])
                        confidence_scores.append(s)
                
                if detected_objects:
                    now = time.time()
                    if now - st.session_state.last_whatsapp_alert > ALERT_COOLDOWN_SECONDS:
                        # Save detection image
                        saved_path = save_detection_image(annotated, detected_objects, camera_id)
                        
                        # Send WhatsApp alert
                        if WHATSAPP_ENABLED:
                            weapon_detected_alert(
                                client_number=CLIENT_WHATSAPP_NUMBER,
                                camera_id=camera_id,
                                detected_objects=detected_objects,
                                confidence_scores=confidence_scores
                            )
                        
                        st.session_state.last_whatsapp_alert = now
                        st.session_state.total_detections += 1
                
                stframe.image(annotated[:, :, ::-1], channels="RGB")
            
            cap.release()
            os.unlink(tfile.name)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.6); padding: 1rem;'>
    <p>🛡️ Advanced Weapon Surveillance System | AI-Powered Security Solution</p>
    <p>Alert images saved to: <code>alerts/</code> folder</p>
</div>
""", unsafe_allow_html=True)
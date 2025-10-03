"""
Streamlit Frontend - Main Application
Food Recognition & Nutrition Web Application
"""
import streamlit as st
import requests
import json
from PIL import Image
import io
import time
import base64
import os
from pathlib import Path

# Configure Streamlit page
st.set_page_config(
    page_title="Food Recognition & Nutrition",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API configuration
BACKEND_URL = "http://127.0.0.1:8000"

def load_logo_base64(logo_filename="logo.png"):
    """Load logo from assets/icons and convert to base64"""
    try:
        logo_path = Path(__file__).parent / "assets" / "icons" / logo_filename
        if logo_path.exists():
            with open(logo_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        else:
            print(f"Logo not found: {logo_path}")
            return None
    except Exception as e:
        print(f"Error loading logo: {e}")
        return None

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        /* Main app styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.9;
            margin: 0;
        }
        
        /* Feature cards */
        .feature-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3498db;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .feature-card h3 {
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .feature-card p {
            color: #5a6c7d;
            margin: 0;
        }
        
        /* Stats section */
        .stats-container {
            display: flex;
            justify-content: space-around;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        
        .stat-item {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            min-width: 120px;
            margin: 0.5rem;
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.3);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        /* Instructions section */
        .instructions {
            background: #EDC213;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #f39c12;
            margin: 1.5rem 0;
        }
        
        .instructions h3 {
            color: #d68910;
            margin-bottom: 1rem;
        }
        
        /* API status indicator */
        .api-status {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            text-align: center;
            margin: 1rem 0;
        }
        
        .api-online {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .api-offline {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        /* Navigation styling */
        .nav-item {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border: 1px solid #dee2e6;
            transition: all 0.3s ease;
        }
        
        .nav-item:hover {
            background: #e9ecef;
            transform: translateY(-2px);
        }
        
        
        /* Footer */
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem;
            border-radius: 12px;
            margin-top: 3rem;
        }
        .top-logo {
            position: absolute;
            top: -230px;
            left: -15px;
            z-index: 999999;
            display: flex;
            align-items: center;
            gap: 8px;
            /* Màu adaptive với system theme */
            background: var(--background-color, #fafafa);
            border: 0px solid var(--border-color, #e0e0e0);
            color: var(--text-color, #262730);
            padding: 4px 12px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        /* Dark theme override */
        @media (prefers-color-scheme: dark) {
            .top-logo {
                background: #262730;
                border-color: #3a3b47;
                color: #fafafa;
            }
        }
        
        .top-logo img {
            width: 37px;
            height: 37px;
            border-radius: 4px;
            object-fit: cover;
        }
        
        .top-logo span {
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }
        
        
    </style>
    """, unsafe_allow_html=True)

def check_backend_status():
    """Check if backend API is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
    except Exception as e:
        return False, str(e)

def render_api_status():
    """Render API status indicator"""
    is_online, status_data = check_backend_status()
    
    if is_online:
        st.markdown("""
        <div class="api-status api-online">
            Backend API is Online - Ready to process requests
        </div>
        """, unsafe_allow_html=True)
        if status_data:
            st.success(f" API Status: {status_data.get('status', 'healthy')}")
        #  | Version: {status_data.get('version', '1.0.0')}
    else:
        st.markdown("""
        <div class="api-status api-offline">
             Backend API is Offline - Please start the backend server first
        </div>
        """, unsafe_allow_html=True)
        
        st.error("""
         *Backend Not Running*
        """)

        # Please start the backend server first:
        # ```bash
        # cd foodapp/backend
        # python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        # ```    
    return is_online

def main():
    """Main application function"""
    apply_custom_css()
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>Food Recognition & Nutrition</h1>
        <p>AI-Powered Food Recognition with Comprehensive Nutritional Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    api_online = render_api_status()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## Welcome to NutriDish")
        
        st.markdown("""
        Transform your food photos into detailed nutritional insights using our advanced AI system. 
        Simply upload an image and discover what's in your meal!
        """)
        
        # Feature overview
        # st.markdown("###Key Features")
        
        features = [
            {
                "title":"AI Food Recognition",
                "description": "Identify 131 different food items with high accuracy using ResNet50 deep learning"
            },
            {
                "title":"Nutrition Analysis", 
                "description": "Get detailed nutritional information including calories, protein, fat, and carbs"
            },
            {
                "title": "Food Diversity",
                "description": "Support for both international cuisine and Vietnamese traditional dishes"
            },
            {
                "title":"Real-Time Processing",
                "description": "Fast image analysis and instant results for practical daily use"
            }
        ]
        
        for feature in features:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{feature['title']}</h3>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Statistics
        st.markdown("### Web Application Ability")
        st.markdown("""
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">131</div>
                <div class="stat-label">Food Categories</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">101</div>
                <div class="stat-label">International Dishes</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">30</div>
                <div class="stat-label">Vietnamese Dishes</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">224×224</div>
                <div class="stat-label">Input Resolution</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Instructions
        st.markdown("""
        <div class="instructions">
            <h3>How to Get Started</h3>
            <ol>
                <li><strong>Navigate to Predict Page:</strong> Use the sidebar to go to the Predict page</li>
                <li><strong>Upload Image:</strong> Choose a clear photo of your food (JPG, PNG, JPEG)</li>
                <li><strong>Get Results:</strong> Receive instant food identification and nutrition information</li>
                <li><strong>Explore Data:</strong> View detailed nutritional breakdown and health suggestions</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### Navigation")
        
        # Page navigation buttons
        col_nav1, col_nav2 = st.columns(2)
        
        with col_nav1:
            if st.button("Go to Prediction Page", use_container_width=True):
                st.switch_page("pages/1_Predict.py")
        
        with col_nav2:
            if st.button(" About Our Team", use_container_width=True):
                st.switch_page("pages/2_AboutUs.py")
    # Sidebar information
    with st.sidebar:
        # Logo header
        logo_base64 = load_logo_base64("LOGO HCMUTE.png")
        if logo_base64:
            st.markdown(f"""
            <div class="top-logo">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo">
                <h3>Food Recognition & Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="top-logo">
                <span style="font-size: 20px;">🍽️</span>
                <h3>Food Recognition & Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("## The API Status")
        
        if api_online:
            st.success(" Backend Connected")
            st.info(f" API Endpoint: {BACKEND_URL}")
        else:
            st.error("Backend Disconnected")
            st.warning("Please start the backend server")
        
        st.markdown("---")
        st.markdown("### Supported Formats")
        st.markdown("- JPG/JPEG")
        st.markdown("- PNG")
        st.markdown("- Max size: 10MB")

        st.markdown("---")
        st.markdown("## Tips for Best Results")
        st.markdown("- Use clear, well-lit images")
        st.markdown("- Center the food in the frame")
        st.markdown("- Avoid multiple dishes in one image")
        st.markdown("- Higher resolution works better")
        
        st.markdown("---")
        st.markdown("### Quick Links")
        st.markdown(f"[API Documentation]({BACKEND_URL}/docs)")
        st.markdown(f"[API Status]({BACKEND_URL}/health)")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>Food Recognition & Nutrition Web Application</h3>
        <p>Built with using FastAPI, Streamlit, and TensorFlow</p>
        <p>Developed by: Tran Dinh Khuong, Nguyen Nhat Phat, Tran Huynh Xuan Thanh</p>
        <small>Supervisor: Assoc. Prof. Dr. Hoang Van Dung | 15-Week IT Project 2025</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
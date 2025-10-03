"""
Predict Page - Food Recognition and Nutrition Analysis
Upload images and get AI-powered food recognition with detailed nutrition information
"""
import streamlit as st

import requests
import json
from PIL import Image
import io
import time
import base64
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Food Prediction",
    page_icon="🔍",
    layout="wide"
)

# Backend API configuration
BACKEND_URL = "http://127.0.0.1:8000"

def load_logo_base64(logo_filename="logo.png"):
    """Load logo from assets/icons and convert to base64"""
    try:
        logo_path = Path(__file__).parent.parent / "assets" / "icons" / logo_filename
        if logo_path.exists():
            with open(logo_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        else:
            print(f"Logo not found: {logo_path}")
            return None
    except Exception as e:
        print(f"Error loading logo: {e}")
        return None
    
NUTRITION_COLORS = {
    "calories": "#FF6B35",  # Orange for energy
    "protein": "#4ECDC4",   # Teal for protein  
    "fat": "#FFE66D",       # Yellow for fat
    "carbs": "#A8E6CF",     # Light green for carbs
    "fiber": "#88D8B0"      # Green for fiber
}
def apply_predict_css():
    """Apply custom CSS for prediction page"""
    st.markdown("""
    <style>
        .predict-header {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .predict-header h1 {
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
        }
        
        .upload-section {
            background: #3498db;
            padding: 2rem;
            border-radius: 12px;
            border: 2px dashed #dee2e6;
            text-align: center;
            margin: 1.5rem 0;
        }
        
        .result-card {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 1rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            box-shadow: 0 10px 30px rgba(52, 152, 219, 0.3);
        }
        
        .result-card h2 {
            margin-bottom: 0rem;
            padding: 0.25rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        .result-card h3 {
            margin-bottom: 0rem;
            padding: 0.25rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        .confidence-bar {
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            height: 20px;
            margin: 1rem 0;
            overflow: hidden;
        }
        
        .confidence-fill {
            background: #2ecc71;
            height: 100%;
            border-radius: 20px;
            transition: width 0.5s ease;
        }
        
        .nutrition-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }
        
        .nutrition-item {
            background: white;
            color: #2c3e50;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .nutrition-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 0.5rem;
        }
        
        .nutrition-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .top-predictions {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .prediction-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.8rem;
            margin: 0.5rem 0;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 3px solid #3498db;
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #dc3545;
            margin: 1.5rem 0;
        }
        
        .processing-animation {
            text-align: center;
            padding: 2rem;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
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
        /* Nutrition Progress Bars */
        .nutrition-container {
            margin: 0.5rem 0;
        }
        
        .nutrition-container:first-child {
            margin-top: 0.5rem;
        }
        
        .nutrition-container:not(:first-child) {
            margin-top: 1rem;
        }
        
        .nutrition-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.8rem;
        }
        
        .nutrition-icon-section {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .nutrition-icon {
            padding: 0.5rem;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 50px;
        }
        
        .nutrition-icon span {
            font-size: 1.6rem;
        }
        
        .nutrition-label {
            font-size: 1.2rem;
            font-weight: 700;
            color: #fafafa;
        }
        
        .nutrition-values {
            text-align: right;
        }
        
        .nutrition-value {
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 0.2rem;
        }
        
        .nutrition-percentage {
            font-size: 0.9rem;
            color: #7f8c8d;
        }
        
        .nutrition-progress-bar {
            background: #e9ecef;
            border-radius: 20px;
            height: 20px;
            overflow: hidden;
            position: relative;
        }
        
        .nutrition-progress-fill {
            height: 100%;
            border-radius: 20px;
            transition: width 1s ease-out;
            position: relative;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .nutrition-shimmer {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.4) 50%, transparent 100%);
            animation: shimmer 2.5s infinite;
        }
        
        .nutrition-daily-ref {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.75rem;
            color: #6c757d;
            font-weight: 600;
        }
        
    </style>
    """, unsafe_allow_html=True)

def check_backend_connection():
    """Check backend API connection"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def predict_food(image_file):
    """Send image to backend for prediction"""
    try:
        files = {"file": ("image.jpg", image_file, "image/jpeg")}
        response = requests.post(f"{BACKEND_URL}/api/predict", files=files, timeout=30)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            return False, error_data.get('detail', f'Error: {response.status_code}')
    
    except requests.exceptions.Timeout:
        return False, "Request timeout. The image might be too large or the server is busy."
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to backend server. Please ensure the backend is running."
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def render_prediction_result(result):
    """Render prediction results with enhanced UI"""
    if not result:
        return
    st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    """, unsafe_allow_html=True)
    # Main result card
    food_name = result.get('food_name', 'Unknown')
    confidence = result.get('confidence', 0)
    confidence_pct = confidence * 100
    
    st.markdown(f"""
    <div class="result-card">
        <h2><i class="material-icons" style="font-size:24px; color:#27ae60;">search</i> Identified Food: {food_name}</h2>
        <h3>Confidence: {confidence_pct:.1f}%</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Confidence visualization
    # st.markdown("###Prediction Confidence")
    # st.progress(confidence)
    
    if confidence >= 0.8:
        st.success(f"High confidence prediction ({confidence_pct:.1f}%)")
    elif confidence >= 0.5:
        st.warning(f"Moderate confidence prediction ({confidence_pct:.1f}%)")
    else:
        st.error(f"Low confidence prediction ({confidence_pct:.1f}%)")
    
    # Nutrition information
    nutrition = result.get('nutrition', {})
    if nutrition:
        st.markdown("### Nutritional Information")
        
        # col1, col2, col3, col4,col5 = st.columns(5)
        
        # with col1:
        #     st.metric(
        #         label="Calories",
        #         value=f"{nutrition.get('calories', 0):.0f}",
        #         help="Calories per serving"
        #     )
        
        # with col2:
        #     st.metric(
        #         label="Protein",
        #         value=f"{nutrition.get('protein', 0):.1f}g",
        #         help="Protein content in grams"
        #     )
        
        # with col3:
        #     st.metric(
        #         label="Fat",
        #         value=f"{nutrition.get('fat', 0):.1f}g",
        #         help="Fat content in grams"
        #     )
        
        # with col4:
        #     st.metric(
        #         label="Carbs",
        #         value=f"{nutrition.get('carbs', 0):.1f}g",
        #         help="Carbohydrate content in grams"
        #     )
        # with col5:
        #     st.metric(
        #         label="Fiber",
        #         value=f"{nutrition.get('fiber', 0):.1f}g",
        #         help="Dietary fiber in grams"
        #     )
        # Additional nutrition details
        # if nutrition.get('fiber'):
        #     st.info(f"Fiber: {nutrition['fiber']:.1f}g")
        metrics = [
            ("🔥", "Calories", nutrition.get('calories', 0), "", "calories", 2000),
            ("🥩", "Protein", nutrition.get('protein', 0), "g", "protein", 50),
            ("🧈", "Fat", nutrition.get('fat', 0), "g", "fat", 65),
            ("🍞", "Carbs", nutrition.get('carbs', 0), "g", "carbs", 300),
            ("🌾", "Fiber", nutrition.get('fiber', 0), "g", "fiber", 25)
        ]
        
        for i, (icon, label, value, unit, color_key, daily_ref) in enumerate(metrics):
            color = NUTRITION_COLORS[color_key]
            
            # Calculate percentage of daily reference value (max 100%)
            percentage = min((value / daily_ref) * 100, 100) if daily_ref > 0 else 0
            st.markdown(f"""
            <div class="nutrition-container">
                <div class="nutrition-header">
                    <div class="nutrition-icon-section">
                        <div class="nutrition-icon" style="background: {color}20;">
                            <span>{icon}</span>
                        </div>
                        <span class="nutrition-label">{label}</span>
                    </div>
                    <div class="nutrition-values">
                        <div class="nutrition-value" style="color: {color};">
                            {value:.1f}{unit}
                        </div>
                        <div class="nutrition-percentage">
                            {percentage:.1f}% of daily needs
                        </div>
                    </div>
                </div>
                <div class="nutrition-progress-bar">
                    <div class="nutrition-progress-fill" 
                         style="background: linear-gradient(135deg, {color}, {color}aa); width: {percentage}%;">
                        <div class="nutrition-shimmer"></div>
                    </div>
                    <div class="nutrition-daily-ref">
                        Needs: {daily_ref}{unit}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Top predictions
    top_predictions = result.get('top_3_predictions', [])
    if len(top_predictions) > 1:
        st.markdown("### Other Predictions")
        
        for i, pred in enumerate(top_predictions[:3]):
            conf_pct = pred['confidence'] * 100
            medal = ["🥇", "🥈", "🥉"][i]
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{medal} {pred['name']}")
            with col2:
                st.write(f"{conf_pct:.1f}%")
    
    # Processing time and model info
    processing_time = result.get('processing_time', 0)
    model_info = result.get('model_info', 'Unknown')
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Processing Time: {processing_time:.2f}s")
    with col2:
        st.info(f"Model: {model_info}")

def main():
    """Main prediction page function"""
    apply_predict_css()
    
    # Header
    st.markdown("""
    <div class="predict-header">
        <h1> Food Recognition & Analysis</h1>
        <p>Upload your food image and get instant AI-powered recognition with nutrition details</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check backend connection
    if not check_backend_connection():
        st.error("""
        **Backend Server Not Running**
        
        The backend API server is not accessible. Please start it first:
        ```bash
        cd foodapp/backend
        python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ```
        """)
        return
    
    # File upload section
    st.markdown("## Upload Your Food Image")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of food. Supported formats: JPG, JPEG, PNG (Max 10MB)"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Food Image", use_container_width=True)#use_column_width
            
            # Image info
            st.info(f"""
            **Image Details:**
            - Filename: {uploaded_file.name}
            - Size: {len(uploaded_file.getvalue())/1024:.1f} KB
            - Format: {image.format}
            - Dimensions: {image.size[0]} × {image.size[1]}
            """)
        
        with col2:
            st.markdown("### Analysis Results")
            
            # Predict button
            if st.button(" Analyze Food", type="primary", use_container_width=True):
                
                # Show processing animation
                with st.spinner(" Analyzing your food image..."):
                    
                    # Reset file pointer
                    uploaded_file.seek(0)
                    image_bytes = uploaded_file.read()
                    
                    # Make prediction
                    success, result = predict_food(image_bytes)
                    
                    if success:
                        st.success("Analysis completed successfully!")
                        render_prediction_result(result)
                    else:
                        st.error(f"Analysis failed: {result}")
    
    else:
        # Instructions when no file uploaded
        st.markdown("""
        <div class="upload-section">
            <h3>Upload a clear image of your food to get started with AI-powered recognition and nutrition analysis.</h3>
            <p><strong>Tips for best results:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>Use well-lit, clear images</li>
                <li>Center the food in the frame</li>
                <li>Avoid multiple dishes in one image</li>
                <li>Higher resolution images work better</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar with additional information
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
        
        
        st.markdown("### Prediction Help")
        st.info("""
        **Supported Foods:**
        - 131 different food categories
        - International cuisine (101 dishes)  
        - Vietnamese dishes (30 dishes)
        - Various cooking styles and presentations
        """)
        
        st.markdown("### Nutrition Data")
        st.info("""
        **Provided Information:**
        - Calories per serving
        - Protein content (grams)
        - Fat content (grams)
        - Carbohydrate content (grams)
        - Fiber content (grams)
        """)
        
        st.markdown("### Performance")
        st.info("""
        **System Stats:**
        - ResNet50 deep learning model
        - ~1-3 seconds processing time
        - 224×224 input resolution
        - Automatic image preprocessing
        """)
        
        st.markdown("---")
        if st.button(" Back to Home"):
            st.switch_page("Overview.py")

        if st.button(" About Team"):
            st.switch_page("pages/2_AboutUs.py")

if __name__ == "__main__":
    main()
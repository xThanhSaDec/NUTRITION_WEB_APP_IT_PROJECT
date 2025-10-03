# 🍽️ Food Recognition & Nutrition Web Application

An advanced AI-powered web application that combines computer vision and nutritional science to identify food items from images and provide comprehensive nutritional information.

## 📖 Project Overview

This application uses a trained ResNet50 deep learning model to recognize 131 different food items (101 international dishes + 30 Vietnamese traditional dishes) and provides detailed nutritional analysis including calories, protein, fat, carbohydrates, and fiber content.

## 🏗️ Architecture

### Backend (FastAPI) - Port 8000

- **POST /api/predict**: Image upload and food recognition
- **GET /api/nutrition/{dish_name}**: Nutrition information retrieval
- **GET /api/aboutus**: Project and team information
- **Automatic API documentation**: Available at `/docs`

### Frontend (Streamlit) - Port 8501

- **Main Page** (`streamlit_app.py`): Introduction and navigation
- **Predict Page** (`pages/1_Predict.py`): Image upload and analysis
- **About Us Page** (`pages/2_AboutUs.py`): Team and project information

### ML Model

- **Architecture**: ResNet50 Convolutional Neural Network
- **Training**: Transfer learning on Food-101 + Vietnamese dishes dataset
- **Input**: 224×224×3 RGB images
- **Output**: 131 food categories with confidence scores

##Project Structure

```
foodapp/
│
├── backend/                         # FastAPI Backend
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── routes/
│   │   │   ├── predict.py           # Prediction endpoints
│   │   │   ├── nutrition.py         # Nutrition endpoints
│   │   │   └── aboutus.py           # About endpoints
│   │   ├── models/                  # Pydantic schemas
│   │   │   ├── predict_model.py
│   │   │   └── nutrition_model.py
│   │   ├── services/                # Business logic
│   │   │   ├── inference_service.py # ML model handling
│   │   │   └── nutrition_service.py # Nutrition database
│   │   └── ml_models/               # ML assets
│   │       ├── best_model_phase2.keras
│   │       └── final_class_mapping.json
│   └── requirements.txt
│
├── frontend/                        # Streamlit Frontend
│   ├── streamlit_app.py             # Main page
│   ├── pages/
│   │   ├── 1_Predict.py             # Prediction interface
│   │   └── 2_AboutUs.py             # Team information
│   └── requirements.txt
│
├── data/
│   └── nutrition_database.csv       # Nutrition database
│
└── README.md                        # This file
```

##Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- At least 4GB RAM (for ML model)

### 1. Clone Repository

```bash
git clone <repository-url>
cd foodapp
```

### 2. Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://127.0.0.1:8000

- API Documentation: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

### 3. Start Frontend Application (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pip install -r requirements.txt

# Start Streamlit app
streamlit run Overview.py --server.port 8501
#Start API routes
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```
Frontend will be available at: http://localhost:8501

## 🔧 Features

### AI-Powered Food Recognition

- **131 Food Categories**: 101 international + 30 Vietnamese dishes
- **High Accuracy**: ResNet50 deep learning architecture
- **Confidence Scores**: Prediction confidence with visual indicators
- **Top-3 Predictions**: Alternative predictions with confidence levels

### Comprehensive Nutrition Database

- **Detailed Information**: Calories, protein, fat, carbohydrates, fiber
- **Per Serving Values**: All nutritional values calculated per typical serving
- **Health Suggestions**: AI-generated dietary recommendations
- **Search & Compare**: Search dishes and compare nutritional values

### Modern Web Interface

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Processing**: Fast image analysis and results
- **Interactive UI**: Streamlit-powered user interface
- **Multi-page Navigation**: Organized content across multiple pages

### Developer-Friendly API

- **RESTful Design**: Clean and intuitive API endpoints
- **Auto Documentation**: Swagger/OpenAPI documentation
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Comprehensive error responses

## Technical Details

### Machine Learning

- **Model**: ResNet50 with custom classification head
- **Framework**: TensorFlow/Keras
- **Input Size**: 224×224×3 RGB images
- **Preprocessing**: Automatic resize and normalization
- **Fallback Strategy**: Multiple model loading approaches

### Backend Technology

- **Framework**: FastAPI with async support
- **API Documentation**: Automatic OpenAPI/Swagger generation
- **File Upload**: Multipart form data handling
- **Data Validation**: Pydantic models for request/response
- **CORS**: Cross-origin resource sharing enabled

### Frontend Technology

- **Framework**: Streamlit for rapid web app development
- **Multi-page**: Native Streamlit pages system
- **Responsive**: Mobile-friendly interface
- **Real-time**: Live API integration
- **Styling**: Custom CSS for enhanced UI

### Data Management

- **Nutrition Database**: CSV-based storage with Pandas processing
- **Class Mapping**: JSON file for model output interpretation
- **Caching**: Efficient data retrieval and model caching
- **Fuzzy Matching**: Intelligent dish name matching

## Usage Instructions

### For Users

1. **Start both servers** (backend and frontend)
2. **Navigate to frontend** at http://localhost:8501
3. **Go to Predict page** using sidebar navigation
4. **Upload food image** (JPG, PNG, JPEG - max 10MB)
5. **Click "Analyze Food"** to get results
6. **View results**: Food name, confidence, nutrition info, alternatives

### For Developers

1. **API Testing**: Use http://127.0.0.1:8000/docs for interactive testing
2. **Custom Integration**: Make HTTP requests to API endpoints
3. **Model Updates**: Replace `.keras` model file and class mapping
4. **Database Updates**: Modify `nutrition_database.csv` for new dishes

### Supported Formats

- **JPG/JPEG**: Recommended for photos
- **PNG**: Good for graphics and screenshots
- **Maximum size**: 10MB per image
- **Minimum resolution**: 64×64 pixels

## API Endpoints

### Prediction

- `POST /api/predict` - Upload image for food recognition
- `GET /api/predict/status` - Get prediction service status
- `GET /api/predict/test` - Test prediction endpoint

### Nutrition

- `GET /api/nutrition/{dish_name}` - Get nutrition info
- `GET /api/nutrition/search/dishes?query={term}` - Search dishes
- `GET /api/nutrition/database/summary` - Database statistics
- `GET /api/nutrition/compare?dishes={dish1,dish2}` - Compare nutrition

### Information

- `GET /api/aboutus` - HTML about page
- `GET /api/aboutus/json` - JSON project info
- `GET /api/aboutus/team` - Team member details

## Testing

### Manual Testing

1. **Health Check**: `curl http://127.0.0.1:8000/health`
2. **Image Upload**: Use frontend or API docs at `/docs`
3. **Nutrition Query**: `curl http://127.0.0.1:8000/api/nutrition/pho_bo`

### Automated Testing

```bash
# Backend tests (if implemented)
cd backend
python -m pytest

# Frontend testing through manual interaction
cd frontend
streamlit run streamlit_app.py
```

## 🔧 Troubleshooting

### Common Issues

**Backend won't start:**

- Check Python version (3.8+)
- Install requirements: `pip install -r requirements.txt`
- Check port 8000 availability

**Model loading fails:**

- Ensure `best_model_phase2.keras` exists in `backend/app/ml_models/`
- Check available memory (>4GB recommended)
- Verify TensorFlow installation

**Frontend can't connect:**

- Ensure backend is running on port 8000
- Check CORS settings in backend
- Verify network connectivity

**Prediction errors:**

- Check image format (JPG, PNG, JPEG)
- Verify image size (<10MB)
- Ensure image is not corrupted

### Performance Optimization

- **First prediction**: May be slower due to model loading
- **Subsequent predictions**: Cached model for faster processing
- **Memory usage**: Monitor system resources with large models
- **GPU acceleration**: Automatic if CUDA is available

## Development Team

- **Tran Dinh Khuong** (23110035) - Lead Developer & ML Engineer
- **Nguyen Nhat Phat** (23110053) - Backend Developer & API Engineer
- **Tran Huynh Xuan Thanh** (23110060) - Frontend Developer & UI/UX Designer

**Supervisor**: Assoc. Prof. Dr. Hoang Van Dung

## Project Statistics

- **Development Time**: 15 weeks
- **Food Categories**: 131 (101 international + 30 Vietnamese)
- **Model Parameters**: 23M+ parameters
- **API Endpoints**: 12 endpoints
- **Technologies Used**: 8+ frameworks and libraries

## Future Enhancements

- **Object Detection**: Multiple food items in one image
- **Mobile App**: iOS and Android applications
- **User Accounts**: Personal nutrition tracking
- **Recipe Integration**: Cooking instructions and ingredients
- **Barcode Scanning**: Packaged food recognition
- **Voice Commands**: Audio-based interaction

## License

This project is developed for academic purposes as part of a 15-week IT project course.

## Contributing

This is an academic project. For suggestions or issues, please contact the development team.

---

**Enjoy exploring the world of AI-powered food recognition and nutrition analysis!**

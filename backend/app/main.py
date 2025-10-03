"""
FastAPI Backend for Food Recognition and Nutrition Web Application
Main entry point for the API server
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from app.routes import predict, nutrition, aboutus

# Create FastAPI instance
app = FastAPI(
    title="Food Recognition & Nutrition API",
    description="API for food recognition using AI and nutrition information retrieval",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Environment configuration for free deployment
import os
ALLOWED_ORIGINS = [
    "https://*.streamlit.app",
    "http://localhost:8501", 
    "http://127.0.0.1:8501",
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api", tags=["Prediction"])
app.include_router(nutrition.router, prefix="/api", tags=["Nutrition"])
app.include_router(aboutus.router, prefix="/api", tags=["About"])

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    return """
    <html>
        <head>
            <title>Food Recognition API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; text-align: center; }
                .feature { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .endpoint { background: #3498db; color: white; padding: 10px; margin: 5px 0; border-radius: 5px; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .status { color: #27ae60; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Food Recognition & Nutrition API</h1>
                <p class="status">API Server Running Successfully</p>
                
                <h2>Available Endpoints:</h2>
                <div class="endpoint">POST /api/predict - Upload image for food recognition</div>
                <div class="endpoint">GET /api/nutrition/{dish_name} - Get nutrition information</div>
                <div class="endpoint">GET /api/aboutus - Get project information</div>

                <h2>API Documentation:</h2>
                <div class="feature">
                    <strong>Interactive Docs:</strong> <a href="/docs" target="_blank">FastAPI Swagger UI</a>
                </div>
                <div class="feature">
                    <strong>ReDoc:</strong> <a href="/redoc" target="_blank">Alternative Documentation</a>
                </div>

                <h2>Features:</h2>
                <div class="feature">
                    <strong>AI Food Recognition:</strong> Identifies 131 different food items using trained ResNet50 model
                </div>
                <div class="feature">
                    <strong>Nutrition Database:</strong> Comprehensive nutritional information for all recognized foods
                </div>
                <div class="feature">
                    <strong>CORS Enabled:</strong> Ready for frontend integration on port 8501
                </div>

                <h2>Usage:</h2>
                <p>This API is designed to work with the Streamlit frontend running on port 8501. 
                Upload food images to get AI-powered recognition and detailed nutrition information.</p>
                
                <p style="text-align: center; margin-top: 30px; color: #7f8c8d;">
                    Food Recognition & Nutrition Web Application<br>
                    Backend API Server v1.0.0
                </p>
            </div>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Food Recognition API is running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    print("Starting Food Recognition API Server...")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Homepage: http://127.0.0.1:8000")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
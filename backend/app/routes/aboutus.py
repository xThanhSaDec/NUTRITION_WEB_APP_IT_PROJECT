"""
FastAPI route for About Us information
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
import json

router = APIRouter()

@router.get("/aboutus", response_class=HTMLResponse)
async def get_about_us_html():
    """
    Get About Us information as HTML page
    
    - Returns: Formatted HTML with team and project information
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About Us - Food Recognition & Nutrition App</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 50px;
            }
            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
                margin-bottom: 5px;
            }
            .content {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .section {
                padding: 40px;
                border-bottom: 1px solid #f0f0f0;
            }
            .section:last-child {
                border-bottom: none;
            }
            .section h2 {
                color: #2c3e50;
                font-size: 1.8rem;
                margin-bottom: 20px;
            }
            .team-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin-top: 30px;
            }
            .team-member {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            .team-member:hover {
                transform: translateY(-5px);
            }
            .team-member h3 {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            .team-member p {
                color: #7f8c8d;
                margin-bottom: 5px;
            }
            .tech-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .tech-item {
                background: #ecf0f1;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .tech-item h4 {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            .features-list {
                list-style: none;
                padding: 0;
            }
            .features-list li {
                background: #f8f9fa;
                margin: 10px 0;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #3498db;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .stat-item {
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .stat-number {
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .footer {
                background: #2c3e50;
                color: white;
                text-align: center;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>NutriDish: AI Food Recognition & Nutrition App</h1>
                <p>Advanced Computer Vision for Food Recognition and Nutritional Analysis</p>
                <p>Supervisor: Assoc. Prof. Dr. Hoang Van Dung</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>Development Team</h2>
                    <div class="team-grid">
                        <div class="team-member">
                            <h3>Tran Dinh Khuong</h3>
                            <p><strong>Student ID:</strong> 23110035</p>
                            <p><strong>Role:</strong> Lead Developer & ML Engineer</p>
                            <p>Specialized in deep learning model development and system architecture</p>
                        </div>
                        <div class="team-member">
                            <h3>Nguyen Nhat Phat</h3>
                            <p><strong>Student ID:</strong> 23110053</p>
                            <p><strong>Role:</strong> Backend Developer & API Engineer</p>
                            <p>Expert in FastAPI development and database management</p>
                        </div>
                        <div class="team-member">
                            <h3>Tran Huynh Xuan Thanh</h3>
                            <p><strong>Student ID:</strong> 23110060</p>
                            <p><strong>Role:</strong> Frontend Developer & UI/UX Designer</p>
                            <p>Specialized in Streamlit applications and user experience design</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Project Overview</h2>
                    <p>The Food Recognition & Nutrition Web Application is an innovative project that combines artificial intelligence with nutritional science to help users identify food items and obtain detailed nutritional information. Our system uses advanced computer vision techniques to analyze food images and provide comprehensive dietary insights.</p>
                    
                    <h3>Key Objectives:</h3>
                    <ul class="features-list">
                        <li><strong>AI-Powered Recognition:</strong> Identify 131 different food items with high accuracy using ResNet50 deep learning architecture</li>
                        <li><strong>Comprehensive Database:</strong> Provide detailed nutritional information including calories, protein, fat, carbohydrates, and fiber content</li>
                        <li><strong>Food Diversity:</strong> Support both international cuisine (Food-101 dataset) and Vietnamese traditional dishes</li>
                        <li><strong>User-Friendly Interface:</strong> Deliver an intuitive web application for seamless user interaction</li>
                        <li><strong>Real-Time Processing:</strong> Ensure fast response times for practical daily use</li>
                    </ul>
                </div>
                
                <div class="section">
                    <h2>Technical Architecture</h2>
                    <div class="tech-grid">
                        <div class="tech-item">
                            <h4>Machine Learning</h4>
                            <p>ResNet50 Convolutional Neural Network</p>
                            <p>TensorFlow & Keras Framework</p>
                            <p>Transfer Learning Techniques</p>
                        </div>
                        <div class="tech-item">
                            <h4>Backend API</h4>
                            <p>FastAPI Framework</p>
                            <p>RESTful API Design</p>
                            <p>Async Request Processing</p>
                        </div>
                        <div class="tech-item">
                            <h4>Frontend Interface</h4>
                            <p>Streamlit Framework</p>
                            <p>Responsive Web Design</p>
                            <p>Interactive Data Visualization</p>
                        </div>
                        <div class="tech-item">
                            <h4>Data Management</h4>
                            <p>CSV-based Nutrition Database</p>
                            <p>JSON Class Mapping</p>
                            <p>Efficient Data Retrieval</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Project Statistics</h2>
                    <div class="stats">
                        <div class="stat-item">
                            <div class="stat-number">131</div>
                            <div>Food Categories</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">101</div>
                            <div>International Dishes</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">30</div>
                            <div>Vietnamese Dishes</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">224×224</div>
                            <div>Input Resolution</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Innovation & Impact</h2>
                    <p>This project represents a significant advancement in the intersection of computer vision and nutritional science. By leveraging state-of-the-art deep learning techniques, we've created a practical solution that can help users make informed dietary decisions.</p>
                    
                    <h3>Potential Applications:</h3>
                    <ul class="features-list">
                        <li><strong>Personal Health Management:</strong> Help individuals track their daily nutritional intake</li>
                        <li><strong>Restaurant Industry:</strong> Assist restaurants in providing accurate nutritional information</li>
                        <li><strong>Healthcare Systems:</strong> Support dietitians and nutritionists in patient consultation</li>
                        <li><strong>Educational Tools:</strong> Teach students about nutrition through interactive technology</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <p>15-Week IT Project - Advanced Computer Vision and Web Development</p>
                <p>2025 Food Recognition & Nutrition</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@router.get("/aboutus/json")
async def get_about_us_json():
    """
    Get About Us information as JSON data
    
    - Returns: Structured JSON with team and project information
    """
    about_data = {
        "project": {
            "title": "NutriDish: AI Food Recognition & Nutrition Web Application",
            "description": "Advanced Computer Vision for Food Recognition and Nutritional Analysis",
            "supervisor": "Assoc. Prof. Dr. Hoang Van Dung",
            "duration": "15 weeks",
            "academic_year": "2025"
        },
        "team_members": [
            {
                "name": "Tran Dinh Khuong",
                "student_id": "23110035",
                "role": "Lead Developer & ML Engineer",
                "specialization": "Deep learning model development and system architecture",
                "responsibilities": [
                    "ResNet50 model training and optimization",
                    "System architecture design",
                    "Model deployment and integration"
                ]
            },
            {
                "name": "Nguyen Nhat Phat", 
                "student_id": "23110053",
                "role": "Backend Developer & API Engineer",
                "specialization": "FastAPI development and database management",
                "responsibilities": [
                    "RESTful API development",
                    "Database design and management",
                    "Backend service optimization"
                ]
            },
            {
                "name": "Tran Huynh Xuan Thanh",
                "student_id": "23110060", 
                "role": "Frontend Developer & UI/UX Designer",
                "specialization": "Streamlit applications and user experience design",
                "responsibilities": [
                    "User interface design",
                    "Frontend development",
                    "User experience optimization"
                ]
            }
        ],
        "technical_stack": {
            "machine_learning": {
                "model": "ResNet50 Convolutional Neural Network",
                "framework": "TensorFlow & Keras",
                "technique": "Transfer Learning",
                "input_size": "224x224x3",
                "classes": 131
            },
            "backend": {
                "framework": "FastAPI",
                "architecture": "RESTful API",
                "processing": "Asynchronous",
                "documentation": "OpenAPI/Swagger"
            },
            "frontend": {
                "framework": "Streamlit",
                "design": "Responsive Web Design",
                "features": "Interactive Data Visualization"
            },
            "data": {
                "nutrition_db": "CSV-based Database",
                "class_mapping": "JSON Format",
                "storage": "File-based System"
            }
        },
        "project_statistics": {
            "total_food_categories": 131,
            "international_dishes": 101,
            "vietnamese_dishes": 30,
            "input_resolution": "224x224",
            "model_parameters": "23M+",
            "supported_formats": ["JPG", "JPEG", "PNG"]
        },
        "features": [
            {
                "category": "AI Recognition",
                "description": "High-accuracy food identification using deep learning",
                "details": "ResNet50-based model trained on Food-101 + Vietnamese dishes"
            },
            {
                "category": "Nutrition Analysis", 
                "description": "Comprehensive nutritional information",
                "details": "Calories, protein, fat, carbohydrates, and fiber content"
            },
            {
                "category": "Cultural Diversity",
                "description": "Support for multiple cuisines",
                "details": "International and Vietnamese traditional dishes"
            },
            {
                "category": "Real-time Processing",
                "description": "Fast image analysis and response",
                "details": "Optimized for practical daily use"
            }
        ],
        "applications": [
            "Personal health and nutrition tracking",
            "Restaurant nutritional information systems", 
            "Healthcare and dietitian consultation tools",
            "Educational nutrition learning platforms",
            "Food logging and diary applications"
        ],
        "api_info": {
            "version": "1.0.0",
            "endpoints": {
                "prediction": "/api/predict",
                "nutrition": "/api/nutrition/{dish_name}",
                "about": "/api/aboutus"
            },
            "documentation": "/docs"
        },
        "contact": {
            "institution": "University",
            "course": "IT Project",
            "year": 2024,
            "github": "https://github.com/nutrition-app"
        }
    }
    
    return JSONResponse(content=about_data)

@router.get("/aboutus/team")
async def get_team_info():
    """
    Get detailed team member information
    
    - Returns: Team member details and contributions
    """
    team_info = {
        "team_size": 3,
        "roles_distribution": {
            "machine_learning": 1,
            "backend_development": 1, 
            "frontend_development": 1
        },
        "members": [
            {
                "id": 1,
                "name": "Tran Dinh Khuong",
                "student_id": "23110035",
                "primary_role": "Train and evaluate ML models",
                "skills": [
                    "Deep Learning",
                    "TensorFlow/Keras",
                    "Computer Vision",
                    "Python Programming",
                    "Model Optimization"
                ],
                "contributions": [
                    "ResNet50 model architecture design",
                    "Training pipeline development",
                    "Model evaluation and optimization",
                    "Integration with backend services"
                ]
            },
            {
                "id": 2,
                "name": "Nguyen Nhat Phat",
                "student_id": "23110053", 
                "primary_role": "Preparing and preprocessing data for model training",
                "skills": [
                    "FastAPI Development",
                    "RESTful API Design",
                    "Database Management",
                    "Async Programming",
                    "API Documentation"
                ],
                "contributions": [
                    "FastAPI application architecture",
                    "RESTful endpoints implementation",
                    "Database design and optimization",
                    "API documentation and testing"
                ]
            },
            {
                "id": 3,
                "name": "Tran Huynh Xuan Thanh",
                "student_id": "23110060",
                "primary_role": "Website application and deployment", 
                "skills": [
                    "Streamlit Development",
                    "UI/UX Design",
                    "Web Technologies",
                    "User Experience",
                    "Responsive Design"
                ],
                "contributions": [
                    "Streamlit application development",
                    "User interface design",
                    "User experience optimization",
                    "Frontend-backend integration"
                ]
            }
        ],
        "collaboration_tools": [
            "GitHub for version control",
            "VS Code for development",
            "Discord for communication",
            "Google Drive for documentation"
        ]
    }
    
    return JSONResponse(content=team_info)
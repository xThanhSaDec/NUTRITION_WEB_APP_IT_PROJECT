"""
Pydantic models for prediction requests and responses
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from PIL import Image

class PredictionResponse(BaseModel):
    """Response model for food prediction"""
    success: bool = Field(..., description="Whether prediction was successful")
    food_name: str = Field(..., description="Predicted food name")
    class_name: str = Field(..., description="Internal class name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence (0-1)")
    nutrition: Dict[str, Any] = Field(..., description="Nutrition information")
    top_3_predictions: List[Dict[str, Any]] = Field(default=[], description="Top 3 predictions with confidence")
    bounding_box: Optional[Dict[str, int]] = Field(None, description="Bounding box coordinates (if available)")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    model_info: Optional[str] = Field(None, description="Model information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "food_name": "Phở Bò",
                "class_name": "pho_bo",
                "confidence": 0.89,
                "nutrition": {
                    "calories": 350,
                    "protein": 12.0,
                    "fat": 5.0,
                    "carbs": 58.0,
                    "fiber": 2.0
                },
                "top_3_predictions": [
                    {
                        "class_id": 125,
                        "class_name": "pho_bo",
                        "name": "Phở Bò",
                        "confidence": 0.89
                    },
                    {
                        "class_id": 124,
                        "class_name": "pho_ga",
                        "name": "Phở Gà", 
                        "confidence": 0.07
                    }
                ],
                "bounding_box": {
                    "x": 50,
                    "y": 60,
                    "width": 200,
                    "height": 180
                },
                "processing_time": 1.23,
                "model_info": "ResNet50 trained model"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Invalid image format. Please upload JPG, PNG, or JPEG file.",
                "error_code": "INVALID_IMAGE_FORMAT",
                "details": {
                    "supported_formats": ["jpg", "jpeg", "png"],
                    "uploaded_format": "gif"
                }
            }
        }

class UploadImageRequest(BaseModel):
    """Request model for image upload (for documentation purposes)"""
    file: bytes = Field(..., description="Image file (multipart/form-data)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "file": "Binary image data (JPG/PNG/JPEG format)"
            }
        }
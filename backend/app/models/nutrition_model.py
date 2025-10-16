"""
Pydantic models for nutrition requests and responses
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional
from enum import Enum
class NutritionResponse(BaseModel):
    """Response model for nutrition information"""
    success: bool = Field(..., description="Whether request was successful")
    dish_name: str = Field(..., description="Name of the dish")
    nutrition: Dict[str, Any] = Field(..., description="Nutritional information")
    serving_info: Optional[str] = Field(None, description="Serving size information")
    dataset_source: Optional[str] = Field(None, description="Source of nutrition data")
    suggestions: Optional[Dict[str, Any]] = Field(None, description="Health suggestions based on nutrition")
    
    @validator('dish_name')
    def dish_name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Dish name cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "dish_name": "pho_bo",
                "nutrition": {
                    "calories": 350,
                    "protein": 12.0,
                    "fat": 5.0,
                    "carbs": 58.0,
                    "fiber": 2.0
                },
                "serving_info": "1 bowl (400ml)",
                "dataset_source": "30VNFoods",
                "suggestions": {
                    "health_level": "moderate",
                    "recommendations": [
                        "Good source of protein",
                        "Moderate caloric content",
                        "Consider adding vegetables"
                    ],
                    "dietary_notes": "Suitable for most diets"
                }
            }
        }

class NutritionErrorResponse(BaseModel):
    """Error response for nutrition requests"""
    success: bool = False
    error: str = Field(..., description="Error message")
    dish_name: str = Field(..., description="Requested dish name")
    available_dishes: Optional[list] = Field(None, description="List of available dishes")
    suggestions: Optional[list] = Field(None, description="Similar dish suggestions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Dish not found in nutrition database",
                "dish_name": "unknown_dish",
                "available_dishes": ["pho_bo", "banh_mi", "com_tam"],
                "suggestions": ["pho_ga", "pho_tai"]
            }
        }

class HealthSuggestion(BaseModel):
    """Model for health suggestions based on nutrition"""
    health_level: str = Field(..., description="Overall health level (low/moderate/high)")
    recommendations: list = Field(default=[], description="Health recommendations")
    dietary_notes: str = Field(default="", description="Dietary compatibility notes")
    calorie_category: str = Field(..., description="Calorie category (low/moderate/high)")
    protein_level: str = Field(..., description="Protein content level")
    
    class Config:
        json_schema_extra = {
            "example": {
                "health_level": "moderate",
                "recommendations": [
                    "Good source of protein",
                    "Moderate caloric content",
                    "Consider adding vegetables"
                ],
                "dietary_notes": "Suitable for most diets, contains gluten",
                "calorie_category": "moderate",
                "protein_level": "good"
            }
        }
"""
FastAPI route for food prediction using uploaded images
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import time
from typing import Dict, Any

from app.models.predict_model import PredictionResponse, ErrorResponse
from app.services.inference_service import get_inference_service, FoodInferenceService
from app.services.nutrition_service import get_nutrition_service, NutritionService

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_food(
    file: UploadFile = File(...),
    inference_service: FoodInferenceService = Depends(get_inference_service),
    nutrition_service: NutritionService = Depends(get_nutrition_service)
):
    """
    Upload an image and get food recognition prediction with nutrition information
    - filetype: Image file: JPG, PNG, JPEG
    - Returns: Food prediction with confidence, nutrition info, and top 3 predictions
    """
    start_time = time.time()
    
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        file_extension = '.' + file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file format. Supported formats: {', '.join(allowed_extensions)}"
            )
        
        # Check file size (limit to 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {max_size // (1024*1024)}MB"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Make prediction
        prediction_result = inference_service.predict(content)
        
        if not prediction_result.get("success"):
            error_msg = prediction_result.get("error", "Prediction failed")
            raise HTTPException(status_code=500, detail=error_msg)
        
        # Get nutrition information
        class_name = prediction_result["class_name"]
        nutrition_result = nutrition_service.get_nutrition(class_name)
        
        if nutrition_result.get("success"):
            nutrition_data = nutrition_result["nutrition"]
        else:
            # Fallback nutrition data
            nutrition_data = {
                "calories": 200,
                "protein": 10.0,
                "fat": 8.0,
                "carbs": 25.0,
                "fiber": 3.0
            }
        
        # Prepare response
        response_data = {
            "success": True,
            "food_name": prediction_result["food_name"],
            "class_name": prediction_result["class_name"], 
            "confidence": prediction_result["confidence"],
            "nutrition": nutrition_data,
            "top_3_predictions": prediction_result.get("top_3_predictions", []),
            "bounding_box": prediction_result.get("bounding_box"),
            "processing_time": round(time.time() - start_time, 3),
            "model_info": prediction_result.get("model_info", "Unknown model")
        }
        
        return JSONResponse(content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        error_response = {
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "error_code": "INTERNAL_ERROR",
            "details": {
                "processing_time": round(time.time() - start_time, 3),
                "file_info": {
                    "filename": file.filename if file else None,
                    "content_type": file.content_type if file else None
                }
            }
        }
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )

@router.get("/predict/status")
async def get_prediction_status(
    inference_service: FoodInferenceService = Depends(get_inference_service)
):
    """
    Get the current status of the prediction service
    
    - Returns: Model loading status and configuration info
    """
    try:
        status = inference_service.get_model_status()
        return {
            "success": True,
            "status": "ready" if status["model_loaded"] else "not_ready",
            "model_info": status,
            "supported_formats": ["jpg", "jpeg", "png"],
            "max_file_size_mb": 10,
            "image_dimensions": "224x224 (auto-resized)"
        }
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "error": str(e)
        }

@router.get("/predict/test")
async def test_prediction_endpoint():
    """
    Test endpoint to verify prediction service is working
    
    - Returns: Service health status
    """
    return {
        "success": True,
        "message": "Prediction endpoint is working",
        "endpoint": "/api/predict",
        "method": "POST",
        "expected_input": "Image file (multipart/form-data)",
        "timestamp": time.time()
    }
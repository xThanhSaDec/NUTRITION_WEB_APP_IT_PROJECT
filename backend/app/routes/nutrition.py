"""
FastAPI route for nutrition information retrieval
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List, Optional

from app.models.nutrition_model import NutritionResponse, NutritionErrorResponse
from app.services.nutrition_service import get_nutrition_service, NutritionService

router = APIRouter()

@router.get("/nutrition/{dish_name}", response_model=NutritionResponse)
async def get_nutrition_info(
    dish_name: str,
    nutrition_service: NutritionService = Depends(get_nutrition_service)
):
    """
    Get detailed nutrition information for a specific dish
    
    - **dish_name**: Name of the dish (e.g., "pho_bo", "pizza", "banh_mi")
    - Returns: Comprehensive nutrition data including calories, protein, fat, carbs, and health suggestions
    """
    try:
        # Get nutrition data from service
        result = nutrition_service.get_nutrition(dish_name)
        
        if result.get("success"):
            return JSONResponse(content=result)
        else:
            # Dish not found
            error_response = {
                "success": False,
                "error": result.get("error", "Dish not found"),
                "dish_name": dish_name,
                "available_dishes": result.get("available_dishes", []),
                "suggestions": result.get("suggestions", [])
            }
            
            return JSONResponse(
                status_code=404,
                content=error_response
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Internal server error: {str(e)}",
                "dish_name": dish_name
            }
        )

@router.get("/nutrition/search/dishes")
async def search_dishes(
    query: str = Query(..., min_length=1, description="Search query for dish names"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    nutrition_service: NutritionService = Depends(get_nutrition_service)
):
    """
    Search for dishes by name
    
    - **query**: Search term to find matching dish names
    - **limit**: Maximum number of results to return (1-50)
    - Returns: List of matching dish names
    """
    try:
        matching_dishes = nutrition_service.search_dishes(query, limit)
        
        return {
            "success": True,
            "query": query,
            "matches_found": len(matching_dishes),
            "dishes": matching_dishes,
            "total_available": len(nutrition_service.get_all_dishes())
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Search failed: {str(e)}",
                "query": query
            }
        )

@router.get("/nutrition/database/summary")
async def get_database_summary(
    nutrition_service: NutritionService = Depends(get_nutrition_service)
):
    """
    Get summary information about the nutrition database
    
    - Returns: Database statistics and sample dishes
    """
    try:
        summary = nutrition_service.get_nutrition_summary()
        return {
            "success": True,
            "database_info": summary,
            "endpoints": {
                "get_nutrition": "/api/nutrition/{dish_name}",
                "search_dishes": "/api/nutrition/search/dishes?query={search_term}",
                "list_all": "/api/nutrition/database/list"
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Failed to get database summary: {str(e)}"
            }
        )

@router.get("/nutrition/database/list")
async def list_all_dishes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of dishes per page"),
    nutrition_service: NutritionService = Depends(get_nutrition_service)
):
    """
    Get paginated list of all available dishes
    
    - **page**: Page number (starting from 1)
    - **page_size**: Number of dishes per page (1-100)
    - Returns: Paginated list of dish names
    """
    try:
        all_dishes = nutrition_service.get_all_dishes()
        total_dishes = len(all_dishes)
        
        # Calculate pagination
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        page_dishes = all_dishes[start_index:end_index]
        
        total_pages = (total_dishes + page_size - 1) // page_size
        
        return {
            "success": True,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_dishes": total_dishes,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            },
            "dishes": page_dishes
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Failed to list dishes: {str(e)}",
                "pagination": {
                    "current_page": page,
                    "page_size": page_size
                }
            }
        )

@router.get("/nutrition/compare")
async def compare_nutrition(
    dishes: str = Query(..., description="Comma-separated list of dish names to compare"),
    nutrition_service: NutritionService = Depends(get_nutrition_service)
):
    """
    Compare nutrition information between multiple dishes
    
    - **dishes**: Comma-separated dish names (e.g., "pho_bo,pizza,salad")
    - Returns: Side-by-side nutrition comparison
    """
    try:
        dish_list = [dish.strip() for dish in dishes.split(',')]
        
        if len(dish_list) > 5:
            raise HTTPException(
                status_code=400,
                detail="Maximum 5 dishes can be compared at once"
            )
        
        comparison_results = {}
        successful_dishes = []
        failed_dishes = []
        
        for dish in dish_list:
            result = nutrition_service.get_nutrition(dish)
            if result.get("success"):
                comparison_results[dish] = result["nutrition"]
                successful_dishes.append(dish)
            else:
                failed_dishes.append({
                    "dish": dish,
                    "error": result.get("error", "Not found")
                })
        
        if not successful_dishes:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "No valid dishes found for comparison",
                    "failed_dishes": failed_dishes
                }
            )
        
        return {
            "success": True,
            "comparison": comparison_results,
            "successful_dishes": successful_dishes,
            "failed_dishes": failed_dishes,
            "comparison_count": len(successful_dishes)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Comparison failed: {str(e)}",
                "requested_dishes": dishes.split(',') if dishes else []
            }
        )
"""
Nutrition Service for retrieving nutritional information from CSV database
"""
import pandas as pd
import os
from typing import Dict, Any, Optional, List
import difflib

class NutritionService:
    """Service for managing nutrition database and queries"""
    
    def __init__(self, csv_path: str = None):
        self.csv_path = csv_path or "../../data/nutrition_database.csv"
        self.nutrition_df = None
        self.dishes_dict = {}
        self._load_nutrition_database()
    
    def _load_nutrition_database(self):
        """Load nutrition data from CSV file"""
        try:
            # Try multiple possible paths
            possible_paths = [
                self.csv_path,
                "data/nutrition_database.csv",
                "../data/nutrition_database.csv", 
                "../../data/nutrition_database.csv",
                "app/data/nutrition_database.csv"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.nutrition_df = pd.read_csv(path)
                    print(f"Loaded nutrition database from: {path}")
                    break
            else:
                print("Nutrition database CSV not found, creating default data")
                self._create_default_nutrition_data()
                return
            
            # Convert to dictionary for faster lookups
            self.dishes_dict = {}
            for _, row in self.nutrition_df.iterrows():
                dish_name = row['dish_name']
                self.dishes_dict[dish_name] = {
                    'calories': float(row['calories']),
                    'protein': float(row['protein']),
                    'fat': float(row['fat']),
                    'carbs': float(row['carbs']),
                    'serving': row.get('serving', '1 serving'),
                    'dataset_source': row.get('dataset_source', 'Unknown')
                }
            
            print(f"Loaded nutrition data for {len(self.dishes_dict)} dishes")
            
        except Exception as e:
            print(f"Error loading nutrition database: {e}")
            self._create_default_nutrition_data()
    
    def _create_default_nutrition_data(self):
        """Create default nutrition data if CSV not found"""
        print("Creating default nutrition database...")
        
        # Default nutrition data for common dishes
        default_data = {
            # Vietnamese dishes
            "banh_mi": {"calories": 400, "protein": 18, "fat": 12, "carbs": 55, "serving": "1 sandwich"},
            "pho_bo": {"calories": 350, "protein": 12, "fat": 5, "carbs": 58, "serving": "1 bowl"},
            "pho_ga": {"calories": 320, "protein": 15, "fat": 4, "carbs": 52, "serving": "1 bowl"},
            "bun_bo_hue": {"calories": 380, "protein": 14, "fat": 8, "carbs": 60, "serving": "1 bowl"},
            "com_tam": {"calories": 450, "protein": 20, "fat": 15, "carbs": 65, "serving": "1 plate"},
            "banh_xeo": {"calories": 320, "protein": 12, "fat": 18, "carbs": 30, "serving": "1 piece"},
            "goi_cuon": {"calories": 120, "protein": 8, "fat": 2, "carbs": 20, "serving": "2 rolls"},
            
            # International dishes
            "pizza": {"calories": 285, "protein": 12, "fat": 10, "carbs": 36, "serving": "1 slice"},
            "burger": {"calories": 540, "protein": 25, "fat": 31, "carbs": 40, "serving": "1 burger"},
            "sushi": {"calories": 200, "protein": 9, "fat": 7, "carbs": 28, "serving": "6 pieces"},
            "pasta": {"calories": 220, "protein": 8, "fat": 1, "carbs": 44, "serving": "1 cup"},
            "salad": {"calories": 150, "protein": 5, "fat": 10, "carbs": 12, "serving": "1 bowl"},
            "fried_rice": {"calories": 238, "protein": 6, "fat": 8, "carbs": 36, "serving": "1 cup"},
            "chicken_curry": {"calories": 280, "protein": 25, "fat": 15, "carbs": 12, "serving": "1 cup"},
            "fish_and_chips": {"calories": 585, "protein": 32, "fat": 30, "carbs": 45, "serving": "1 serving"},
            "apple_pie": {"calories": 237, "protein": 2.4, "fat": 11, "carbs": 34, "serving": "1 slice"},
            "chocolate_cake": {"calories": 352, "protein": 5, "fat": 14, "carbs": 56, "serving": "1 slice"}
        }
        
        # Add dataset source
        for dish in default_data:
            default_data[dish]["dataset_source"] = "Default"
        
        self.dishes_dict = default_data
        print(f"Created default nutrition data for {len(default_data)} dishes")
    
    def get_nutrition(self, dish_name: str) -> Dict[str, Any]:
        """Get nutrition information for a specific dish"""
        # Normalize dish name (lowercase, replace spaces with underscores)
        normalized_name = dish_name.lower().replace(' ', '_').replace('-', '_')
        
        # Direct lookup
        if normalized_name in self.dishes_dict:
            nutrition_data = self.dishes_dict[normalized_name].copy()
            return {
                "success": True,
                "dish_name": normalized_name,
                "nutrition": {
                    "calories": nutrition_data["calories"],
                    "protein": nutrition_data["protein"],
                    "fat": nutrition_data["fat"],
                    "carbs": nutrition_data["carbs"],
                    "fiber": nutrition_data.get("fiber", 2.0)  # Default fiber value
                },
                "serving_info": nutrition_data.get("serving", "1 serving"),
                "dataset_source": nutrition_data.get("dataset_source", "Unknown"),
                "suggestions": self._get_health_suggestions(nutrition_data)
            }
        
        # Try fuzzy matching
        similar_dishes = self._find_similar_dishes(normalized_name, limit=3)
        
        if similar_dishes:
            # Use the closest match
            closest_match = similar_dishes[0]
            nutrition_data = self.dishes_dict[closest_match].copy()
            
            return {
                "success": True,
                "dish_name": closest_match,
                "nutrition": {
                    "calories": nutrition_data["calories"],
                    "protein": nutrition_data["protein"],
                    "fat": nutrition_data["fat"], 
                    "carbs": nutrition_data["carbs"],
                    "fiber": nutrition_data.get("fiber", 2.0)
                },
                "serving_info": nutrition_data.get("serving", "1 serving"),
                "dataset_source": nutrition_data.get("dataset_source", "Unknown"),
                "suggestions": self._get_health_suggestions(nutrition_data),
                "match_info": f"Closest match for '{dish_name}'"
            }
        
        # No match found
        return {
            "success": False,
            "error": f"Nutrition information not found for '{dish_name}'",
            "dish_name": dish_name,
            "available_dishes": list(self.dishes_dict.keys())[:20],  # First 20 dishes
            "suggestions": self._find_similar_dishes(normalized_name, limit=5)
        }
    
    def _find_similar_dishes(self, dish_name: str, limit: int = 5) -> List[str]:
        """Find similar dish names using fuzzy matching"""
        try:
            available_dishes = list(self.dishes_dict.keys())
            # Use difflib to find similar matches
            similar = difflib.get_close_matches(dish_name, available_dishes, n=limit, cutoff=0.3)
            return similar
        except Exception:
            return []
    
    def _get_health_suggestions(self, nutrition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate health suggestions based on nutrition data"""
        calories = nutrition_data.get("calories", 0)
        protein = nutrition_data.get("protein", 0)
        fat = nutrition_data.get("fat", 0)
        carbs = nutrition_data.get("carbs", 0)
        
        recommendations = []
        
        # Calorie analysis
        if calories < 200:
            calorie_category = "low"
            recommendations.append("Light meal - consider pairing with other dishes")
        elif calories < 400:
            calorie_category = "moderate"
            recommendations.append("Moderate caloric content - suitable for most meal plans")
        else:
            calorie_category = "high"
            recommendations.append("High caloric content - consider portion control")
        
        # Protein analysis
        if protein >= 15:
            protein_level = "excellent"
            recommendations.append("Excellent source of protein")
        elif protein >= 8:
            protein_level = "good"
            recommendations.append("Good source of protein")
        else:
            protein_level = "low"
            recommendations.append("Consider adding protein-rich foods")
        
        # Fat analysis
        if fat > 20:
            recommendations.append("High fat content - balance with vegetables")
        elif fat < 5:
            recommendations.append("Low fat content - good for low-fat diets")
        
        # Carb analysis
        if carbs > 50:
            recommendations.append("High carbohydrate content - good for energy")
        elif carbs < 15:
            recommendations.append("Low carbohydrate content - suitable for low-carb diets")
        
        # Overall health level
        health_score = 0
        if calories <= 400: health_score += 1
        if protein >= 10: health_score += 1  
        if fat <= 15: health_score += 1
        if carbs <= 50: health_score += 1
        
        if health_score >= 3:
            health_level = "high"
        elif health_score >= 2:
            health_level = "moderate"
        else:
            health_level = "low"
        
        return {
            "health_level": health_level,
            "recommendations": recommendations,
            "dietary_notes": "Nutritional values are estimates per serving",
            "calorie_category": calorie_category,
            "protein_level": protein_level
        }
    
    def get_all_dishes(self) -> List[str]:
        """Get list of all available dishes"""
        return list(self.dishes_dict.keys())
    
    def search_dishes(self, query: str, limit: int = 10) -> List[str]:
        """Search for dishes matching query"""
        query_lower = query.lower()
        matching_dishes = []
        
        for dish in self.dishes_dict.keys():
            if query_lower in dish.lower():
                matching_dishes.append(dish)
        
        return matching_dishes[:limit]
    
    def get_nutrition_summary(self) -> Dict[str, Any]:
        """Get summary statistics of nutrition database"""
        if not self.dishes_dict:
            return {"error": "No nutrition data loaded"}
        
        total_dishes = len(self.dishes_dict)
        avg_calories = sum(dish["calories"] for dish in self.dishes_dict.values()) / total_dishes
        avg_protein = sum(dish["protein"] for dish in self.dishes_dict.values()) / total_dishes
        
        return {
            "total_dishes": total_dishes,
            "average_calories": round(avg_calories, 1),
            "average_protein": round(avg_protein, 1),
            "database_status": "loaded",
            "sample_dishes": list(self.dishes_dict.keys())[:10]
        }

# Global nutrition service instance
nutrition_service = None

def get_nutrition_service() -> NutritionService:
    """Get or create nutrition service instance (singleton pattern)"""
    global nutrition_service
    if nutrition_service is None:
        nutrition_service = NutritionService()
    return nutrition_service
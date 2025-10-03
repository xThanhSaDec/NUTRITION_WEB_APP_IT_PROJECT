"""
ML Inference Service for Food Recognition
Handles model loading, image preprocessing, and prediction
"""
import os
import json
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
# from tensorflow.keras.applications import ResNet50
# from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
# from tensorflow.keras.models import Model
from PIL import Image
import io
from typing import Tuple, Dict, Any, Optional
from tensorflow.keras.applications.resnet50 import preprocess_input

class FoodInferenceService:
    """Service for food recognition using trained ML model"""
    
    def __init__(self, model_path: str = None, class_mapping_path: str = None):
        # self.model_path = model_path or "app/ml_models/best_model_phase2.keras"
        # self.class_mapping_path = class_mapping_path or "app/ml_models/final_class_mapping.json"
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.model_path = model_path or os.path.join(base_dir, "ml_models", "best_model_phase2.keras")
        self.class_mapping_path = class_mapping_path or os.path.join(base_dir, "ml_models", "final_class_mapping.json")
        self.model = None
        self.class_mapping = {}
        self.model_type = None
        self.img_height = 224
        self.img_width = 224
        
        # Load class mapping
        self._load_class_mapping()
        
        # Load model
        self._load_model()
    
    def _load_class_mapping(self):
        """Load class mapping from JSON file"""
        try:
            if os.path.exists(self.class_mapping_path):
                with open(self.class_mapping_path, 'r', encoding='utf-8') as f:
                    raw_mapping = json.load(f)
                # Convert string keys to integers
                self.class_mapping = {int(k): v for k, v in raw_mapping.items()}
                print(f"Loaded class mapping with {len(self.class_mapping)} classes")
            else:
                print(f"Class mapping file not found: {self.class_mapping_path}")
                # Create default mapping
                self.class_mapping = {i: f"class_{i}" for i in range(131)}
        except Exception as e:
            print(f"Error loading trained model: {e}")

            self.class_mapping = {i: f"class_{i}" for i in range(131)}

    
    def _load_model(self):
        print("Loading ML model...")
        print(f"🔍 DEBUG - Model path: {self.model_path}")
        print(f"🔍 DEBUG - Current working directory: {os.getcwd()}")
        print(f"🔍 DEBUG - Model exists: {os.path.exists(self.model_path)}")
        print(f"🔍 DEBUG - Absolute model path: {os.path.abspath(self.model_path)}")
        if os.path.exists(self.model_path):
            try:
                print(f"Found model file: {self.model_path}")
                # self.model = keras.models.load_model(self.model_path, compile=False)
                custom_objects = {'preprocess_input': preprocess_input}
                self.model = keras.models.load_model(self.model_path, compile=False, custom_objects=custom_objects)
                print("Successfully loaded trained model")
                
                # console.log(f"Model summary:\n{self.model.summary()}")
                
                # Test prediction
                test_input = tf.random.normal((1, self.img_height, self.img_width, 3))
                _ = self.model.predict(test_input, verbose=0)
                print("Model prediction test successful")
                self.model_type = "trained_model"
                return
                
            except Exception as e:
                print(f"Error loading trained model: {e}")
        

    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """Preprocess image for model input"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            # Convert to RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image = image.resize((self.img_width, self.img_height))
            
            # Convert to numpy array
            image_array = np.array(image)
            
            # image_array = image_array.astype(np.float32) / 255.0
            image_array = image_array.astype(np.float32) # Keep [0,255] range for preprocess_input
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            raise ValueError(f"Error preprocessing image: {str(e)}")
    
    def predict(self, image_bytes: bytes) -> Dict[str, Any]:
        """Make prediction on uploaded image"""
        start_time = time.time()
        
        try:
            if self.model is None:
                raise RuntimeError("Model not loaded")
            # Preprocess image
            processed_image = self.preprocess_image(image_bytes)
            
            # Make prediction //Checkpoint
            predictions = self.model.predict(processed_image, verbose=0)
            
            if predictions is None or len(predictions) == 0:
                raise RuntimeError("No predictions returned from model")
            
            # Get prediction results
            pred = predictions[0]
            
            # Get top 3 predictions
            top_indices = np.argsort(pred)[-3:][::-1]
            top_confidences = pred[top_indices]
            
            # Build top predictions list
            top_predictions = []
            for idx, confidence in zip(top_indices, top_confidences):
                class_name = self.class_mapping.get(idx, f"class_{idx}")
                display_name = self._get_display_name(class_name)
                
                top_predictions.append({
                    "class_id": int(idx),
                    "class_name": class_name,
                    "name": display_name,
                    "confidence": float(confidence)
                })
            
            # Main prediction
            main_prediction = top_predictions[0]
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare result
            result = {
                "success": True,
                "food_name": main_prediction["name"],
                "class_name": main_prediction["class_name"],
                "confidence": main_prediction["confidence"],
                "top_3_predictions": top_predictions,
                "processing_time": round(processing_time, 3),
                "model_info": self._get_model_info(),
                "bounding_box": self._generate_dummy_bbox()  # Dummy bounding box
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Prediction failed: {str(e)}",
                "processing_time": time.time() - start_time
            }
    
    def _get_display_name(self, class_name: str) -> str:
        """Convert class name to display name"""
        # Handle Vietnamese dishes
        vietnamese_mapping = {
            "banh_beo": "Bánh Bèo",
            "banh_bot_loc": "Bánh Bột Lọc", 
            "banh_can": "Bánh Căn",
            "banh_canh": "Bánh Canh",
            "banh_chung": "Bánh Chưng",
            "banh_cuon": "Bánh Cuốn",
            "banh_duc": "Bánh Đúc",
            "banh_gio": "Bánh Giò",
            "banh_khot": "Bánh Khọt",
            "banh_mi": "Bánh Mì",
            "banh_pia": "Bánh Pía",
            "banh_tet": "Bánh Tét",
            "banh_trang_nuong": "Bánh Tráng Nướng",
            "banh_xeo": "Bánh Xèo",
            "bun_bo_hue": "Bún Bò Huế",
            "bun_dau_mam_tom": "Bún Đậu Mắm Tôm",
            "bun_mam": "Bún Mắm",
            "bun_rieu": "Bún Riêu",
            "bun_thit_nuong": "Bún Thịt Nướng",
            "cao_lau": "Cao Lầu",
            "com_tam": "Cơm Tấm",
            "goi_cuon": "Gỏi Cuốn",
            "hu_tieu": "Hủ Tiếu",
            "mi_quang": "Mì Quảng",
            "nem_lui": "Nem Lụi",
            "nem_ran": "Nem Rán",
            "pho_bo": "Phở Bò",
            "pho_ga": "Phở Gà",
            "xoi_man": "Xôi Mặn",
            "xoi_xeo": "Xôi Xéo"
        }
        
        if class_name in vietnamese_mapping:
            return vietnamese_mapping[class_name]
        
        # For other dishes, convert underscores to spaces and title case
        return class_name.replace('_', ' ').title()
    
    def _get_model_info(self) -> str:
        """Get model information string"""
        if self.model_type == "trained_model":
            return "ResNet50 trained model with custom weights"
        elif self.model_type == "functional_fallback":
            return "ResNet50 functional model (ImageNet weights)"
        elif self.model_type == "sequential_fallback":
            return "ResNet50 sequential model (ImageNet weights)"
        else:
            return "Unknown model type"
    
    def _generate_dummy_bbox(self) -> Dict[str, int]:
        """Generate dummy bounding box (placeholder for future object detection)"""
        return {
            "x": 50,
            "y": 60,
            "width": 200,
            "height": 180
        }
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current model status"""
        return {
            "model_loaded": self.model is not None,
            "model_type": self.model_type,
            "classes_loaded": len(self.class_mapping),
            "model_info": self._get_model_info() if self.model else "No model loaded"
        }

# Global inference service instance
inference_service = None

def get_inference_service() -> FoodInferenceService:
    """Get or create inference service instance (singleton pattern)"""
    global inference_service
    if inference_service is None:
        inference_service = FoodInferenceService()
    return inference_service
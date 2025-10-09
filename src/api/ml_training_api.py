"""
API endpoints for ML model training on real data
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

from src.ai.ml_training_engine import MLTrainingEngine, ModelType
from src.api.auth import get_current_user
from src.lib.utils import get_logger

logger = get_logger("MLTrainingAPI")
router = APIRouter(prefix="/ml/training", tags=["ml-training"])

# Initialize the ML training engine
ml_training_engine = MLTrainingEngine()

class DataCollectionRequest(BaseModel):
    """Request model for data collection."""
    chip_ids: List[str]
    hours: int = 168  # Default: 1 week

class DataPreprocessingRequest(BaseModel):
    """Request model for data preprocessing."""
    raw_data: Dict[str, Any]
    features: Optional[List[str]] = None
    target: str = "defect_rate"

class ModelTrainingRequest(BaseModel):
    """Request model for model training."""
    preprocessed_data: Dict[str, Any]
    model_type: str = "random_forest"
    model_params: Optional[Dict[str, Any]] = None

class ModelEvaluationRequest(BaseModel):
    """Request model for model evaluation."""
    model_id: str
    test_data: Optional[Dict[str, Any]] = None

class ModelPredictionRequest(BaseModel):
    """Request model for model prediction."""
    model_id: str
    input_data: List[List[float]]

class ModelIntegrationRequest(BaseModel):
    """Request model for model integration."""
    model_id: str
    optimization_goal: str = "minimize_defects"

class MLTrainingResponse(BaseModel):
    """Response model for ML training operations."""
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    process_id: Optional[str] = None
    model_id: Optional[str] = None

@router.post("/collect-data", response_model=MLTrainingResponse)
async def collect_real_data(
    request: DataCollectionRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Collect real chip design data for ML training.
    
    Args:
        request: Data collection request with chip IDs and time range
        current_user: Authenticated user
        
    Returns:
        Collected data for training
    """
    try:
        logger.info(f"Data collection requested by {current_user}")
        
        result = await ml_training_engine.collect_real_data(
            request.chip_ids, request.hours
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return MLTrainingResponse(
            status=result["status"],
            message="Data collection completed successfully",
            data=result,
            process_id=result.get("process_id")
        )
    except Exception as e:
        logger.error(f"Data collection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")

@router.post("/preprocess-data", response_model=MLTrainingResponse)
async def preprocess_data(
    request: DataPreprocessingRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Preprocess collected data for ML training.
    
    Args:
        request: Data preprocessing request with raw data and parameters
        current_user: Authenticated user
        
    Returns:
        Preprocessed training data
    """
    try:
        logger.info(f"Data preprocessing requested by {current_user}")
        
        result = await ml_training_engine.preprocess_data(
            request.raw_data, request.features, request.target
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return MLTrainingResponse(
            status=result["status"],
            message="Data preprocessing completed successfully",
            data=result,
            process_id=result.get("process_id")
        )
    except Exception as e:
        logger.error(f"Data preprocessing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data preprocessing failed: {str(e)}")

@router.post("/train-model", response_model=MLTrainingResponse)
async def train_model(
    request: ModelTrainingRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Train ML model on preprocessed data.
    
    Args:
        request: Model training request with preprocessed data and model type
        current_user: Authenticated user
        
    Returns:
        Trained model information
    """
    try:
        logger.info(f"Model training requested by {current_user}")
        
        # Convert string to ModelType enum
        try:
            model_type = ModelType(request.model_type.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid model type: {request.model_type}")
        
        result = await ml_training_engine.train_model(
            request.preprocessed_data, model_type, request.model_params
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return MLTrainingResponse(
            status=result["status"],
            message="Model training completed successfully",
            data=result.get("model_info"),
            process_id=result.get("process_id"),
            model_id=result.get("model_id")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Model training failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")

@router.post("/evaluate-model", response_model=MLTrainingResponse)
async def evaluate_model(
    request: ModelEvaluationRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Evaluate trained model performance.
    
    Args:
        request: Model evaluation request with model ID
        current_user: Authenticated user
        
    Returns:
        Model evaluation results
    """
    try:
        logger.info(f"Model evaluation requested by {current_user}")
        
        result = await ml_training_engine.evaluate_model(
            request.model_id, request.test_data
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return MLTrainingResponse(
            status=result["status"],
            message="Model evaluation completed successfully",
            data=result,
            process_id=result.get("process_id"),
            model_id=result.get("model_id")
        )
    except Exception as e:
        logger.error(f"Model evaluation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Model evaluation failed: {str(e)}")

@router.post("/predict", response_model=MLTrainingResponse)
async def predict_with_model(
    request: ModelPredictionRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Make predictions using a trained model.
    
    Args:
        request: Model prediction request with model ID and input data
        current_user: Authenticated user
        
    Returns:
        Model predictions
    """
    try:
        logger.info(f"Model prediction requested by {current_user}")
        
        result = await ml_training_engine.predict_with_model(
            request.model_id, request.input_data
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return MLTrainingResponse(
            status=result["status"],
            message="Model prediction completed successfully",
            data=result,
            process_id=result.get("process_id"),
            model_id=result.get("model_id")
        )
    except Exception as e:
        logger.error(f"Model prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")

@router.post("/integrate", response_model=MLTrainingResponse)
async def integrate_with_optimization(
    request: ModelIntegrationRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Integrate trained ML model with chip optimization engines.
    
    Args:
        request: Model integration request with model ID and optimization goal
        current_user: Authenticated user
        
    Returns:
        Integration results
    """
    try:
        logger.info(f"Model integration requested by {current_user}")
        
        result = await ml_training_engine.integrate_with_optimization(
            request.model_id, request.optimization_goal
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return MLTrainingResponse(
            status=result["status"],
            message="Model integration completed successfully",
            data=result,
            process_id=result.get("process_id"),
            model_id=result.get("model_id")
        )
    except Exception as e:
        logger.error(f"Model integration failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Model integration failed: {str(e)}")

@router.get("/model/{model_id}", response_model=MLTrainingResponse)
async def get_model_info(
    model_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Get information about a trained model.
    
    Args:
        model_id: ID of the model to retrieve
        current_user: Authenticated user
        
    Returns:
        Model information
    """
    try:
        logger.info(f"Model info requested by {current_user}")
        
        result = ml_training_engine.get_model_info(model_id)
        
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
            
        return MLTrainingResponse(
            status=result["status"],
            message="Model information retrieved successfully",
            data=result.get("model_info"),
            model_id=model_id
        )
    except Exception as e:
        logger.error(f"Failed to get model info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

@router.get("/models", response_model=MLTrainingResponse)
async def list_models(
    current_user: str = Depends(get_current_user)
):
    """
    List all trained models.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        List of all trained models
    """
    try:
        logger.info(f"Model list requested by {current_user}")
        
        result = ml_training_engine.list_models()
        
        return MLTrainingResponse(
            status=result["status"],
            message="Model list retrieved successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Failed to list models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")

@router.get("/history/{process_id}", response_model=MLTrainingResponse)
async def get_training_history(
    process_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Get training history for a specific process.
    
    Args:
        process_id: Process ID to get history for
        current_user: Authenticated user
        
    Returns:
        Training history
    """
    try:
        logger.info(f"Training history requested by {current_user} for process {process_id}")
        
        result = ml_training_engine.get_training_history(process_id)
        
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
            
        return MLTrainingResponse(
            status=result["status"],
            message="Training history retrieved successfully",
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Failed to get training history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get training history: {str(e)}")

@router.get("/history", response_model=MLTrainingResponse)
async def get_all_training_history(
    current_user: str = Depends(get_current_user)
):
    """
    Get all training history.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Complete training history
    """
    try:
        logger.info(f"Complete training history requested by {current_user}")
        
        result = ml_training_engine.get_training_history()
        
        return MLTrainingResponse(
            status=result["status"],
            message="Training history retrieved successfully",
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Failed to get training history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get training history: {str(e)}")
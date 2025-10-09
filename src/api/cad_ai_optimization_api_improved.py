"""
CAD AI Optimization API for GlobalScope MultiFrame Platform
Provides REST API endpoints for AI-driven CAD parameter optimization.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import asyncio

from src.ai.cad_ai_optimizer import get_cad_ai_optimizer, init_cad_ai_optimizer, AIOptimizationStrategy
from src.lib.utils import get_logger

logger = get_logger("CADAIOptimizationAPI")
router = APIRouter(prefix="/api/v1/cad/ai", tags=["cad-ai-optimization"])

# Request models
class OptimizeParametersRequest(BaseModel):
    tool_name: str
    project_id: str
    initial_params: Dict[str, Any]
    target_metrics: Dict[str, float]
    strategy: str = "bayesian"
    max_iterations: int = 50

class SaveTemplateRequest(BaseModel):
    tool_name: str
    template_name: str
    parameters: Dict[str, Any]
    project_context: Dict[str, Any]

class GetRecommendationsRequest(BaseModel):
    tool_name: str
    project_context: Dict[str, Any]

class UpdateProjectDatabaseRequest(BaseModel):
    project_id: str
    tool_name: str
    optimal_config: Dict[str, Any]
    context: Dict[str, Any]
    performance_metrics: Dict[str, float]

# Response models
class OptimizationResult(BaseModel):
    status: str
    process_id: Optional[str] = None
    optimized_params: Optional[Dict[str, Any]] = None
    final_metrics: Optional[Dict[str, float]] = None
    method: Optional[str] = None
    iterations: Optional[int] = None
    improvement: Optional[Dict[str, float]] = None
    message: Optional[str] = None

class RecommendationResult(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    message: Optional[str] = None

class TemplateResult(BaseModel):
    status: str
    message: str

class OptimizationStatus(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class ProjectDatabaseResponse(BaseModel):
    status: str
    message: str

# Initialize optimizer
_cad_ai_optimizer = None

async def get_optimizer():
    """Get or initialize the CAD AI optimizer."""
    global _cad_ai_optimizer
    if _cad_ai_optimizer is None:
        _cad_ai_optimizer = await init_cad_ai_optimizer()
    return _cad_ai_optimizer

# API Endpoints

@router.post("/optimize-parameters", response_model=OptimizationResult)
async def optimize_cad_parameters(request: OptimizeParametersRequest):
    """
    Optimize CAD tool parameters using AI techniques.
    
    This endpoint uses machine learning algorithms to find optimal parameter configurations
    for CAD tools based on target performance metrics.
    """
    try:
        optimizer = await get_optimizer()
        
        # Convert strategy string to enum
        try:
            strategy = AIOptimizationStrategy(request.strategy.lower())
        except ValueError:
            strategy = AIOptimizationStrategy.BAYESIAN  # Default
        
        result = await optimizer.optimize_cad_parameters(
            tool_name=request.tool_name,
            project_id=request.project_id,
            initial_params=request.initial_params,
            target_metrics=request.target_metrics,
            strategy=strategy,
            max_iterations=request.max_iterations
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        return OptimizationResult(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in optimize_cad_parameters: {e}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@router.get("/optimization-status/{process_id}", response_model=OptimizationStatus)
async def get_optimization_status(process_id: str):
    """
    Get the status of an ongoing AI optimization process.
    """
    try:
        optimizer = await get_optimizer()
        history = optimizer.get_optimization_history(process_id)
        
        if history["status"] == "error":
            raise HTTPException(status_code=500, detail=history["message"])
        
        if not history["data"]:
            raise HTTPException(status_code=404, detail=f"No optimization found for process {process_id}")
        
        return OptimizationStatus(
            status="success",
            data=history["data"][-1] if history["data"] else None,
            message=f"Status retrieved for process {process_id}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_optimization_status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")

@router.post("/save-template", response_model=TemplateResult)
async def save_optimization_template(request: SaveTemplateRequest):
    """
    Save an optimized parameter configuration as a template for future use.
    """
    try:
        # In a real implementation, this would save to a database or cache
        # For now, we'll just simulate the operation
        await asyncio.sleep(0.1)  # Simulate processing
        
        logger.info(f"Saved template '{request.template_name}' for tool '{request.tool_name}'")
        
        return TemplateResult(
            status="success",
            message=f"Template '{request.template_name}' saved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in save_optimization_template: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save template: {str(e)}")

@router.post("/recommendations", response_model=RecommendationResult)
async def get_ai_recommendations(request: GetRecommendationsRequest):
    """
    Get AI-driven recommendations for CAD parameter optimization.
    
    This endpoint provides intelligent parameter recommendations based on project context
    and historical optimization data.
    """
    try:
        optimizer = await get_optimizer()
        result = await optimizer.get_recommendations(
            tool_name=request.tool_name,
            project_context=request.project_context
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        return RecommendationResult(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_ai_recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.get("/strategies", response_model=Dict[str, Any])
async def list_optimization_strategies():
    """
    List available AI optimization strategies.
    """
    try:
        strategies = {strategy.name: strategy.value for strategy in AIOptimizationStrategy}
        return {
            "status": "success",
            "data": strategies,
            "message": "Available optimization strategies retrieved"
        }
    except Exception as e:
        logger.error(f"Error in list_optimization_strategies: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list strategies: {str(e)}")

@router.get("/history", response_model=Dict[str, Any])
async def get_optimization_history():
    """
    Get history of all AI optimization processes.
    """
    try:
        optimizer = await get_optimizer()
        history = optimizer.get_optimization_history()
        
        if history["status"] == "error":
            raise HTTPException(status_code=500, detail=history["message"])
        
        return {
            "status": "success",
            "data": history["data"],
            "count": len(history["data"]),
            "message": "Optimization history retrieved"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_optimization_history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")

@router.post("/project-database", response_model=ProjectDatabaseResponse)
async def update_project_database(request: UpdateProjectDatabaseRequest):
    """
    Update the project database with optimal configurations for transfer learning.
    
    This endpoint allows adding project data to the database for future transfer learning.
    """
    try:
        optimizer = await get_optimizer()
        
        # Add project to database
        project_data = {
            "project_id": request.project_id,
            "tool_name": request.tool_name,
            "optimal_config": request.optimal_config,
            "context": request.context,
            "performance_metrics": request.performance_metrics,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # In a real implementation, this would store in a database
        # For now, we'll store in the optimizer's in-memory database
        optimizer.project_database[request.project_id] = project_data
        
        logger.info(f"Added project {request.project_id} to database for transfer learning")
        
        return ProjectDatabaseResponse(
            status="success",
            message=f"Project {request.project_id} added to database successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in update_project_database: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update project database: {str(e)}")

@router.get("/health", response_model=Dict[str, str])
async def ai_optimizer_health_check():
    """
    Check the health status of the AI optimization system.

"""
CAD AI Optimization API v2 for GlobalScope MultiFrame Platform
Provides enhanced REST API endpoints for AI-driven CAD parameter optimization.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import asyncio
import json

from src.ai.cad_ai_optimizer import CADAIOptimizer, AIOptimizationStrategy, InteractionMode
from src.lib.utils import get_logger

logger = get_logger("CADAIOptimizationAPIv2")
router = APIRouter(prefix="/api/v2/cad/ai", tags=["cad-ai-optimization-v2"])

# Request models
class OptimizeParametersRequest(BaseModel):
    tool_name: str
    project_id: str
    initial_params: Dict[str, Any]
    target_metrics: Dict[str, float]
    strategy: str = "bayesian"
    max_iterations: int = 50
    project_context: Optional[Dict[str, Any]] = None
    interaction_mode: str = "professional"  # New field for interaction mode
    confidentiality_enabled: bool = True  # New field for confidentiality

class SaveTemplateRequest(BaseModel):
    tool_name: str
    template_name: str
    parameters: Dict[str, Any]
    project_context: Dict[str, Any]
    performance_metrics: Optional[Dict[str, float]] = None

class GetRecommendationsRequest(BaseModel):
    tool_name: str
    project_context: Dict[str, Any]
    target_metrics: Optional[Dict[str, float]] = None

class UpdateProjectDatabaseRequest(BaseModel):
    project_id: str
    tool_name: str
    optimal_config: Dict[str, Any]
    context: Dict[str, Any]
    performance_metrics: Dict[str, float]
    chip_type: Optional[str] = None
    technology_node: Optional[str] = None

class BatchOptimizationRequest(BaseModel):
    optimizations: List[OptimizeParametersRequest]
    parallel: bool = False

# Response models
class OptimizationResult(BaseModel):
    status: str
    process_id: Optional[str] = None
    optimized_params: Optional[Dict[str, Any]] = None
    final_metrics: Optional[Dict[str, float]] = None
    method: Optional[str] = None
    iterations: Optional[int] = None
    improvement: Optional[Dict[str, float]] = None
    confidence_score: Optional[float] = None
    execution_time: Optional[float] = None
    message: Optional[str] = None
    interaction_mode: Optional[str] = None  # New field
    confidentiality_enabled: Optional[bool] = None  # New field
    strategy_info: Optional[Dict[str, Any]] = None  # New field for mode-specific information

class RecommendationResult(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    confidence_score: Optional[float] = None
    similar_projects_used: Optional[int] = None
    message: Optional[str] = None

class TemplateResult(BaseModel):
    status: str
    template_id: Optional[str] = None
    message: str

class OptimizationStatus(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    progress: Optional[float] = None
    message: Optional[str] = None

class ProjectDatabaseResponse(BaseModel):
    status: str
    project_id: str
    message: str

class BatchOptimizationResult(BaseModel):
    status: str
    results: List[OptimizationResult]
    message: str

# Initialize optimizer
_cad_ai_optimizer = None

async def get_optimizer():
    """Get or initialize the CAD AI optimizer."""
    global _cad_ai_optimizer
    if _cad_ai_optimizer is None:
        _cad_ai_optimizer = CADAIOptimizer()
        await _cad_ai_optimizer.initialize_modules()
    return _cad_ai_optimizer

# API Endpoints

@router.post("/optimize-parameters", response_model=OptimizationResult)
async def optimize_cad_parameters(request: OptimizeParametersRequest):
    """
    Optimize CAD tool parameters using advanced AI techniques.
    
    This endpoint uses machine learning algorithms including Bayesian Optimization with Gaussian Processes,
    Transfer Learning, and Ensemble Methods to find optimal parameter configurations for CAD tools.
    
    New in v2:
    - Support for semi-automatic and manual interaction modes with HoloMesh
    - Confidentiality controls for professional workflows
    - Enhanced confidence scoring based on interaction mode
    """
    try:
        start_time = asyncio.get_event_loop().time()
        optimizer = await get_optimizer()
        
        # Convert strategy string to enum
        try:
            strategy = AIOptimizationStrategy(request.strategy.lower())
        except ValueError:
            strategy = AIOptimizationStrategy.BAYESIAN  # Default
        
        # Convert interaction mode string to enum
        try:
            interaction_mode = InteractionMode(request.interaction_mode.lower())
        except ValueError:
            interaction_mode = InteractionMode.PROFESSIONAL  # Default
        
        # Add project context to optimizer database if provided
        if request.project_context:
            optimizer.project_database[request.project_id] = {
                "project_id": request.project_id,
                "tool_name": request.tool_name,
                "context": request.project_context,
                "timestamp": asyncio.get_event_loop().time()
            }
        
        result = await optimizer.optimize_cad_parameters(
            tool_name=request.tool_name,
            project_id=request.project_id,
            initial_params=request.initial_params,
            target_metrics=request.target_metrics,
            strategy=strategy,
            max_iterations=request.max_iterations,
            interaction_mode=interaction_mode,
            confidentiality_enabled=request.confidentiality_enabled
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        # Add execution time
        execution_time = asyncio.get_event_loop().time() - start_time
        result["execution_time"] = execution_time
        
        # Add confidence score based on method and iterations
        if result.get("method") == "bayesian":
            result["confidence_score"] = min(0.95, 0.7 + 0.01 * result.get("iterations", 0))
        elif result.get("method") == "transfer_learning":
            result["confidence_score"] = 0.85
        elif result.get("method") == "ensemble":
            result["confidence_score"] = 0.9
        elif result.get("method") == "semi_automatic":
            result["confidence_score"] = 0.8
        elif result.get("method") == "manual":
            result["confidence_score"] = 0.75
        else:
            result["confidence_score"] = 0.7
        
        # Add mode-specific information
        if interaction_mode == InteractionMode.SEMI_AUTOMATIC:
            result["strategy_info"] = {
                "type": "human_ai_collaboration",
                "features": ["holomesh_recommendations", "tool_switching", "error_elimination"],
                "description": "Combines AI optimization with HoloMesh interaction for seamless tool switching"
            }
        elif interaction_mode == InteractionMode.MANUAL:
            result["strategy_info"] = {
                "type": "professional_guidance",
                "features": ["tool_guidance", "consultation_on_demand", "confidentiality_controls"],
                "description": "Professional tool guidance with confidentiality controls enabled by default",
                "confidentiality_status": "enabled" if request.confidentiality_enabled else "disabled"
            }
        
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
        
        # Calculate progress if available
        progress = None
        if history["data"] and "iterations" in history["data"][-1].get("result", {}):
            result = history["data"][-1]["result"]
            if "max_iterations" in result:
                progress = min(1.0, result.get("iterations", 0) / result["max_iterations"])
        
        return OptimizationStatus(
            status="success",
            data=history["data"][-1] if history["data"] else None,
            progress=progress,
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
        optimizer = await get_optimizer()
        
        # Add template to project database for transfer learning
        template_id = f"template_{request.tool_name}_{hash(request.template_name) % 10000}"
        
        template_data = {
            "project_id": template_id,
            "tool_name": request.tool_name,
            "optimal_config": request.parameters,
            "context": request.project_context,
            "performance_metrics": request.performance_metrics or {},
            "template_name": request.template_name,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        optimizer.project_database[template_id] = template_data
        
        logger.info(f"Saved template '{request.template_name}' for tool '{request.tool_name}'")
        
        return TemplateResult(
            status="success",
            template_id=template_id,
            message=f"Template '{request.template_name}' saved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in save_optimization_template: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save template: {str(e)}")

@router.post("/recommendations", response_model=RecommendationResult)
async def get_ai_recommendations(request: GetRecommendationsRequest):
    """
    Get AI-driven recommendations for CAD parameter optimization.
    
    This endpoint provides intelligent parameter recommendations based on project context,
    historical optimization data, and transfer learning from similar projects.
    
    New in v2:
    - Enhanced recommendations with confidence scoring
    - Better similarity matching for transfer learning
    """
    try:
        optimizer = await get_optimizer()
        result = await optimizer.get_recommendations(
            tool_name=request.tool_name,
            project_context=request.project_context
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        # Enhance the response with additional information
        enhanced_result = {
            "status": result["status"],
            "data": result.get("data", {}),
            "source": result.get("source", "unknown"),
            "confidence_score": result.get("data", {}).get("confidence_score", 0.0),
            "similar_projects_used": result.get("data", {}).get("similar_projects_used", 0),
            "message": result.get("message", "")
        }
        
        return RecommendationResult(**enhanced_result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_ai_recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.get("/strategies", response_model=Dict[str, Any])
async def list_optimization_strategies():
    """
    List available AI optimization strategies with descriptions.
    """
    try:
        strategies_info = {
            "bayesian": {
                "name": "Bayesian Optimization",
                "description": "Uses Gaussian Process surrogate models and Expected Improvement acquisition function for efficient parameter search",
                "best_for": "Complex parameter spaces with expensive evaluations"
            },
            "transfer_learning": {
                "name": "Transfer Learning",
                "description": "Leverages knowledge from similar past projects to accelerate optimization",
                "best_for": "Projects similar to previously optimized designs"
            },
            "ensemble": {
                "name": "Ensemble Methods",
                "description": "Combines multiple optimization strategies for robust results",
                "best_for": "Critical projects requiring high reliability"
            },
            "genetic": {
                "name": "Genetic Algorithm",
                "description": "Evolutionary optimization approach using mutation and crossover",
                "best_for": "Exploring diverse parameter combinations"
            },
            "semi_automatic": {
                "name": "Semi-Automatic Mode",
                "description": "Combines AI optimization with HoloMesh interaction for professional and innovative tools",
                "best_for": "Projects requiring human-AI collaboration with easy switching between tools",
                "new_in_v2": True
            },
            "manual": {
                "name": "Manual Mode",
                "description": "Professional tool guidance with confidentiality controls",
                "best_for": "Chip designers working in confidential environments",
                "new_in_v2": True
            }
        }
        
        return {
            "status": "success",
            "data": strategies_info,
            "count": len(strategies_info),
            "message": "Available optimization strategies retrieved"
        }
    except Exception as e:
        logger.error(f"Error in list_optimization_strategies: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list strategies: {str(e)}")

@router.get("/history", response_model=Dict[str, Any])
async def get_optimization_history(project_id: Optional[str] = None):
    """
    Get history of AI optimization processes, optionally filtered by project.
    """
    try:
        optimizer = await get_optimizer()
        history = optimizer.get_optimization_history()
        
        if history["status"] == "error":
            raise HTTPException(status_code=500, detail=history["message"])
        
        # Filter by project_id if provided
        filtered_data = history["data"]
        if project_id:
            filtered_data = {
                k: v for k, v in history["data"].items() 
                if any(item.get("result", {}).get("project_id") == project_id for item in v)
            }
        
        return {
            "status": "success",
            "data": filtered_data,
            "count": len(filtered_data),
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
    
    This endpoint allows adding project data to the database for future transfer learning,
    enabling the system to learn from past successful optimizations.
    
    New in v2:
    - Support for chip type and technology node metadata
    - Enhanced project similarity matching
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
            "chip_type": request.chip_type,
            "technology_node": request.technology_node,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Store in the optimizer's database
        optimizer.project_database[request.project_id] = project_data
        
        logger.info(f"Added project {request.project_id} to database for transfer learning")
        
        return ProjectDatabaseResponse(
            status="success",
            project_id=request.project_id,
            message=f"Project {request.project_id} added to database successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in update_project_database: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update project database: {str(e)}")

@router.post("/batch-optimize", response_model=BatchOptimizationResult)
async def batch_optimize_parameters(request: BatchOptimizationRequest):
    """
    Run multiple optimization tasks in batch, either sequentially or in parallel.
    """
    try:
        optimizer = await get_optimizer()
        results = []
        
        if request.parallel:
            # Run optimizations in parallel
            tasks = []
            for i, opt_request in enumerate(request.optimizations):
                # Convert strategy string to enum
                try:
                    strategy = AIOptimizationStrategy(opt_request.strategy.lower())
                except ValueError:
                    strategy = AIOptimizationStrategy.BAYESIAN  # Default
                
                # Convert interaction mode string to enum
                try:
                    interaction_mode = InteractionMode(opt_request.interaction_mode.lower())
                except ValueError:
                    interaction_mode = InteractionMode.PROFESSIONAL  # Default
                
                task = optimizer.optimize_cad_parameters(
                    tool_name=opt_request.tool_name,
                    project_id=opt_request.project_id,
                    initial_params=opt_request.initial_params,
                    target_metrics=opt_request.target_metrics,
                    strategy=strategy,
                    max_iterations=opt_request.max_iterations,
                    interaction_mode=interaction_mode,
                    confidentiality_enabled=opt_request.confidentiality_enabled
                )
                tasks.append(task)
            
            # Run all tasks concurrently
            task_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, task_result in enumerate(task_results):
                if isinstance(task_result, Exception):
                    results.append(OptimizationResult(
                        status="error",
                        message=f"Optimization {i} failed: {str(task_result)}"
                    ))
                else:
                    # Handle the result properly
                    if isinstance(task_result, dict):
                        # Ensure all required fields are present
                        result_data = dict(task_result)
                        if "status" not in result_data:
                            result_data["status"] = "success"
                        results.append(OptimizationResult(**result_data))
                    else:
                        # Handle non-dict results
                        results.append(OptimizationResult(
                            status="success",
                            message=str(task_result)
                        ))
        else:
            # Run optimizations sequentially
            for opt_request in request.optimizations:
                # Convert strategy string to enum
                try:
                    strategy = AIOptimizationStrategy(opt_request.strategy.lower())
                except ValueError:
                    strategy = AIOptimizationStrategy.BAYESIAN  # Default
                
                # Convert interaction mode string to enum
                try:
                    interaction_mode = InteractionMode(opt_request.interaction_mode.lower())
                except ValueError:
                    interaction_mode = InteractionMode.PROFESSIONAL  # Default
                
                result = await optimizer.optimize_cad_parameters(
                    tool_name=opt_request.tool_name,
                    project_id=opt_request.project_id,
                    initial_params=opt_request.initial_params,
                    target_metrics=opt_request.target_metrics,
                    strategy=strategy,
                    max_iterations=opt_request.max_iterations,
                    interaction_mode=interaction_mode,
                    confidentiality_enabled=opt_request.confidentiality_enabled
                )
                
                # Handle the result properly
                if isinstance(result, dict):
                    # Ensure all required fields are present
                    result_data = dict(result)
                    if "status" not in result_data:
                        result_data["status"] = "success"
                    results.append(OptimizationResult(**result_data))
                else:
                    # Handle non-dict results
                    results.append(OptimizationResult(
                        status="success",
                        message=str(result)
                    ))
        
        return BatchOptimizationResult(
            status="success",
            results=results,
            message=f"Batch optimization completed with {len(results)} results"
        )
        
    except Exception as e:
        logger.error(f"Error in batch_optimize_parameters: {e}")
        raise HTTPException(status_code=500, detail=f"Batch optimization failed: {str(e)}")

@router.get("/database-stats", response_model=Dict[str, Any])
async def get_database_stats():
    """
    Get statistics about the project database for transfer learning.
    """
    try:
        optimizer = await get_optimizer()
        
        # Calculate statistics
        total_projects = len(optimizer.project_database)
        
        # Count by tool
        tool_counts = {}
        for project in optimizer.project_database.values():
            tool = project.get("tool_name", "unknown")
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        # Count by chip type if available
        chip_type_counts = {}
        for project in optimizer.project_database.values():
            chip_type = project.get("chip_type", "unknown")
            chip_type_counts[chip_type] = chip_type_counts.get(chip_type, 0) + 1
        
        return {
            "status": "success",
            "data": {
                "total_projects": total_projects,
                "projects_by_tool": tool_counts,
                "projects_by_chip_type": chip_type_counts,
                "database_size": len(json.dumps(optimizer.project_database))
            },
            "message": "Database statistics retrieved"
        }
        
    except Exception as e:
        logger.error(f"Error in get_database_stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get database stats: {str(e)}")

@router.get("/health", response_model=Dict[str, str])
async def ai_optimizer_health_check():
    """
    Check the health status of the AI optimization system.
    """
    try:
        optimizer = await get_optimizer()
        if optimizer is not None:
            # Check if the optimizer has been properly initialized
            db_size = len(optimizer.project_database)
            return {
                "status": "healthy",
                "message": f"AI CAD optimizer is running with {db_size} projects in database"
            }
        else:
            return {
                "status": "degraded",
                "message": "AI CAD optimizer is not initialized"
            }
    except Exception as e:
        logger.error(f"Error in ai_optimizer_health_check: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

"""
API endpoints for chip optimization services
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

from src.chip_design.chip_optimization_engine import ChipOptimizationEngine, OptimizationType
from src.api.auth import get_current_user
from src.lib.utils import get_logger

logger = get_logger("ChipOptimizationAPI")
router = APIRouter(prefix="/chip/optimization", tags=["chip-optimization"])

# Initialize the optimization engine
optimization_engine = ChipOptimizationEngine()

class ChipDataRequest(BaseModel):
    """Request model for chip optimization data."""
    components: List[Dict[str, Any]] = []
    connections: List[Dict[str, Any]] = []
    logic_gates: List[Dict[str, Any]] = []
    registers: List[Dict[str, Any]] = []
    timing_paths: List[Dict[str, Any]] = []
    constraints: Dict[str, Any] = {}
    clocks: List[Dict[str, Any]] = []
    timing_constraints: Dict[str, Any] = {}

class OptimizationResponse(BaseModel):
    """Response model for optimization results."""
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    process_id: Optional[str] = None

class MultiObjectiveRequest(BaseModel):
    """Request model for multi-objective optimization."""
    chip_data: ChipDataRequest
    objectives: List[str] = ["placement", "routing"]

class BenefitEstimationRequest(BaseModel):
    """Request model for benefit estimation."""
    chip_data: ChipDataRequest
    optimization_type: str

@router.post("/placement", response_model=OptimizationResponse)
async def optimize_placement(
    chip_data: ChipDataRequest,
    algorithm: str = "simulated_annealing",
    current_user: str = Depends(get_current_user)
):
    """
    Optimize component placement on chip.
    
    Args:
        chip_data: Chip design data
        algorithm: Algorithm to use ('simulated_annealing' or 'force_directed')
        current_user: Authenticated user
        
    Returns:
        Optimization results
    """
    try:
        logger.info(f"Placement optimization requested by {current_user}")
        
        result = await optimization_engine.optimize_placement(
            chip_data.dict(), algorithm
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            message=result.get("message"),
            data=result.get("data"),
            process_id=result.get("process_id")
        )
    except Exception as e:
        logger.error(f"Placement optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Placement optimization failed: {str(e)}")

@router.post("/routing", response_model=OptimizationResponse)
async def optimize_routing(
    chip_data: ChipDataRequest,
    algorithm: str = "a_star",
    current_user: str = Depends(get_current_user)
):
    """
    Optimize signal routing on chip.
    
    Args:
        chip_data: Chip design data with placement info
        algorithm: Algorithm to use ('a_star' or 'maze_routing')
        current_user: Authenticated user
        
    Returns:
        Optimization results
    """
    try:
        logger.info(f"Routing optimization requested by {current_user}")
        
        result = await optimization_engine.optimize_routing(
            chip_data.dict(), algorithm
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            message=result.get("message"),
            data=result.get("data"),
            process_id=result.get("process_id")
        )
    except Exception as e:
        logger.error(f"Routing optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Routing optimization failed: {str(e)}")

@router.post("/synthesis", response_model=OptimizationResponse)
async def optimize_logic_synthesis(
    chip_data: ChipDataRequest,
    algorithm: str = "technology_mapping",
    current_user: str = Depends(get_current_user)
):
    """
    Optimize logic synthesis.
    
    Args:
        chip_data: Chip design data
        algorithm: Algorithm to use ('technology_mapping' or 'retiming')
        current_user: Authenticated user
        
    Returns:
        Optimization results
    """
    try:
        logger.info(f"Logic synthesis optimization requested by {current_user}")
        
        result = await optimization_engine.optimize_logic_synthesis(
            chip_data.dict(), algorithm
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            message=result.get("message"),
            data=result.get("data"),
            process_id=result.get("process_id")
        )
    except Exception as e:
        logger.error(f"Logic synthesis optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Logic synthesis optimization failed: {str(e)}")

@router.post("/power", response_model=OptimizationResponse)
async def optimize_power(
    chip_data: ChipDataRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Optimize power consumption.
    
    Args:
        chip_data: Chip design data
        current_user: Authenticated user
        
    Returns:
        Optimization results
    """
    try:
        logger.info(f"Power optimization requested by {current_user}")
        
        result = await optimization_engine.optimize_power(chip_data.dict())
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            message=result.get("message"),
            data=result.get("data"),
            process_id=result.get("process_id")
        )
    except Exception as e:
        logger.error(f"Power optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Power optimization failed: {str(e)}")

@router.post("/timing", response_model=OptimizationResponse)
async def optimize_timing(
    chip_data: ChipDataRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Optimize timing constraints.
    
    Args:
        chip_data: Chip design data
        current_user: Authenticated user
        
    Returns:
        Optimization results
    """
    try:
        logger.info(f"Timing optimization requested by {current_user}")
        
        result = await optimization_engine.optimize_timing(chip_data.dict())
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            message=result.get("message"),
            data=result.get("data"),
            process_id=result.get("process_id")
        )
    except Exception as e:
        logger.error(f"Timing optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Timing optimization failed: {str(e)}")

@router.post("/multi-objective", response_model=OptimizationResponse)
async def multi_objective_optimization(
    request: MultiObjectiveRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Perform multi-objective optimization.
    
    Args:
        request: Multi-objective optimization request
        current_user: Authenticated user
        
    Returns:
        Combined optimization results
    """
    try:
        logger.info(f"Multi-objective optimization requested by {current_user}")
        
        result = await optimization_engine.multi_objective_optimization(
            request.chip_data.dict(), request.objectives
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            message=result.get("message"),
            data=result.get("data"),
            process_id=result.get("process_id")
        )
    except Exception as e:
        logger.error(f"Multi-objective optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Multi-objective optimization failed: {str(e)}")

@router.post("/estimate-benefit", response_model=OptimizationResponse)
async def estimate_optimization_benefit(
    request: BenefitEstimationRequest,
    current_user: str = Depends(get_current_user)
):
    """
    Estimate potential benefits of optimization.
    
    Args:
        request: Benefit estimation request
        current_user: Authenticated user
        
    Returns:
        Estimated benefits
    """
    try:
        logger.info(f"Benefit estimation requested by {current_user}")
        
        # Convert string to OptimizationType enum
        try:
            opt_type = OptimizationType(request.optimization_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid optimization type: {request.optimization_type}")
        
        result = await optimization_engine.estimate_optimization_benefit(
            request.chip_data.dict(), opt_type
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            message=result.get("message"),
            data=result.get("estimated_benefit")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Benefit estimation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Benefit estimation failed: {str(e)}")

@router.get("/history/{process_id}", response_model=OptimizationResponse)
async def get_optimization_history(
    process_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Get optimization history for a specific process.
    
    Args:
        process_id: Process ID to get history for
        current_user: Authenticated user
        
    Returns:
        Optimization history
    """
    try:
        logger.info(f"Optimization history requested by {current_user} for process {process_id}")
        
        result = optimization_engine.get_optimization_history(process_id)
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Failed to get optimization history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get optimization history: {str(e)}")

@router.get("/history", response_model=OptimizationResponse)
async def get_all_optimization_history(
    current_user: str = Depends(get_current_user)
):
    """
    Get all optimization history.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Complete optimization history
    """
    try:
        logger.info(f"Complete optimization history requested by {current_user}")
        
        result = optimization_engine.get_optimization_history()
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
            
        return OptimizationResponse(
            status=result["status"],
            data=result.get("data")
        )
    except Exception as e:
        logger.error(f"Failed to get optimization history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get optimization history: {str(e)}")
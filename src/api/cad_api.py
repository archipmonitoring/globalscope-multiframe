"""
CAD API for GlobalScope MultiFrame 11.0
This module provides REST API endpoints for CAD tool integration
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import logging

from src.chip_design.cad_worker import cad_worker, run_verilator_simulation, run_yosys_synthesis, run_nextpnr_place_and_route, get_cad_tool_versions
from src.security.quantum_singularity_firewall import QuantumSingularityFirewall
from src.lib.utils import get_logger

logger = get_logger("CADAPI")
router = APIRouter(prefix="/api/v1/cad", tags=["cad"])

# Request models
class VerilogFile(BaseModel):
    name: str
    content: str

class VerilatorSimulationRequest(BaseModel):
    user_id: str
    project_id: str
    verilog_files: List[VerilogFile]
    top_module: str
    simulation_time: Optional[int] = 1000

class YosysSynthesisRequest(BaseModel):
    user_id: str
    project_id: str
    verilog_files: List[VerilogFile]
    target_family: Optional[str] = "generic"

class NextPNRRequest(BaseModel):
    user_id: str
    project_id: str
    netlist_file: str
    target_device: Optional[str] = "generic"

class CADToolResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

# Tool availability check
@router.get("/tools/available", response_model=Dict[str, bool])
async def check_cad_tools_availability():
    """Check which CAD tools are available"""
    try:
        tools_status = {}
        for tool_name in cad_worker.supported_tools.keys():
            tools_status[tool_name] = await cad_worker.check_tool_availability(tool_name)
        return tools_status
    except Exception as e:
        logger.error(f"Error checking CAD tools availability: {e}")
        raise HTTPException(status_code=500, detail=f"Error checking tools: {str(e)}")

# Tool versions
@router.get("/tools/versions", response_model=Dict[str, str])
async def get_cad_tools_versions():
    """Get versions of all available CAD tools"""
    try:
        versions = await get_cad_tool_versions()
        return versions
    except Exception as e:
        logger.error(f"Error getting CAD tools versions: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting versions: {str(e)}")

# Verilator simulation endpoint
@router.post("/verilator/simulate", response_model=CADToolResponse)
async def verilator_simulation(request: VerilatorSimulationRequest):
    """Run Verilator simulation"""
    try:
        logger.info(f"Starting Verilator simulation for project {request.project_id}")
        
        result = await run_verilator_simulation(
            user_id=request.user_id,
            project_id=request.project_id,
            verilog_files=[{"name": f.name, "content": f.content} for f in request.verilog_files],
            top_module=request.top_module,
            simulation_time=request.simulation_time
        )
        
        if result["status"] == "success":
            return CADToolResponse(
                status="success",
                message=f"Verilator simulation completed for project {request.project_id}",
                data=result
            )
        else:
            return CADToolResponse(
                status="error",
                message=result["message"],
                data=result
            )
    except Exception as e:
        logger.error(f"Error in Verilator simulation: {e}")
        raise HTTPException(status_code=500, detail=f"Verilator simulation error: {str(e)}")

# Yosys synthesis endpoint
@router.post("/yosys/synthesize", response_model=CADToolResponse)
async def yosys_synthesis(request: YosysSynthesisRequest):
    """Run Yosys synthesis"""
    try:
        logger.info(f"Starting Yosys synthesis for project {request.project_id}")
        
        result = await run_yosys_synthesis(
            user_id=request.user_id,
            project_id=request.project_id,
            verilog_files=[{"name": f.name, "content": f.content} for f in request.verilog_files],
            target_family=request.target_family
        )
        
        if result["status"] == "success":
            return CADToolResponse(
                status="success",
                message=f"Yosys synthesis completed for project {request.project_id}",
                data=result
            )
        else:
            return CADToolResponse(
                status="error",
                message=result["message"],
                data=result
            )
    except Exception as e:
        logger.error(f"Error in Yosys synthesis: {e}")
        raise HTTPException(status_code=500, detail=f"Yosys synthesis error: {str(e)}")

# NextPNR place and route endpoint
@router.post("/nextpnr/pnr", response_model=CADToolResponse)
async def nextpnr_place_and_route(request: NextPNRRequest):
    """Run NextPNR place and route"""
    try:
        logger.info(f"Starting NextPNR place and route for project {request.project_id}")
        
        result = await run_nextpnr_place_and_route(
            user_id=request.user_id,
            project_id=request.project_id,
            netlist_file=request.netlist_file,
            target_device=request.target_device
        )
        
        if result["status"] == "success":
            return CADToolResponse(
                status="success",
                message=f"NextPNR place and route completed for project {request.project_id}",
                data=result
            )
        else:
            return CADToolResponse(
                status="error",
                message=result["message"],
                data=result
            )
    except Exception as e:
        logger.error(f"Error in NextPNR place and route: {e}")
        raise HTTPException(status_code=500, detail=f"NextPNR place and route error: {str(e)}")

# Get CAD result
@router.get("/result/{tool}/{project_id}", response_model=CADToolResponse)
async def get_cad_result(tool: str, project_id: str):
    """Get CAD tool result for a specific project"""
    try:
        from src.lib.redis_client import redis_client
        
        result = await redis_client.get_json(f"cad_result:{tool}:{project_id}")
        
        if result:
            return CADToolResponse(
                status="success",
                message=f"CAD result for {tool} project {project_id}",
                data=result
            )
        else:
            raise HTTPException(status_code=404, detail=f"No result found for {tool} project {project_id}")
    except Exception as e:
        logger.error(f"Error getting CAD result: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting result: {str(e)}")

# Health check
@router.get("/health", response_model=CADToolResponse)
async def cad_health_check():
    """Check CAD system health"""
    try:
        # Check if at least one tool is available
        tools_status = {}
        available_tools = 0
        
        for tool_name in cad_worker.supported_tools.keys():
            is_available = await cad_worker.check_tool_availability(tool_name)
            tools_status[tool_name] = is_available
            if is_available:
                available_tools += 1
        
        if available_tools > 0:
            return CADToolResponse(
                status="success",
                message=f"CAD system healthy. {available_tools} tools available.",
                data={"tools": tools_status}
            )
        else:
            return CADToolResponse(
                status="error",
                message="No CAD tools available",
                data={"tools": tools_status}
            )
    except Exception as e:
        logger.error(f"Error in CAD health check: {e}")
        raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")
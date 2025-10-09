"""
Performance Monitoring Dashboard API for HoloMesh Interaction Modes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import json

from src.monitoring.performance_dashboard import get_performance_monitor

router = APIRouter(prefix="/api/v1/monitoring", tags=["performance-monitoring"])

@router.get("/performance/overall")
async def get_overall_performance():
    """Get overall performance across all modes"""
    try:
        monitor = get_performance_monitor()
        performance = monitor.get_overall_performance()
        return {"status": "success", "data": performance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get overall performance: {str(e)}")

@router.get("/performance/mode/{tool_name}/{interaction_mode}")
async def get_mode_performance(tool_name: str, interaction_mode: str):
    """Get performance statistics for a specific mode"""
    try:
        monitor = get_performance_monitor()
        performance = monitor.get_mode_performance(tool_name, interaction_mode)
        return {"status": "success", "data": performance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mode performance: {str(e)}")

@router.get("/performance/recent")
async def get_recent_records(limit: int = 50):
    """Get recent optimization records"""
    try:
        monitor = get_performance_monitor()
        records = monitor.get_recent_records(limit)
        return {"status": "success", "data": records, "count": len(records)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recent records: {str(e)}")

@router.get("/performance/export")
async def export_performance_data():
    """Export all monitoring data"""
    try:
        monitor = get_performance_monitor()
        data = monitor.export_data()
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export data: {str(e)}")

@router.get("/modes/supported")
async def get_supported_modes():
    """Get list of supported interaction modes"""
    modes = [
        {"value": "professional", "label": "Professional Mode", "description": "Standard optimization for general CAD tasks"},
        {"value": "innovative", "label": "Innovative Mode", "description": "Creative exploration and experimental optimization"},
        {"value": "semi_automatic", "label": "Semi-Automatic Mode", "description": "Human-AI collaboration with HoloMesh recommendations"},
        {"value": "manual", "label": "Manual Mode", "description": "Professional tool guidance with confidentiality controls"}
    ]
    return {"status": "success", "data": modes}

@router.get("/tools/supported")
async def get_supported_tools():
    """Get list of supported CAD tools"""
    tools = [
        {"value": "yosys", "label": "Yosys", "description": "Open-source synthesis tool"},
        {"value": "nextpnr", "label": "NextPNR", "description": "Open-source place and route tool"},
        {"value": "verilator", "label": "Verilator", "description": "Open-source simulator"},
        {"value": "openroad", "label": "OpenROAD", "description": "Open-source RTL-to-GDS flow"},
        {"value": "vivado", "label": "Vivado", "description": "Xilinx FPGA design suite"}
    ]
    return {"status": "success", "data": tools}
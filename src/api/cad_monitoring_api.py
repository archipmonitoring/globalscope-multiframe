"""
CAD Monitoring API for GlobalScope MultiFrame 11.0
This module provides REST API endpoints for monitoring CAD tools usage.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

# Import the CAD monitor
from src.monitoring.cad_monitor import cad_monitor, get_cad_system_health, get_cad_tool_metrics, get_all_tool_metrics

logger = logging.getLogger("CADMonitoringAPI")
router = APIRouter(prefix="/api/v1/monitoring/cad", tags=["cad-monitoring"])

@router.get("/health", response_model=Dict[str, Any])
async def cad_monitoring_health():
    """Get health status of CAD monitoring system"""
    try:
        health_status = get_cad_system_health()
        return {
            "status": "success",
            "data": health_status
        }
    except Exception as e:
        logger.error(f"Error getting CAD monitoring health: {e}")
        raise HTTPException(status_code=500, detail="Error getting CAD monitoring health")

@router.get("/overall", response_model=Dict[str, Any])
async def cad_overall_metrics():
    """Get overall CAD tools metrics"""
    try:
        metrics = cad_monitor.get_overall_metrics()
        return {
            "status": "success",
            "data": metrics
        }
    except Exception as e:
        logger.error(f"Error getting overall CAD metrics: {e}")
        raise HTTPException(status_code=500, detail="Error getting overall CAD metrics")

@router.get("/tool/{tool_name}", response_model=Dict[str, Any])
async def cad_tool_metrics(tool_name: str):
    """Get metrics for a specific CAD tool"""
    try:
        metrics = get_cad_tool_metrics(tool_name)
        if not metrics:
            raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
        
        return {
            "status": "success",
            "data": metrics
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting metrics for tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail="Error getting tool metrics")

@router.get("/all", response_model=Dict[str, Any])
async def all_cad_tool_metrics():
    """Get metrics for all CAD tools"""
    try:
        metrics = get_all_tool_metrics()
        return {
            "status": "success",
            "data": metrics
        }
    except Exception as e:
        logger.error(f"Error getting all CAD tool metrics: {e}")
        raise HTTPException(status_code=500, detail="Error getting all CAD tool metrics")

@router.get("/top-tools", response_model=Dict[str, Any])
async def top_cad_tools(count: int = 5):
    """Get top CAD tools by usage"""
    try:
        top_tools = cad_monitor.get_top_tools_by_usage(count)
        return {
            "status": "success",
            "data": {
                "count": count,
                "tools": top_tools
            }
        }
    except Exception as e:
        logger.error(f"Error getting top CAD tools: {e}")
        raise HTTPException(status_code=500, detail="Error getting top CAD tools")
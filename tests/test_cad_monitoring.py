"""
Unit tests for CAD monitoring functionality
"""
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from src.api.main_app import app

client = TestClient(app)

def test_cad_monitoring_health():
    """Test CAD monitoring health endpoint."""
    response = client.get("/api/v1/monitoring/cad/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "status" in data["data"]
    assert "overall_metrics" in data["data"]

def test_cad_overall_metrics():
    """Test overall CAD metrics endpoint."""
    response = client.get("/api/v1/monitoring/cad/overall")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "total_usage" in data["data"]
    assert "total_successes" in data["data"]
    assert "total_errors" in data["data"]

def test_all_cad_tool_metrics():
    """Test all CAD tool metrics endpoint."""
    response = client.get("/api/v1/monitoring/cad/all")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    # Should have at least the tools we know about
    known_tools = ["verilator", "yosys", "nextpnr", "iverilog", "gtkwave"]
    for tool in known_tools:
        if tool in data["data"]:
            assert "tool_name" in data["data"][tool]
            assert "usage_count" in data["data"][tool]

@patch('src.monitoring.cad_monitor.get_cad_tool_metrics')
def test_cad_tool_metrics(mock_get_metrics):
    """Test specific CAD tool metrics endpoint."""
    # Mock the response
    mock_get_metrics.return_value = {
        "tool_name": "verilator",
        "usage_count": 10,
        "success_count": 9,
        "error_count": 1,
        "average_execution_time": 1.5
    }
    
    response = client.get("/api/v1/monitoring/cad/tool/verilator")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["tool_name"] == "verilator"

    # Test for non-existent tool
    mock_get_metrics.return_value = {}
    response = client.get("/api/v1/monitoring/cad/tool/nonexistent")
    assert response.status_code == 404

@patch('src.monitoring.cad_monitor.cad_monitor.get_top_tools_by_usage')
def test_top_cad_tools(mock_get_top):
    """Test top CAD tools endpoint."""
    # Mock the response
    mock_get_top.return_value = [
        {
            "tool": "verilator",
            "usage": 100,
            "successes": 95,
            "errors": 5,
            "success_rate": 0.95,
            "avg_execution_time": 1.2
        },
        {
            "tool": "yosys",
            "usage": 80,
            "successes": 75,
            "errors": 5,
            "success_rate": 0.9375,
            "avg_execution_time": 2.1
        }
    ]
    
    response = client.get("/api/v1/monitoring/cad/top-tools?count=2")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["count"] == 2
    assert len(data["data"]["tools"]) == 2
    assert data["data"]["tools"][0]["tool"] == "verilator"

if __name__ == "__main__":
    pytest.main([__file__])
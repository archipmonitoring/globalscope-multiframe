"""
Unit tests for CAD API endpoints
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.api.main_app import app

client = TestClient(app)

def test_cad_tools_availability():
    """Test CAD tools availability endpoint."""
    response = client.get("/api/v1/cad/tools/available")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_cad_tools_versions():
    """Test CAD tools versions endpoint."""
    response = client.get("/api/v1/cad/tools/versions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_cad_health_check():
    """Test CAD health check endpoint."""
    response = client.get("/api/v1/cad/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["success", "error"]

# Mock tests for CAD operations
@patch('src.chip_design.cad_worker.run_verilator_simulation')
def test_verilator_simulation_endpoint(mock_run_simulation):
    """Test Verilator simulation endpoint."""
    # Mock the response
    mock_run_simulation.return_value = {
        "status": "success",
        "project_id": "test_project",
        "simulation_output": "test output"
    }
    
    response = client.post("/api/v1/cad/verilator/simulate", json={
        "user_id": "test_user",
        "project_id": "test_project",
        "verilog_files": [{"name": "test.v", "content": "module test; endmodule"}],
        "top_module": "test"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

@patch('src.chip_design.cad_worker.run_yosys_synthesis')
def test_yosys_synthesis_endpoint(mock_run_synthesis):
    """Test Yosys synthesis endpoint."""
    # Mock the response
    mock_run_synthesis.return_value = {
        "status": "success",
        "project_id": "test_project",
        "synthesis_output": "test output"
    }
    
    response = client.post("/api/v1/cad/yosys/synthesize", json={
        "user_id": "test_user",
        "project_id": "test_project",
        "verilog_files": [{"name": "test.v", "content": "module test; endmodule"}]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

@patch('src.chip_design.cad_worker.run_nextpnr_place_and_route')
def test_nextpnr_pnr_endpoint(mock_run_pnr):
    """Test NextPNR place and route endpoint."""
    # Mock the response
    mock_run_pnr.return_value = {
        "status": "success",
        "project_id": "test_project",
        "pnr_output": "test output"
    }
    
    response = client.post("/api/v1/cad/nextpnr/pnr", json={
        "user_id": "test_user",
        "project_id": "test_project",
        "netlist_file": "test.json"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

if __name__ == "__main__":
    pytest.main([__file__])
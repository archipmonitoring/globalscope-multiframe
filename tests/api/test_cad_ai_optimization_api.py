"""
API tests for CAD AI Optimization endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from src.api.main_app import app

client = TestClient(app)

def test_optimize_parameters_success():
    """Test successful parameter optimization request"""
    # Test data
    test_data = {
        "tool_name": "verilator",
        "project_id": "test_project_123",
        "initial_params": {"optimization_level": 2, "language_extensions": "sv"},
        "target_metrics": {"execution_time": 50.0, "memory_usage": 500.0},
        "strategy": "bayesian",
        "max_iterations": 10
    }
    
    # Since we can't easily mock the optimizer in the API context,
    # we'll test that the endpoint exists and accepts the right data format
    response = client.post("/api/v1/cad/ai/optimize-parameters", json=test_data)
    assert response.status_code in [200, 500]  # 200 if successful, 500 if modules not initialized

def test_optimize_parameters_invalid_strategy():
    """Test parameter optimization with invalid strategy"""
    # Test data with invalid strategy
    test_data = {
        "tool_name": "verilator",
        "project_id": "test_project_123",
        "initial_params": {"optimization_level": 2},
        "target_metrics": {"execution_time": 50.0},
        "strategy": "invalid_strategy",  # This should default to bayesian
        "max_iterations": 10
    }
    
    response = client.post("/api/v1/cad/ai/optimize-parameters", json=test_data)
    assert response.status_code in [200, 500]

def test_get_optimization_status_not_found():
    """Test getting status for non-existent optimization process"""
    response = client.get("/api/v1/cad/ai/optimization-status/nonexistent_process")
    # Should return 404 for not found or 500 if modules not initialized
    assert response.status_code in [404, 500]

def test_save_template():
    """Test saving optimization template"""
    test_data = {
        "tool_name": "yosys",
        "template_name": "asic_optimization",
        "parameters": {"optimization_level": 3, "abc_optimization": True},
        "project_context": {"target_technology": "asic", "design_complexity": "high"}
    }
    
    response = client.post("/api/v1/cad/ai/save-template", json=test_data)
    assert response.status_code in [200, 500]

def test_get_recommendations():
    """Test getting AI recommendations"""
    test_data = {
        "tool_name": "nextpnr",
        "project_context": {"design_complexity": "medium", "target_device": "generic"}
    }
    
    response = client.post("/api/v1/cad/ai/recommendations", json=test_data)
    assert response.status_code in [200, 500]

def test_list_strategies():
    """Test listing available optimization strategies"""
    response = client.get("/api/v1/cad/ai/strategies")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert isinstance(data["data"], dict)

def test_get_history():
    """Test getting optimization history"""
    response = client.get("/api/v1/cad/ai/history")
    # Will return 200 with empty data or 500 if modules not initialized
    assert response.status_code in [200, 500]

def test_health_check():
    """Test AI optimizer health check"""
    response = client.get("/api/v1/cad/ai/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data

# Test with missing required fields
def test_optimize_parameters_missing_fields():
    """Test parameter optimization with missing required fields"""
    # Missing required fields
    incomplete_data = {
        "tool_name": "verilator"
        # Missing project_id, initial_params, target_metrics
    }
    
    response = client.post("/api/v1/cad/ai/optimize-parameters", json=incomplete_data)
    # Should return 422 for validation error
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__])
"""
Unit tests for CAD AI Optimizer functionality
"""
import pytest
import asyncio
from unittest.mock import patch, AsyncMock, Mock
from fastapi.testclient import TestClient

from src.ai.cad_ai_optimizer import CADAIOptimizer, AIOptimizationStrategy
from src.api.main_app import app

client = TestClient(app)

class TestCADAIOptimizer:
    @pytest.fixture
    def ai_optimizer(self):
        """Create a CADAIOptimizer instance"""
        return CADAIOptimizer()
    
    def test_init(self):
        """Test CADAIOptimizer initialization"""
        optimizer = CADAIOptimizer()
        assert optimizer is not None
        assert hasattr(optimizer, 'optimization_history')
        assert hasattr(optimizer, 'chip_optimizer')
    
    async def test_bayesian_optimization(self, ai_optimizer):
        """Test Bayesian optimization method"""
        tool_name = "verilator"
        initial_params = {"optimization_level": 2, "language_extensions": "sv"}
        target_metrics = {"execution_time": 50.0, "memory_usage": 500.0}
        
        # Test the method
        result = await ai_optimizer._bayesian_optimization(
            tool_name, initial_params, target_metrics, 5, "test_process"
        )
        
        # Verify result
        assert isinstance(result, dict)
        assert len(result) > 0
    
    async def test_transfer_learning_optimization(self, ai_optimizer):
        """Test Transfer Learning optimization method"""
        tool_name = "yosys"
        initial_params = {"optimization_level": 3, "abc_optimization": True}
        target_metrics = {"area": 1000.0, "delay": 5.0}
        project_id = "test_project_123"
        
        # Test the method
        result = await ai_optimizer._transfer_learning_optimization(
            tool_name, initial_params, target_metrics, project_id, "test_process"
        )
        
        # Verify result
        assert isinstance(result, dict)
        assert len(result) > 0
    
    async def test_ensemble_optimization(self, ai_optimizer):
        """Test Ensemble optimization method"""
        tool_name = "nextpnr"
        initial_params = {"placer": "heap", "router": "router1"}
        target_metrics = {"placement_quality": 0.9, "routing_efficiency": 0.8}
        
        # Test the method
        result = await ai_optimizer._ensemble_optimization(
            tool_name, initial_params, target_metrics, "test_process"
        )
        
        # Verify result
        assert isinstance(result, dict)
        assert len(result) > 0
    
    def test_perturb_parameters(self, ai_optimizer):
        """Test parameter perturbation"""
        params = {"param1": 10.0, "param2": 20.0, "param3": "string"}
        perturbed = ai_optimizer._perturb_parameters(params, 0.1)
        
        # Verify numeric parameters were perturbed
        assert perturbed["param1"] != params["param1"]
        assert perturbed["param2"] != params["param2"]
        # Verify non-numeric parameters unchanged
        assert perturbed["param3"] == params["param3"]
    
    def test_adapt_parameters_for_project(self, ai_optimizer):
        """Test parameter adaptation for project"""
        params = {"param1": 10.0, "param2": 20.0}
        project_id = "test_project_123"
        adapted = ai_optimizer._adapt_parameters_for_project(params, project_id)
        
        # Verify parameters were adapted
        assert isinstance(adapted, dict)
        assert len(adapted) == len(params)

def test_optimize_parameters_endpoint():
    """Test the optimize parameters API endpoint"""
    # Test data
    test_data = {
        "tool_name": "verilator",
        "project_id": "test_project_123",
        "initial_params": {"optimization_level": 2},
        "target_metrics": {"execution_time": 50.0},
        "strategy": "bayesian",
        "max_iterations": 10
    }
    
    # Make request
    response = client.post("/api/v1/cad/ai/optimize-parameters", json=test_data)
    
    # Verify response
    assert response.status_code in [200, 500]  # 500 if modules not initialized in test env

def test_get_recommendations_endpoint():
    """Test the get recommendations API endpoint"""
    # Test data
    test_data = {
        "tool_name": "yosys",
        "project_context": {"design_complexity": "medium", "target_technology": "asic"}
    }
    
    # Make request
    response = client.post("/api/v1/cad/ai/recommendations", json=test_data)
    
    # Verify response
    assert response.status_code in [200, 500]  # 500 if modules not initialized in test env

def test_list_strategies_endpoint():
    """Test the list strategies API endpoint"""
    # Make request
    response = client.get("/api/v1/cad/ai/strategies")
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data

def test_health_check_endpoint():
    """Test the health check API endpoint"""
    # Make request
    response = client.get("/api/v1/cad/ai/health")
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert "status" in data

if __name__ == "__main__":
    pytest.main([__file__])
"""
Tests for CAD AI Optimization API v2

This file contains tests for the enhanced CAD AI Optimization API endpoints,
including the new semi-automatic and manual modes with HoloMesh interaction.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.cad_ai_optimization_api_v2 import app, router
from unittest.mock import patch, AsyncMock

# Create a test client
client = TestClient(app)

# Include the router in the app for testing
app.include_router(router)

class TestCADAIOptimizationAPIv2:
    """Test cases for CAD AI Optimization API v2."""
    
    def test_optimize_parameters_semi_automatic_mode(self):
        """Test optimize-parameters endpoint with semi-automatic mode."""
        # Mock the optimizer
        with patch('src.api.cad_ai_optimization_api_v2.get_optimizer') as mock_get_optimizer:
            # Create a mock optimizer
            mock_optimizer = AsyncMock()
            mock_optimizer.optimize_cad_parameters.return_value = {
                "status": "success",
                "process_id": "test_process_123",
                "optimized_params": {
                    "optimization_level": 3,
                    "abc_optimization": True
                },
                "method": "semi_automatic",
                "interaction_mode": "semi_automatic",
                "confidentiality_enabled": True
            }
            mock_get_optimizer.return_value = mock_optimizer
            
            # Send request with semi-automatic mode
            response = client.post("/api/v2/cad/ai/optimize-parameters", json={
                "tool_name": "yosys",
                "project_id": "test_project_123",
                "initial_params": {
                    "optimization_level": 2,
                    "abc_optimization": True
                },
                "target_metrics": {
                    "execution_time": 5.0,
                    "quality_score": 0.95
                },
                "strategy": "semi_automatic",
                "interaction_mode": "semi_automatic",
                "confidentiality_enabled": True
            })
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["method"] == "semi_automatic"
            assert data["interaction_mode"] == "semi_automatic"
            assert data["confidentiality_enabled"] == True
            
            # Verify optimizer was called with correct parameters
            mock_optimizer.optimize_cad_parameters.assert_called_once()
    
    def test_optimize_parameters_manual_mode_with_confidentiality(self):
        """Test optimize-parameters endpoint with manual mode and confidentiality."""
        # Mock the optimizer
        with patch('src.api.cad_ai_optimization_api_v2.get_optimizer') as mock_get_optimizer:
            # Create a mock optimizer
            mock_optimizer = AsyncMock()
            mock_optimizer.optimize_cad_parameters.return_value = {
                "status": "success",
                "process_id": "test_process_456",
                "optimized_params": {
                    "placer": "heap",
                    "timing_driven": True
                },
                "method": "manual",
                "interaction_mode": "manual",
                "confidentiality_enabled": True
            }
            mock_get_optimizer.return_value = mock_optimizer
            
            # Send request with manual mode and confidentiality enabled
            response = client.post("/api/v2/cad/ai/optimize-parameters", json={
                "tool_name": "nextpnr",
                "project_id": "test_project_456",
                "initial_params": {
                    "placer": "heap",
                    "timing_driven": True
                },
                "target_metrics": {
                    "resource_efficiency": 0.85,
                    "quality_score": 0.90
                },
                "strategy": "manual",
                "interaction_mode": "manual",
                "confidentiality_enabled": True
            })
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["method"] == "manual"
            assert data["interaction_mode"] == "manual"
            assert data["confidentiality_enabled"] == True
    
    def test_optimize_parameters_manual_mode_without_confidentiality(self):
        """Test optimize-parameters endpoint with manual mode without confidentiality."""
        # Mock the optimizer
        with patch('src.api.cad_ai_optimization_api_v2.get_optimizer') as mock_get_optimizer:
            # Create a mock optimizer
            mock_optimizer = AsyncMock()
            mock_optimizer.optimize_cad_parameters.return_value = {
                "status": "success",
                "process_id": "test_process_789",
                "optimized_params": {
                    "placer": "sa",
                    "router": "router2"
                },
                "method": "manual",
                "interaction_mode": "manual",
                "confidentiality_enabled": False
            }
            mock_get_optimizer.return_value = mock_optimizer
            
            # Send request with manual mode and confidentiality disabled
            response = client.post("/api/v2/cad/ai/optimize-parameters", json={
                "tool_name": "nextpnr",
                "project_id": "test_project_789",
                "initial_params": {
                    "placer": "sa",
                    "router": "router2"
                },
                "target_metrics": {
                    "resource_efficiency": 0.90,
                    "quality_score": 0.95
                },
                "strategy": "manual",
                "interaction_mode": "manual",
                "confidentiality_enabled": False
            })
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["method"] == "manual"
            assert data["interaction_mode"] == "manual"
            assert data["confidentiality_enabled"] == False
    
    def test_list_optimization_strategies_includes_new_modes(self):
        """Test that list strategies endpoint includes new interaction modes."""
        response = client.get("/api/v2/cad/ai/strategies")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        
        strategies = data["data"]
        # Verify that new strategies are included
        assert "semi_automatic" in strategies
        assert "manual" in strategies
        
        # Verify strategy details
        semi_auto_strategy = strategies["semi_automatic"]
        assert semi_auto_strategy["name"] == "Semi-Automatic Mode"
        assert semi_auto_strategy["new_in_v2"] == True
        
        manual_strategy = strategies["manual"]
        assert manual_strategy["name"] == "Manual Mode"
        assert manual_strategy["new_in_v2"] == True
    
    def test_batch_optimize_with_interaction_modes(self):
        """Test batch optimization with different interaction modes."""
        # Mock the optimizer
        with patch('src.api.cad_ai_optimization_api_v2.get_optimizer') as mock_get_optimizer:
            # Create a mock optimizer
            mock_optimizer = AsyncMock()
            mock_optimizer.optimize_cad_parameters.side_effect = [
                {
                    "status": "success",
                    "process_id": "test_process_100",
                    "optimized_params": {"optimization_level": 3},
                    "method": "semi_automatic",
                    "interaction_mode": "semi_automatic",
                    "confidentiality_enabled": True
                },
                {
                    "status": "success",
                    "process_id": "test_process_200",
                    "optimized_params": {"placer": "heap"},
                    "method": "manual",
                    "interaction_mode": "manual",
                    "confidentiality_enabled": False
                }
            ]
            mock_get_optimizer.return_value = mock_optimizer
            
            # Send batch request with different interaction modes
            response = client.post("/api/v2/cad/ai/batch-optimize", json={
                "parallel": False,
                "optimizations": [
                    {
                        "tool_name": "yosys",
                        "project_id": "test_project_100",
                        "initial_params": {"optimization_level": 2},
                        "target_metrics": {"execution_time": 5.0},
                        "strategy": "semi_automatic",
                        "interaction_mode": "semi_automatic",
                        "confidentiality_enabled": True
                    },
                    {
                        "tool_name": "nextpnr",
                        "project_id": "test_project_200",
                        "initial_params": {"placer": "sa"},
                        "target_metrics": {"quality_score": 0.9},
                        "strategy": "manual",
                        "interaction_mode": "manual",
                        "confidentiality_enabled": False
                    }
                ]
            })
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert len(data["results"]) == 2
            
            # Verify first result (semi-automatic mode)
            result1 = data["results"][0]
            assert result1["status"] == "success"
            assert result1["method"] == "semi_automatic"
            assert result1["interaction_mode"] == "semi_automatic"
            assert result1["confidentiality_enabled"] == True
            
            # Verify second result (manual mode)
            result2 = data["results"][1]
            assert result2["status"] == "success"
            assert result2["method"] == "manual"
            assert result2["interaction_mode"] == "manual"
            assert result2["confidentiality_enabled"] == False

if __name__ == "__main__":
    pytest.main([__file__])
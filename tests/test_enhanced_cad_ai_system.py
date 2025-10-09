"""
Comprehensive test for the enhanced CAD AI optimization system
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch

from src.ai.cad_ai_optimizer import CADAIOptimizer, GaussianProcessRegressor
from src.api.cad_ai_optimization_api_v2 import router
from fastapi.testclient import TestClient
from main import app

# Add the v2 router to the app for testing
app.include_router(router)
client = TestClient(app)


class TestEnhancedCADAISystem:
    """Test the complete enhanced CAD AI optimization system."""
    
    @pytest.fixture
    def optimizer(self):
        """Create a CADAIOptimizer instance for testing."""
        return CADAIOptimizer()
    
    @pytest.fixture
    def sample_params(self):
        """Sample CAD parameters for testing."""
        return {
            "optimization_level": 2,
            "abc_optimization": True,
            "flatten_before_synthesis": True,
            "seed": 42
        }
    
    @pytest.fixture
    def target_metrics(self):
        """Target metrics for optimization."""
        return {
            "execution_time": 10.0,
            "memory_usage": 100.0,
            "quality_score": 0.95
        }
    
    def test_gaussian_process_regressor_full_cycle(self):
        """Test the full cycle of Gaussian Process Regressor."""
        gp = GaussianProcessRegressor()
        
        # Training data (simple quadratic function)
        X_train = np.array([[1.0], [2.0], [3.0], [4.0]])
        y_train = np.array([1.0, 4.0, 9.0, 16.0])  # y = x^2
        
        # Fit the model
        gp.fit(X_train, y_train)
        
        # Test prediction
        X_test = np.array([[2.5], [3.5]])
        mu, sigma = gp.predict(X_test)
        
        # Predictions should be reasonable
        assert len(mu) == 2
        assert len(sigma) == 2
        assert all(s > 0 for s in sigma)
        
        # First prediction should be close to 6.25 (2.5^2)
        assert abs(mu[0] - 6.25) < 2.0  # Allow some error due to limited training data
    
    @pytest.mark.asyncio
    async def test_bayesian_optimization_with_gp(self, optimizer, sample_params, target_metrics):
        """Test Bayesian optimization with Gaussian Process."""
        # Mock the evaluation function
        with patch.object(optimizer, '_evaluate_parameter_configuration') as mock_eval:
            # Simulate that higher optimization_level gives better scores
            def mock_evaluation(tool_name, params, targets):
                level = params.get("optimization_level", 0)
                return 0.5 + 0.1 * level  # Higher level = higher score
            
            mock_eval.side_effect = mock_evaluation
            
            # Run Bayesian optimization
            result = await optimizer._bayesian_optimization(
                "yosys", sample_params, target_metrics, max_iterations=15, process_id="test_process"
            )
            
            # Should have tried to improve the parameters
            assert isinstance(result, dict)
            assert "optimization_level" in result
    
    @pytest.mark.asyncio
    async def test_transfer_learning_with_database(self, optimizer, sample_params, target_metrics):
        """Test transfer learning with project database."""
        # Add a similar project to the database
        optimizer.project_database["similar_project"] = {
            "project_id": "similar_project",
            "tool_name": "yosys",
            "optimal_config": {
                "optimization_level": 3,
                "abc_optimization": True,
                "flatten_before_synthesis": True,
                "seed": 123
            },
            "context": {"chip_type": "fpga"},
            "similarity": 0.9
        }
        
        # Add the current project context
        optimizer.project_database["current_project"] = {
            "project_id": "current_project",
            "tool_name": "yosys",
            "context": {"chip_type": "fpga"}
        }
        
        # Mock the fine-tuning function
        with patch.object(optimizer, '_fine_tune_parameters') as mock_fine_tune:
            mock_fine_tune.return_value = {
                "optimization_level": 3,
                "abc_optimization": True,
                "flatten_before_synthesis": True,
                "seed": 125
            }
            
            result = await optimizer._transfer_learning_optimization(
                "yosys", sample_params, target_metrics, "current_project", "test_process"
            )
            
            # Should have used the similar project data
            assert isinstance(result, dict)
            assert result["optimization_level"] == 3
    
    @pytest.mark.asyncio
    async def test_ensemble_optimization_weighted_combination(self, optimizer, sample_params, target_metrics):
        """Test ensemble optimization with weighted combination."""
        # Mock the individual optimization methods
        with patch.object(optimizer, '_bayesian_optimization') as mock_bayesian, \
             patch.object(optimizer, '_transfer_learning_optimization') as mock_transfer:
            
            # Mock Bayesian optimization result
            mock_bayesian.return_value = {
                "param1": 1.0,
                "param2": 2.0
            }
            
            # Mock Transfer Learning result
            mock_transfer.return_value = {
                "param1": 3.0,
                "param2": 4.0
            }
            
            # Run ensemble optimization
            result = await optimizer._ensemble_optimization(
                "yosys", sample_params, target_metrics, "test_process"
            )
            
            # Should have combined results
            assert isinstance(result, dict)
            assert "param1" in result
            assert "param2" in result
    
    def test_parameter_vectorization_cycle(self, optimizer, sample_params):
        """Test parameter vectorization and de-vectorization cycle."""
        param_names = list(sample_params.keys())
        bounds = optimizer._get_parameter_bounds("yosys", param_names)
        
        # Convert to vector
        vector = optimizer._params_to_vector(sample_params, param_names, bounds)
        
        # Convert back
        restored_params = optimizer._vector_to_params(vector, param_names, bounds, sample_params)
        
        # Check that values are preserved (with some tolerance for normalization)
        assert restored_params["abc_optimization"] == sample_params["abc_optimization"]
        assert restored_params["flatten_before_synthesis"] == sample_params["flatten_before_synthesis"]
        assert restored_params["optimization_level"] == sample_params["optimization_level"]
    
    @pytest.mark.asyncio
    async def test_full_optimization_api_integration(self):
        """Test full integration of the optimization API."""
        # Mock the optimizer
        with patch('src.api.cad_ai_optimization_api_v2.get_optimizer') as mock_get_optimizer:
            mock_optimizer = Mock()
            mock_optimizer.optimize_cad_parameters.return_value = {
                "status": "success",
                "process_id": "test_process_123",
                "optimized_params": {"optimization_level": 3},
                "final_metrics": {"execution_time": 5.0},
                "method": "bayesian",
                "iterations": 30,
                "confidence_score": 0.85,
                "execution_time": 1.23
            }
            mock_get_optimizer.return_value = mock_optimizer
            
            # Make request to the API
            response = client.post("/api/v2/cad/ai/optimize-parameters", json={
                "tool_name": "yosys",
                "project_id": "test_project",
                "initial_params": {"optimization_level": 1},
                "target_metrics": {"execution_time": 5.0},
                "strategy": "bayesian",
                "max_iterations": 30,
                "project_context": {"chip_type": "fpga"}
            })
            
            # Check response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["process_id"] == "test_process_123"
            assert data["method"] == "bayesian"
            assert "confidence_score" in data
            assert "execution_time" in data
    
    @pytest.mark.asyncio
    async def test_project_database_api_integration(self):
        """Test project database API integration."""
        # Mock the optimizer
        with patch('src.api.cad_ai_optimization_api_v2.get_optimizer') as mock_get_optimizer:
            mock_optimizer = Mock()
            mock_optimizer.project_database = {}
            mock_get_optimizer.return_value = mock_optimizer
            
            # Make request to add project to database
            response = client.post("/api/v2/cad/ai/project-database", json={
                "project_id": "test_project",
                "tool_name": "yosys",
                "optimal_config": {"optimization_level": 3},
                "context": {"chip_type": "fpga"},
                "performance_metrics": {"execution_time": 5.0},
                "chip_type": "fpga",
                "technology_node": "28nm"
            })
            
            # Check response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["project_id"] == "test_project"
    
    @pytest.mark.asyncio
    async def test_recommendations_api_integration(self):
        """Test recommendations API integration."""
        # Mock the optimizer
        with patch('src.api.cad_ai_optimization_api_v2.get_optimizer') as mock_get_optimizer:
            mock_optimizer = Mock()
            mock_optimizer.get_recommendations.return_value = {
                "status": "success",
                "data": {
                    "recommended_parameters": {"optimization_level": 2},
                    "confidence_score": 0.9,
                    "similar_projects_used": 3,
                    "explanation": "AI-generated recommendations"
                },
                "source": "generated"
            }
            mock_get_optimizer.return_value = mock_optimizer
            
            # Make request to get recommendations
            response = client.post("/api/v2/cad/ai/recommendations", json={
                "tool_name": "yosys",
                "project_context": {"chip_type": "fpga"}
            })
            
            # Check response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["source"] == "generated"
            assert "confidence_score" in data
            assert "similar_projects_used" in data


# Import numpy for the tests
import numpy as np

if __name__ == "__main__":
    pytest.main([__file__])
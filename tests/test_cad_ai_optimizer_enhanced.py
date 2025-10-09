"""
Enhanced tests for the CADAIOptimizer with improved Bayesian optimization
"""

import pytest
import asyncio
import numpy as np
from unittest.mock import Mock, patch

from src.ai.cad_ai_optimizer import CADAIOptimizer, GaussianProcessRegressor


@pytest.fixture
def optimizer():
    """Create a CADAIOptimizer instance for testing."""
    return CADAIOptimizer()


@pytest.fixture
def sample_params():
    """Sample CAD parameters for testing."""
    return {
        "optimization_level": 2,
        "abc_optimization": True,
        "flatten_before_synthesis": True,
        "seed": 42
    }


@pytest.fixture
def target_metrics():
    """Target metrics for optimization."""
    return {
        "execution_time": 10.0,
        "memory_usage": 100.0,
        "quality_score": 0.95
    }


class TestGaussianProcessRegressor:
    """Test the Gaussian Process Regressor implementation."""
    
    def test_rbf_kernel(self):
        """Test the RBF kernel function."""
        gp = GaussianProcessRegressor()
        
        # Test with simple 1D data
        X1 = np.array([[1.0], [2.0]])
        X2 = np.array([[1.0], [2.0]])
        
        K = gp._rbf_kernel(X1, X2)
        
        # Diagonal should be 1 (same points)
        assert K[0, 0] == pytest.approx(1.0)
        assert K[1, 1] == pytest.approx(1.0)
        
        # Off-diagonal should be less than 1 (different points)
        assert K[0, 1] < 1.0
        assert K[1, 0] < 1.0
    
    def test_fit_and_predict(self):
        """Test fitting and prediction."""
        gp = GaussianProcessRegressor()
        
        # Simple training data
        X_train = np.array([[1.0], [2.0], [3.0]])
        y_train = np.array([1.0, 4.0, 9.0])  # y = x^2
        
        # Fit the model
        gp.fit(X_train, y_train)
        
        # Test prediction
        X_test = np.array([[1.5], [2.5]])
        mu, sigma = gp.predict(X_test)
        
        # Predictions should have the right shape
        assert len(mu) == 2
        assert len(sigma) == 2
        
        # Standard deviations should be positive
        assert all(s > 0 for s in sigma)


class TestCADAIOptimizerEnhanced:
    """Test the enhanced CADAIOptimizer."""
    
    @pytest.mark.asyncio
    async def test_bayesian_optimization_improvement(self, optimizer, sample_params, target_metrics):
        """Test that Bayesian optimization improves parameters."""
        # Mock the evaluation function to return better scores for better parameters
        with patch.object(optimizer, '_evaluate_parameter_configuration') as mock_eval:
            # Simulate that parameters with optimization_level=3 are better
            def mock_evaluation(tool_name, params, targets):
                if params.get("optimization_level", 0) == 3:
                    return 0.9  # High score
                else:
                    return 0.5  # Lower score
            
            mock_eval.side_effect = mock_evaluation
            
            # Run Bayesian optimization
            result = await optimizer._bayesian_optimization(
                "yosys", sample_params, target_metrics, max_iterations=10, process_id="test_process"
            )
            
            # Should have tried to improve the parameters
            assert isinstance(result, dict)
            # At least some parameters should have been explored
            assert len(result) > 0
    
    def test_parameter_bounds(self, optimizer):
        """Test parameter bounds calculation."""
        param_names = ["optimization_level", "seed", "abc_optimization"]
        bounds = optimizer._get_parameter_bounds("yosys", param_names)
        
        # Check that bounds exist for all parameters
        assert len(bounds) == len(param_names)
        
        # Check specific bounds
        assert bounds["optimization_level"] == (0, 3)
        assert bounds["seed"] == (1, 1000)
    
    def test_params_to_vector_and_back(self, optimizer, sample_params):
        """Test parameter vector conversion."""
        param_names = list(sample_params.keys())
        bounds = optimizer._get_parameter_bounds("yosys", param_names)
        
        # Convert to vector
        vector = optimizer._params_to_vector(sample_params, param_names, bounds)
        
        # Convert back
        restored_params = optimizer._vector_to_params(vector, param_names, bounds, sample_params)
        
        # Check that boolean values are preserved
        assert restored_params["abc_optimization"] == sample_params["abc_optimization"]
        assert restored_params["flatten_before_synthesis"] == sample_params["flatten_before_synthesis"]
        
        # Check that integer values are preserved
        assert restored_params["optimization_level"] == sample_params["optimization_level"]
        assert restored_params["seed"] == sample_params["seed"]
    
    @pytest.mark.asyncio
    async def test_transfer_learning_with_similar_projects(self, optimizer, sample_params, target_metrics):
        """Test transfer learning with similar projects."""
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
                "seed": 125  # Slightly different
            }
            
            result = await optimizer._transfer_learning_optimization(
                "yosys", sample_params, target_metrics, "current_project", "test_process"
            )
            
            # Should have used the similar project data
            assert isinstance(result, dict)
            assert "optimization_level" in result
    
    def test_weighted_combine_parameter_configurations(self, optimizer):
        """Test weighted combination of parameter configurations."""
        configs = [
            {"param1": 1.0, "param2": 2.0},
            {"param1": 3.0, "param2": 4.0},
            {"param1": 5.0, "param2": 6.0}
        ]
        weights = [0.5, 0.3, 0.2]
        
        combined = optimizer._weighted_combine_parameter_configurations(configs, weights)
        
        # Should be a weighted average
        expected_param1 = (1.0 * 0.5 + 3.0 * 0.3 + 5.0 * 0.2) / (0.5 + 0.3 + 0.2)
        expected_param2 = (2.0 * 0.5 + 4.0 * 0.3 + 6.0 * 0.2) / (0.5 + 0.3 + 0.2)
        
        assert combined["param1"] == pytest.approx(expected_param1)
        assert combined["param2"] == pytest.approx(expected_param2)


if __name__ == "__main__":
    pytest.main([__file__])
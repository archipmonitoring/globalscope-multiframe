"""
Tests for HoloMesh Interaction Modes in CAD AI Optimization

This file contains tests for the new semi-automatic and manual modes
with HoloMesh integration for professional and innovative tool interactions.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from src.ai.cad_ai_optimizer import (
    CADAIOptimizer, 
    AIOptimizationStrategy, 
    InteractionMode,
    CADParameterConfig
)

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
        "flatten_before_synthesis": True
    }

@pytest.fixture
def target_metrics():
    """Sample target metrics for testing."""
    return {
        "execution_time": 5.0,
        "quality_score": 0.95
    }

class TestHoloMeshInteractionModes:
    """Test cases for HoloMesh interaction modes."""
    
    @pytest.mark.asyncio
    async def test_semi_automatic_optimization(self, optimizer, sample_params, target_metrics):
        """Test semi-automatic optimization with HoloMesh interaction."""
        # Mock the holomesh interface
        optimizer.holomesh_interface = Mock()
        optimizer.holomesh_interface.get_recommendations.return_value = {
            "optimization_level": 3,
            "abc_optimization": True
        }
        
        result = await optimizer._semi_automatic_optimization(
            tool_name="yosys",
            initial_params=sample_params,
            target_metrics=target_metrics,
            interaction_mode=InteractionMode.SEMI_AUTOMATIC,
            process_id="test_process_001"
        )
        
        # Verify that the result is a dictionary
        assert isinstance(result, dict)
        # Verify that the optimization completed
        assert len(result) > 0
        
        # Verify that HoloMesh recommendations were applied
        optimizer.holomesh_interface.get_recommendations.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_manual_optimization_with_confidentiality(self, optimizer, sample_params, target_metrics):
        """Test manual optimization with confidentiality enabled."""
        # Mock the holomesh interface
        optimizer.holomesh_interface = Mock()
        optimizer.holomesh_interface.get_tool_guidance.return_value = {
            "placer": "heap",
            "timing_driven": True
        }
        
        # Enable confidentiality mode
        optimizer.confidentiality_mode = True
        
        result = await optimizer._manual_optimization(
            tool_name="nextpnr",
            initial_params=sample_params,
            target_metrics=target_metrics,
            interaction_mode=InteractionMode.MANUAL,
            process_id="test_process_002"
        )
        
        # Verify that the result is a dictionary
        assert isinstance(result, dict)
        # Verify that the optimization completed
        assert len(result) > 0
        
        # Verify confidentiality mode is enabled
        assert optimizer.confidentiality_mode == True
    
    @pytest.mark.asyncio
    async def test_manual_optimization_without_confidentiality(self, optimizer, sample_params, target_metrics):
        """Test manual optimization with confidentiality disabled."""
        # Mock the holomesh interface
        optimizer.holomesh_interface = Mock()
        optimizer.holomesh_interface.get_tool_guidance.return_value = {
            "placer": "sa",
            "router": "router2"
        }
        
        # Disable confidentiality mode
        optimizer.confidentiality_mode = False
        
        result = await optimizer._manual_optimization(
            tool_name="nextpnr",
            initial_params=sample_params,
            target_metrics=target_metrics,
            interaction_mode=InteractionMode.MANUAL,
            process_id="test_process_003"
        )
        
        # Verify that the result is a dictionary
        assert isinstance(result, dict)
        # Verify that the optimization completed
        assert len(result) > 0
        
        # Verify confidentiality mode is disabled
        assert optimizer.confidentiality_mode == False
    
    def test_apply_holomesh_recommendations(self, optimizer, sample_params):
        """Test applying HoloMesh recommendations to parameters."""
        recommendations = {
            "optimization_level": 3,
            "abc_optimization": False
        }
        
        result = optimizer._apply_holomesh_recommendations(sample_params, recommendations)
        
        # Verify that the result is a dictionary
        assert isinstance(result, dict)
        # Verify that recommendations were applied with weighted average
        assert result["optimization_level"] == pytest.approx(2.3)  # 70% old + 30% new
        assert result["abc_optimization"] == False  # Boolean values are directly applied
    
    def test_apply_tool_guidance(self, optimizer, sample_params):
        """Test applying professional tool guidance to parameters."""
        guidance = {
            "optimization_level": 3,
            "flatten_before_synthesis": False
        }
        
        result = optimizer._apply_tool_guidance(sample_params, guidance)
        
        # Verify that the result is a dictionary
        assert isinstance(result, dict)
        # Verify that guidance was applied with conservative approach
        assert result["optimization_level"] == pytest.approx(2.1)  # 90% old + 10% new
        assert result["flatten_before_synthesis"] == False  # Boolean values are directly applied
    
    @pytest.mark.asyncio
    async def test_optimize_cad_parameters_with_semi_automatic_mode(self, optimizer, sample_params, target_metrics):
        """Test full optimization with semi-automatic mode."""
        # Mock required methods
        with patch.object(optimizer, '_semi_automatic_optimization') as mock_semi_auto, \
             patch.object(optimizer, '_send_websocket_update'), \
             patch.object(optimizer, '_get_cached_optimal_config', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_cache', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_queue', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_websocket_manager', return_value=None):
            
            # Mock the semi-automatic optimization to return sample results
            mock_semi_auto.return_value = {
                "optimization_level": 3,
                "abc_optimization": True,
                "execution_time": 4.5
            }
            
            result = await optimizer.optimize_cad_parameters(
                tool_name="yosys",
                project_id="test_project_001",
                initial_params=sample_params,
                target_metrics=target_metrics,
                strategy=AIOptimizationStrategy.SEMI_AUTOMATIC,
                max_iterations=10,
                interaction_mode=InteractionMode.SEMI_AUTOMATIC,
                confidentiality_enabled=True
            )
            
            # Verify that the result is successful
            assert result["status"] == "success"
            # Verify that the method was called
            mock_semi_auto.assert_called_once()
            # Verify that interaction mode is correctly set
            assert result["interaction_mode"] == "semi_automatic"
            # Verify that confidentiality is correctly set
            assert result["confidentiality_enabled"] == True
    
    @pytest.mark.asyncio
    async def test_optimize_cad_parameters_with_manual_mode(self, optimizer, sample_params, target_metrics):
        """Test full optimization with manual mode."""
        # Mock required methods
        with patch.object(optimizer, '_manual_optimization') as mock_manual, \
             patch.object(optimizer, '_send_websocket_update'), \
             patch.object(optimizer, '_get_cached_optimal_config', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_cache', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_queue', return_value=None), \
             patch('src.ai.cad_ai_optimizer.get_cad_websocket_manager', return_value=None):
            
            # Mock the manual optimization to return sample results
            mock_manual.return_value = {
                "placer": "heap",
                "timing_driven": True,
                "resource_efficiency": 0.88
            }
            
            result = await optimizer.optimize_cad_parameters(
                tool_name="nextpnr",
                project_id="test_project_002",
                initial_params=sample_params,
                target_metrics=target_metrics,
                strategy=AIOptimizationStrategy.MANUAL,
                max_iterations=10,
                interaction_mode=InteractionMode.MANUAL,
                confidentiality_enabled=False
            )
            
            # Verify that the result is successful
            assert result["status"] == "success"
            # Verify that the method was called
            mock_manual.assert_called_once()
            # Verify that interaction mode is correctly set
            assert result["interaction_mode"] == "manual"
            # Verify that confidentiality is correctly set
            assert result["confidentiality_enabled"] == False

class TestCADParameterConfig:
    """Test cases for CADParameterConfig dataclass."""
    
    def test_cad_parameter_config_creation(self):
        """Test creating a CADParameterConfig instance."""
        config = CADParameterConfig(
            tool_name="yosys",
            parameters={"optimization_level": 2},
            performance_metrics={"execution_time": 5.0},
            project_context={"chip_type": "FPGA"},
            interaction_mode="semi_automatic",
            confidentiality_enabled=True
        )
        
        # Verify all fields are set correctly
        assert config.tool_name == "yosys"
        assert config.parameters == {"optimization_level": 2}
        assert config.performance_metrics == {"execution_time": 5.0}
        assert config.project_context == {"chip_type": "FPGA"}
        assert config.interaction_mode == "semi_automatic"
        assert config.confidentiality_enabled == True
        # Verify that created_at is set automatically
        assert config.created_at > 0
    
    def test_cad_parameter_config_default_values(self):
        """Test CADParameterConfig with default values."""
        config = CADParameterConfig(
            tool_name="verilator",
            parameters={"language_extensions": "sv"},
            performance_metrics={"quality_score": 0.9},
            project_context={"application_domain": "simulation"}
        )
        
        # Verify default values
        assert config.interaction_mode == "professional"
        assert config.confidentiality_enabled == True
        # Verify that created_at is set automatically
        assert config.created_at > 0

if __name__ == "__main__":
    pytest.main([__file__])
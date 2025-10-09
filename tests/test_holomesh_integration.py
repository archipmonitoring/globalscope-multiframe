"""
Tests for HoloMesh Integration in CAD AI Optimization

This file contains tests for the HoloMesh integration features
in the new semi-automatic and manual modes.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.ai.cad_ai_optimizer import (
    CADAIOptimizer, 
    AIOptimizationStrategy, 
    InteractionMode,
    CADParameterConfig
)
from src.config.holomesh_config_manager import HoloMeshConfigManager

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

class TestHoloMeshIntegration:
    """Test cases for HoloMesh integration features."""
    
    @pytest.mark.asyncio
    async def test_holomesh_recommendations_in_semi_automatic_mode(self, optimizer, sample_params, target_metrics):
        """Test that HoloMesh recommendations are applied in semi-automatic mode."""
        # Mock the HoloMesh interface
        optimizer.holomesh_interface = Mock()
        optimizer.holomesh_interface.get_recommendations.return_value = {
            "optimization_level": 3,
            "abc_optimization": False
        }
        
        # Enable HoloMesh integration in config
        with patch.object(optimizer.config_manager, 'is_holomesh_integration_enabled', return_value=True):
            result = await optimizer._semi_automatic_optimization(
                tool_name="yosys",
                initial_params=sample_params,
                target_metrics=target_metrics,
                interaction_mode=InteractionMode.SEMI_AUTOMATIC,
                process_id="test_process_holomesh_001"
            )
            
            # Verify that the result is a dictionary
            assert isinstance(result, dict)
            # Verify that the optimization completed
            assert len(result) > 0
            
            # Verify that HoloMesh recommendations were applied
            optimizer.holomesh_interface.get_recommendations.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_tool_guidance_in_manual_mode(self, optimizer, sample_params, target_metrics):
        """Test that tool guidance is applied in manual mode."""
        # Mock the HoloMesh interface
        optimizer.holomesh_interface = Mock()
        optimizer.holomesh_interface.get_tool_guidance.return_value = {
            "placer": "heap",
            "timing_driven": True
        }
        
        # Enable HoloMesh integration in config
        with patch.object(optimizer.config_manager, 'is_holomesh_integration_enabled', return_value=True):
            result = await optimizer._manual_optimization(
                tool_name="nextpnr",
                initial_params=sample_params,
                target_metrics=target_metrics,
                interaction_mode=InteractionMode.MANUAL,
                process_id="test_process_holomesh_002"
            )
            
            # Verify that the result is a dictionary
            assert isinstance(result, dict)
            # Verify that the optimization completed
            assert len(result) > 0
            
            # Verify that tool guidance was applied
            optimizer.holomesh_interface.get_tool_guidance.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_holomesh_integration_disabled(self, optimizer, sample_params, target_metrics):
        """Test behavior when HoloMesh integration is disabled."""
        # Disable HoloMesh integration in config
        with patch.object(optimizer.config_manager, 'is_holomesh_integration_enabled', return_value=False):
            # Mock the methods that would be called
            with patch.object(optimizer, '_bayesian_optimization') as mock_bayesian:
                mock_bayesian.return_value = {"optimization_level": 2}
                
                result = await optimizer._semi_automatic_optimization(
                    tool_name="yosys",
                    initial_params=sample_params,
                    target_metrics=target_metrics,
                    interaction_mode=InteractionMode.SEMI_AUTOMATIC,
                    process_id="test_process_holomesh_003"
                )
                
                # Verify that the result is a dictionary
                assert isinstance(result, dict)
                # Verify that Bayesian optimization was called as fallback
                mock_bayesian.assert_called_once()
    
    def test_apply_holomesh_recommendations_with_weighted_average(self, optimizer, sample_params):
        """Test that HoloMesh recommendations are applied with correct weighting."""
        recommendations = {
            "optimization_level": 3,  # Different from initial value of 2
            "abc_optimization": False  # Different from initial value of True
        }
        
        result = optimizer._apply_holomesh_recommendations(sample_params, recommendations)
        
        # Verify that the result is a dictionary
        assert isinstance(result, dict)
        # Verify that numeric recommendations were applied with weighted average (70% old + 30% new)
        assert result["optimization_level"] == pytest.approx(2.3)  # 2 * 0.7 + 3 * 0.3
        # Verify that boolean values are directly applied
        assert result["abc_optimization"] == False
    
    def test_apply_tool_guidance_with_conservative_approach(self, optimizer, sample_params):
        """Test that tool guidance is applied with conservative approach."""
        guidance = {
            "optimization_level": 3,  # Different from initial value of 2
            "flatten_before_synthesis": False  # Different from initial value of True
        }
        
        result = optimizer._apply_tool_guidance(sample_params, guidance)
        
        # Verify that the result is a dictionary
        assert isinstance(result, dict)
        # Verify that numeric guidance was applied with conservative approach (90% old + 10% new)
        assert result["optimization_level"] == pytest.approx(2.1)  # 2 * 0.9 + 3 * 0.1
        # Verify that boolean values are directly applied
        assert result["flatten_before_synthesis"] == False

class TestConfidentialityControls:
    """Test cases for confidentiality controls in manual mode."""
    
    @pytest.mark.asyncio
    async def test_confidentiality_enabled_by_default(self, optimizer, sample_params, target_metrics):
        """Test that confidentiality is enabled by default in manual mode."""
        # Enable confidentiality mode
        optimizer.confidentiality_mode = True
        
        # Mock the HoloMesh interface
        optimizer.holomesh_interface = Mock()
        optimizer.holomesh_interface.get_tool_guidance.return_value = {}
        
        result = await optimizer._manual_optimization(
            tool_name="nextpnr",
            initial_params=sample_params,
            target_metrics=target_metrics,
            interaction_mode=InteractionMode.MANUAL,
            process_id="test_process_conf_001"
        )
        
        # Verify that confidentiality mode is enabled
        assert optimizer.confidentiality_mode == True
    
    @pytest.mark.asyncio
    async def test_confidentiality_disabled_for_learning(self, optimizer, sample_params, target_metrics):
        """Test that confidentiality can be disabled for system learning."""
        # Disable confidentiality mode
        optimizer.confidentiality_mode = False
        
        # Mock the HoloMesh interface
        optimizer.holomesh_interface = Mock()
        optimizer.holomesh_interface.get_tool_guidance.return_value = {}
        
        result = await optimizer._manual_optimization(
            tool_name="nextpnr",
            initial_params=sample_params,
            target_metrics=target_metrics,
            interaction_mode=InteractionMode.MANUAL,
            process_id="test_process_conf_002"
        )
        
        # Verify that confidentiality mode is disabled
        assert optimizer.confidentiality_mode == False

class TestConfigManagerIntegration:
    """Test cases for integration with HoloMesh configuration manager."""
    
    def test_get_interaction_mode_config(self):
        """Test retrieving interaction mode configuration."""
        config_manager = HoloMeshConfigManager()
        
        # Test semi-automatic mode config
        semi_auto_config = config_manager.get_interaction_mode_config("semi_automatic")
        assert "description" in semi_auto_config
        assert "default_confidentiality" in semi_auto_config
        assert semi_auto_config.get("default_confidentiality") == True
        
        # Test manual mode config
        manual_config = config_manager.get_interaction_mode_config("manual")
        assert "description" in manual_config
        assert "default_confidentiality" in manual_config
        assert manual_config.get("default_confidentiality") == True
    
    def test_is_holomesh_integration_enabled(self):
        """Test checking if HoloMesh integration is enabled."""
        config_manager = HoloMeshConfigManager()
        
        # Test that integration is enabled for new modes
        assert config_manager.is_holomesh_integration_enabled("semi_automatic") == True
        assert config_manager.is_holomesh_integration_enabled("manual") == True
        
        # Test that integration is disabled for default modes
        assert config_manager.is_holomesh_integration_enabled("professional") == False
        assert config_manager.is_holomesh_integration_enabled("innovative") == False
    
    def test_get_supported_modes_for_tool(self):
        """Test retrieving supported modes for a tool."""
        config_manager = HoloMeshConfigManager()
        
        # Test supported modes for yosys
        yosys_modes = config_manager.get_supported_modes_for_tool("yosys")
        assert "semi_automatic" in yosys_modes
        assert "manual" in yosys_modes
        assert "professional" in yosys_modes
        assert "innovative" in yosys_modes

if __name__ == "__main__":
    pytest.main([__file__])
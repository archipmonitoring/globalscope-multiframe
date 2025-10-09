"""
Integration tests for chip design components including:
- ChipAutonomousDesigner
- ChipArchitectureAnalyzer
- ChipQualityAssurance
- ChipLifecycleTracker
"""

import sys
import os
import asyncio
import pytest
import json
from typing import Dict, Any
from unittest.mock import AsyncMock, patch

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the classes directly from their modules
from chip_design.chip_autonomous_designer import ChipAutonomousDesigner
from chip_design.chip_architecture_analyzer import ChipArchitectureAnalyzer
from chip_design.chip_quality_assurance import ChipQualityAssurance
from chip_design.chip_lifecycle_tracker import ChipLifecycleTracker, ChipLifecycleStage

# Create a simple data class for design requirements since it's not directly importable
class DesignRequirements:
    def __init__(self, chip_name, target_frequency, target_power, target_area, 
                 ai_acceleration=True, ml_inference_optimized=True, 
                 security_features=True, reliability_target=0.999):
        self.chip_name = chip_name
        self.target_frequency = target_frequency
        self.target_power = target_power
        self.target_area = target_area
        self.ai_acceleration = ai_acceleration
        self.ml_inference_optimized = ml_inference_optimized
        self.security_features = security_features
        self.reliability_target = reliability_target

class TestChipDesignIntegration:
    """Integration tests for chip design components"""
    
    @pytest.fixture
    def design_requirements(self) -> DesignRequirements:
        """Create test design requirements"""
        return DesignRequirements(
            chip_name="TestChipAI",
            target_frequency=2.5,  # GHz
            target_power=5.0,  # Watts
            target_area=100.0,  # mm²
            ai_acceleration=True,
            ml_inference_optimized=True,
            security_features=True,
            reliability_target=0.999
        )
    
    @pytest.fixture
    def analyzer(self) -> ChipArchitectureAnalyzer:
        """Create chip architecture analyzer"""
        return ChipArchitectureAnalyzer()
    
    @pytest.fixture
    def designer(self) -> ChipAutonomousDesigner:
        """Create chip autonomous designer"""
        return ChipAutonomousDesigner()
    
    @pytest.fixture
    def qa(self) -> ChipQualityAssurance:
        """Create chip quality assurance"""
        return ChipQualityAssurance()
    
    @pytest.fixture
    def lifecycle_tracker(self) -> ChipLifecycleTracker:
        """Create chip lifecycle tracker"""
        return ChipLifecycleTracker()
    
    @pytest.mark.asyncio
    async def test_full_chip_design_lifecycle(self, design_requirements, designer, analyzer, qa, lifecycle_tracker):
        """Test the complete chip design lifecycle from autonomous design to quality assurance"""
        # Step 1: Autonomous Design
        print("Step 1: Starting autonomous chip design...")
        # Use the correct method signature
        design_result = await designer.start_autonomous_design(
            "test_user", 
            "test_project", 
            {
                "performance_target": design_requirements.target_frequency,
                "power_limit": design_requirements.target_power,
                "area_limit": design_requirements.target_area
            }
        )
        
        # Verify design session was created
        assert design_result is not None
        assert design_result["status"] == "success"
        
        # Step 2: Architecture Analysis
        print("Step 2: Analyzing chip architecture...")
        # Create mock architecture data for testing
        mock_architecture = {
            "components": [
                {"name": "cpu_core", "type": "processing", "complexity": 0.8},
                {"name": "memory_controller", "type": "memory", "complexity": 0.6},
                {"name": "ai_accelerator", "type": "accelerator", "complexity": 0.9}
            ],
            "connections": [
                {"source": "cpu_core", "target": "memory_controller", "bandwidth": 100},
                {"source": "cpu_core", "target": "ai_accelerator", "bandwidth": 200}
            ],
            "constraints": {
                "target_frequency": design_requirements.target_frequency,
                "target_power": design_requirements.target_power,
                "target_area": design_requirements.target_area
            }
        }
        
        analysis_result = await analyzer.analyze_architecture("test_project", mock_architecture)
        
        # Verify analysis results
        assert analysis_result is not None
        assert analysis_result["status"] == "success"
        assert "analysis_data" in analysis_result
        
        # Step 3: Quality Assurance
        print("Step 3: Performing quality assurance...")
        qa_results = await qa.perform_quality_assurance("test_project", analysis_result["analysis_data"])
        
        # Verify QA results
        assert qa_results is not None
        assert qa_results["status"] == "success"
        assert "quality_metrics" in qa_results
        
        # Step 4: Lifecycle Tracking - Design Stage
        print("Step 4: Tracking lifecycle - Design stage...")
        await lifecycle_tracker.register_chip("test_project", {
            "design_requirements": {
                "performance_target": design_requirements.target_frequency,
                "power_limit": design_requirements.target_power,
                "area_limit": design_requirements.target_area
            }
        })
        
        lifecycle_result = await lifecycle_tracker.update_lifecycle_stage(
            "test_project", 
            ChipLifecycleStage.DESIGN, 
            {
                "design_data": mock_architecture,
                "analysis_results": analysis_result["analysis_data"],
                "qa_results": qa_results["quality_metrics"]
            }
        )
        
        # Verify lifecycle tracking
        assert lifecycle_result is not None
        assert lifecycle_result["status"] == "success"
        
        lifecycle_status = await lifecycle_tracker.get_lifecycle_status("test_project")
        assert lifecycle_status is not None
        assert lifecycle_status["status"] == "success"
        assert lifecycle_status["current_stage"] == ChipLifecycleStage.DESIGN.value
        
        print("Full chip design lifecycle test completed successfully!")
    
    @pytest.mark.asyncio
    async def test_autonomous_design_with_optimization(self, design_requirements, designer, analyzer):
        """Test autonomous design with optimization loop"""
        print("Testing autonomous design with optimization...")
        
        # Perform initial design
        initial_design = await designer.start_autonomous_design(
            "test_user", 
            "test_project_opt", 
            {
                "performance_target": design_requirements.target_frequency,
                "power_limit": design_requirements.target_power,
                "area_limit": design_requirements.target_area
            }
        )
        assert initial_design is not None
        assert initial_design["status"] == "success"
        
        # Create mock architecture data for testing
        mock_architecture = {
            "components": [
                {"name": "cpu_core", "type": "processing", "complexity": 0.7},
                {"name": "memory_controller", "type": "memory", "complexity": 0.5}
            ],
            "connections": [
                {"source": "cpu_core", "target": "memory_controller", "bandwidth": 80}
            ],
            "constraints": {
                "target_frequency": design_requirements.target_frequency,
                "target_power": design_requirements.target_power,
                "target_area": design_requirements.target_area
            }
        }
        
        # Analyze initial design
        initial_analysis = await analyzer.analyze_architecture("test_project_opt", mock_architecture)
        assert initial_analysis is not None
        assert initial_analysis["status"] == "success"
        
        print("Design optimization test completed successfully!")
    
    @pytest.mark.asyncio
    async def test_quality_assurance_predictions(self, analyzer, qa):
        """Test quality assurance prediction capabilities"""
        print("Testing quality assurance predictions...")
        
        # Create mock architecture data
        mock_architecture = {
            "components": [
                {"name": "cpu_core", "type": "processing", "complexity": 0.8},
                {"name": "memory_controller", "type": "memory", "complexity": 0.6},
                {"name": "ai_accelerator", "type": "accelerator", "complexity": 0.9}
            ],
            "connections": [
                {"source": "cpu_core", "target": "memory_controller", "bandwidth": 100},
                {"source": "cpu_core", "target": "ai_accelerator", "bandwidth": 200}
            ],
            "constraints": {
                "target_frequency": 2.0,
                "target_power": 5.0,
                "target_area": 50.0
            }
        }
        
        # Analyze architecture
        analysis_result = await analyzer.analyze_architecture("test_project_qa", mock_architecture)
        
        # Perform quality assurance
        qa_results = await qa.perform_quality_assurance("test_project_qa", analysis_result["analysis_data"])
        
        # Verify prediction results
        assert qa_results["status"] == "success"
        assert "quality_metrics" in qa_results
        
        print("Quality assurance predictions test completed successfully!")
    
    @pytest.mark.asyncio
    async def test_lifecycle_stage_transitions(self, lifecycle_tracker):
        """Test lifecycle stage transitions"""
        print("Testing lifecycle stage transitions...")
        
        # Create a new chip
        chip_id = "TEST_CHIP_001"
        
        # Register the chip
        await lifecycle_tracker.register_chip(chip_id, {
            "design_data": {"version": "1.0"}
        })
        
        # Transition through stages
        stages = [
            (ChipLifecycleStage.DESIGN, {"design_data": {"version": "1.0"}}),
            (ChipLifecycleStage.VERIFICATION, {"verification_results": {"passed": True}}),
            (ChipLifecycleStage.SYNTHESIS, {"synthesis_results": {"utilization": 0.75}}),
            (ChipLifecycleStage.PLACE_ROUTE, {"place_route_results": {"congestion": 0.2}}),
        ]
        
        for stage, data in stages:
            result = await lifecycle_tracker.update_lifecycle_stage(chip_id, stage, data)
            
            # Verify stage update
            assert result["status"] == "success"
            
            lifecycle_status = await lifecycle_tracker.get_lifecycle_status(chip_id)
            assert lifecycle_status["current_stage"] == stage.value
        
        print("Lifecycle stage transitions test completed successfully!")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
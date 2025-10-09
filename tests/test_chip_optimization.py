"""
Unit tests for the Chip Optimization Engine
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from src.chip_design.chip_optimization_engine import ChipOptimizationEngine, OptimizationType


@pytest.mark.asyncio
async def test_chip_optimization_engine_initialization():
    """Test that the ChipOptimizationEngine initializes correctly."""
    engine = ChipOptimizationEngine()
    assert engine is not None
    assert hasattr(engine, 'optimization_history')
    assert isinstance(engine.optimization_history, dict)


@pytest.mark.asyncio
async def test_placement_optimization_simulated_annealing():
    """Test placement optimization using simulated annealing algorithm."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data
    chip_data = {
        "components": [
            {"id": "cpu_core", "type": "core", "width": 100, "height": 100},
            {"id": "memory_controller", "type": "controller", "width": 50, "height": 50}
        ],
        "constraints": {
            "max_width": 1000,
            "max_height": 1000
        }
    }
    
    result = await engine.optimize_placement(chip_data, "simulated_annealing")
    
    assert result["status"] == "success"
    assert "data" in result
    assert "optimized_placement" in result["data"]
    assert len(result["data"]["optimized_placement"]) == len(chip_data["components"])


@pytest.mark.asyncio
async def test_placement_optimization_force_directed():
    """Test placement optimization using force-directed algorithm."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data
    chip_data = {
        "components": [
            {"id": "cpu_core", "type": "core", "width": 100, "height": 100},
            {"id": "memory_controller", "type": "controller", "width": 50, "height": 50}
        ],
        "constraints": {
            "max_width": 1000,
            "max_height": 1000
        }
    }
    
    result = await engine.optimize_placement(chip_data, "force_directed")
    
    assert result["status"] == "success"
    assert "data" in result
    assert "optimized_placement" in result["data"]
    assert len(result["data"]["optimized_placement"]) == len(chip_data["components"])


@pytest.mark.asyncio
async def test_routing_optimization_a_star():
    """Test routing optimization using A* algorithm."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data with placement
    chip_data = {
        "placement": [
            {"component_id": "cpu_core", "x": 100, "y": 100},
            {"component_id": "memory_controller", "x": 200, "y": 200}
        ],
        "connections": [
            {"id": "cpu_mem", "source": "cpu_core", "target": "memory_controller"}
        ]
    }
    
    result = await engine.optimize_routing(chip_data, "a_star")
    
    assert result["status"] == "success"
    assert "data" in result
    assert "routing_paths" in result["data"]
    assert len(result["data"]["routing_paths"]) == len(chip_data["connections"])


@pytest.mark.asyncio
async def test_routing_optimization_maze():
    """Test routing optimization using maze routing algorithm."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data with placement
    chip_data = {
        "placement": [
            {"component_id": "cpu_core", "x": 100, "y": 100},
            {"component_id": "memory_controller", "x": 200, "y": 200}
        ],
        "connections": [
            {"id": "cpu_mem", "source": "cpu_core", "target": "memory_controller"}
        ]
    }
    
    result = await engine.optimize_routing(chip_data, "maze_routing")
    
    assert result["status"] == "success"
    assert "data" in result
    assert "routing_paths" in result["data"]
    assert len(result["data"]["routing_paths"]) == len(chip_data["connections"])


@pytest.mark.asyncio
async def test_logic_synthesis_optimization():
    """Test logic synthesis optimization."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data with logic gates
    chip_data = {
        "logic_gates": [
            {"id": "gate1", "type": "AND"},
            {"id": "gate2", "type": "OR"}
        ]
    }
    
    result = await engine.optimize_logic_synthesis(chip_data, "technology_mapping")
    
    assert result["status"] == "success"
    assert "data" in result
    assert "mapped_gates" in result["data"]
    assert len(result["data"]["mapped_gates"]) == len(chip_data["logic_gates"])


@pytest.mark.asyncio
async def test_power_optimization():
    """Test power optimization."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data
    chip_data = {
        "components": [
            {"id": "cpu_core", "type": "core"},
            {"id": "memory_controller", "type": "controller"}
        ],
        "clocks": [
            {"id": "main_clock", "frequency": 1000}
        ]
    }
    
    result = await engine.optimize_power(chip_data)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "power_techniques" in result["data"]


@pytest.mark.asyncio
async def test_timing_optimization():
    """Test timing optimization."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data with timing paths
    chip_data = {
        "timing_paths": [
            {"id": "path1", "source": "cpu_core", "target": "memory_controller"},
            {"id": "path2", "source": "cpu_core", "target": "gpu_unit"}
        ],
        "timing_constraints": {
            "max_delay": 1.0
        }
    }
    
    result = await engine.optimize_timing(chip_data)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "optimized_paths" in result["data"]


@pytest.mark.asyncio
async def test_multi_objective_optimization():
    """Test multi-objective optimization."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data
    chip_data = {
        "components": [
            {"id": "cpu_core", "type": "core", "width": 100, "height": 100},
            {"id": "memory_controller", "type": "controller", "width": 50, "height": 50}
        ],
        "connections": [
            {"id": "cpu_mem", "source": "cpu_core", "target": "memory_controller"}
        ],
        "constraints": {
            "max_width": 1000,
            "max_height": 1000
        }
    }
    
    result = await engine.multi_objective_optimization(chip_data, ["placement", "routing"])
    
    assert result["status"] == "success"
    assert "results" in result
    assert "placement" in result["results"]
    assert "routing" in result["results"]


@pytest.mark.asyncio
async def test_benefit_estimation():
    """Test optimization benefit estimation."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data
    chip_data = {
        "components": [
            {"id": "cpu_core", "type": "core", "width": 100, "height": 100}
        ]
    }
    
    result = await engine.estimate_optimization_benefit(chip_data, OptimizationType.PLACEMENT)
    
    assert result["status"] == "success"
    assert "estimated_benefit" in result
    assert "estimated_wire_length_reduction" in result["estimated_benefit"]


@pytest.mark.asyncio
async def test_optimization_history():
    """Test optimization history tracking."""
    engine = ChipOptimizationEngine()
    
    # Sample chip data
    chip_data = {
        "components": [
            {"id": "cpu_core", "type": "core", "width": 100, "height": 100}
        ]
    }
    
    # Run an optimization
    await engine.optimize_placement(chip_data, "simulated_annealing")
    
    # Check history
    history = engine.get_optimization_history()
    assert history["status"] == "success"
    assert len(history["data"]) > 0


if __name__ == "__main__":
    pytest.main([__file__])
"""
Simple test script for the chip optimization engine
"""
import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.chip_design.chip_optimization_engine import ChipOptimizationEngine

async def test_optimization_engine():
    """Test the chip optimization engine."""
    print("Testing Chip Optimization Engine...")
    
    # Initialize the optimization engine
    engine = ChipOptimizationEngine()
    
    # Sample chip data
    chip_data = {
        "components": [
            {"id": "cpu_core", "type": "core", "width": 100, "height": 100},
            {"id": "memory_controller", "type": "controller", "width": 50, "height": 50},
            {"id": "gpu_unit", "type": "accelerator", "width": 80, "height": 80}
        ],
        "connections": [
            {"id": "cpu_mem", "source": "cpu_core", "target": "memory_controller"},
            {"id": "cpu_gpu", "source": "cpu_core", "target": "gpu_unit"}
        ],
        "constraints": {
            "max_width": 1000,
            "max_height": 1000,
            "power_limit": 5.0
        }
    }
    
    print("Testing placement optimization...")
    result = await engine.optimize_placement(chip_data, "simulated_annealing")
    print(f"Placement optimization result: {result['status']}")
    
    print("Testing routing optimization...")
    result = await engine.optimize_routing(chip_data, "a_star")
    print(f"Routing optimization result: {result['status']}")
    
    print("Testing logic synthesis optimization...")
    synthesis_data = {
        "logic_gates": [
            {"id": "gate1", "type": "AND"},
            {"id": "gate2", "type": "OR"},
            {"id": "gate3", "type": "NAND"}
        ]
    }
    result = await engine.optimize_logic_synthesis(synthesis_data, "technology_mapping")
    print(f"Logic synthesis optimization result: {result['status']}")
    
    print("Testing power optimization...")
    result = await engine.optimize_power(chip_data)
    print(f"Power optimization result: {result['status']}")
    
    print("Testing timing optimization...")
    timing_data = {
        "timing_paths": [
            {"id": "path1", "source": "cpu_core", "target": "memory_controller"},
            {"id": "path2", "source": "cpu_core", "target": "gpu_unit"}
        ],
        "timing_constraints": {
            "max_delay": 1.0
        }
    }
    result = await engine.optimize_timing(timing_data)
    print(f"Timing optimization result: {result['status']}")
    
    print("Testing multi-objective optimization...")
    result = await engine.multi_objective_optimization(chip_data, ["placement", "routing"])
    print(f"Multi-objective optimization result: {result['status']}")
    
    print("Testing benefit estimation...")
    from src.chip_design.chip_optimization_engine import OptimizationType
    result = await engine.estimate_optimization_benefit(chip_data, OptimizationType.PLACEMENT)
    print(f"Benefit estimation result: {result['status']}")
    
    print("All tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_optimization_engine())
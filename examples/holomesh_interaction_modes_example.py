"""
Example usage of HoloMesh Interaction Modes for CAD AI Optimization

This example demonstrates how to use the new semi-automatic and manual modes
with HoloMesh integration for professional and innovative tool interactions.
"""

import asyncio
import json
from src.ai.cad_ai_optimizer import init_cad_ai_optimizer, AIOptimizationStrategy, InteractionMode

async def demonstrate_holomesh_modes():
    """Demonstrate the new HoloMesh interaction modes."""
    
    # Initialize the AI optimizer
    optimizer = await init_cad_ai_optimizer()
    
    # Example 1: Semi-Automatic Mode
    print("=== Semi-Automatic Mode Example ===")
    
    # Define initial parameters for a Yosys optimization task
    initial_params_yosys = {
        "optimization_level": 2,
        "abc_optimization": True,
        "flatten_before_synthesis": True,
        "dfflibmap": True,
        "timing_analysis": True
    }
    
    # Define target metrics
    target_metrics_yosys = {
        "execution_time": 5.0,      # Target: 5 seconds
        "quality_score": 0.95,      # Target: 95% quality
        "resource_efficiency": 0.9  # Target: 90% efficiency
    }
    
    # Run optimization with semi-automatic mode
    result_semi_auto = await optimizer.optimize_cad_parameters(
        tool_name="yosys",
        project_id="project_holomesh_001",
        initial_params=initial_params_yosys,
        target_metrics=target_metrics_yosys,
        strategy=AIOptimizationStrategy.SEMI_AUTOMATIC,
        max_iterations=30,
        interaction_mode=InteractionMode.SEMI_AUTOMATIC,
        confidentiality_enabled=True
    )
    
    print("Semi-Automatic Mode Result:")
    print(json.dumps(result_semi_auto, indent=2))
    print()
    
    # Example 2: Manual Mode with Confidentiality
    print("=== Manual Mode with Confidentiality Example ===")
    
    # Define initial parameters for a NextPNR optimization task
    initial_params_nextpnr = {
        "placer": "heap",
        "router": "router1",
        "timing_driven": True,
        "seed": 42
    }
    
    # Define target metrics
    target_metrics_nextpnr = {
        "resource_efficiency": 0.85,  # Target: 85% efficiency
        "quality_score": 0.90         # Target: 90% quality
    }
    
    # Run optimization with manual mode and confidentiality enabled
    result_manual_conf = await optimizer.optimize_cad_parameters(
        tool_name="nextpnr",
        project_id="project_holomesh_002",
        initial_params=initial_params_nextpnr,
        target_metrics=target_metrics_nextpnr,
        strategy=AIOptimizationStrategy.MANUAL,
        max_iterations=25,
        interaction_mode=InteractionMode.MANUAL,
        confidentiality_enabled=True  # Designer's work remains private
    )
    
    print("Manual Mode with Confidentiality Result:")
    print(json.dumps(result_manual_conf, indent=2))
    print()
    
    # Example 3: Manual Mode without Confidentiality (for system learning)
    print("=== Manual Mode without Confidentiality Example ===")
    
    # Run optimization with manual mode and confidentiality disabled
    result_manual_learn = await optimizer.optimize_cad_parameters(
        tool_name="nextpnr",
        project_id="project_holomesh_003",
        initial_params=initial_params_nextpnr,
        target_metrics=target_metrics_nextpnr,
        strategy=AIOptimizationStrategy.MANUAL,
        max_iterations=25,
        interaction_mode=InteractionMode.MANUAL,
        confidentiality_enabled=False  # Enable system learning from this process
    )
    
    print("Manual Mode without Confidentiality Result:")
    print(json.dumps(result_manual_learn, indent=2))
    print()
    
    # Example 4: Professional Mode (default)
    print("=== Professional Mode Example ===")
    
    # Run optimization with professional mode
    result_professional = await optimizer.optimize_cad_parameters(
        tool_name="verilator",
        project_id="project_holomesh_004",
        initial_params={
            "optimization_level": 2,
            "language_extensions": "sv",
            "timing_analysis": True
        },
        target_metrics={
            "execution_time": 8.0,
            "quality_score": 0.92
        },
        strategy=AIOptimizationStrategy.BAYESIAN,
        max_iterations=20,
        interaction_mode=InteractionMode.PROFESSIONAL,
        confidentiality_enabled=True
    )
    
    print("Professional Mode Result:")
    print(json.dumps(result_professional, indent=2))
    print()
    
    # Example 5: Innovative Mode
    print("=== Innovative Mode Example ===")
    
    # Run optimization with innovative mode
    result_innovative = await optimizer.optimize_cad_parameters(
        tool_name="yosys",
        project_id="project_holomesh_005",
        initial_params=initial_params_yosys,
        target_metrics=target_metrics_yosys,
        strategy=AIOptimizationStrategy.BAYESIAN,
        max_iterations=35,
        interaction_mode=InteractionMode.INNOVATIVE,
        confidentiality_enabled=True
    )
    
    print("Innovative Mode Result:")
    print(json.dumps(result_innovative, indent=2))
    print()

async def demonstrate_project_database_updates():
    """Demonstrate how to update the project database with optimized configurations."""
    
    # Initialize the AI optimizer
    optimizer = await init_cad_ai_optimizer()
    
    # Add an optimized configuration to the project database for transfer learning
    project_data = {
        "project_id": "example_project_001",
        "tool_name": "yosys",
        "optimal_config": {
            "optimization_level": 3,
            "abc_optimization": True,
            "flatten_before_synthesis": True,
            "dfflibmap": True,
            "timing_analysis": True
        },
        "context": {
            "chip_type": "FPGA",
            "technology_node": "28nm",
            "application_domain": "digital_signal_processing"
        },
        "performance_metrics": {
            "execution_time": 4.2,
            "quality_score": 0.96,
            "resource_efficiency": 0.92
        },
        "chip_type": "FPGA",
        "technology_node": "28nm"
    }
    
    # Store in the optimizer's database
    optimizer.project_database[project_data["project_id"]] = project_data
    
    print("Added project to database for transfer learning:")
    print(json.dumps(project_data, indent=2))
    print()

async def demonstrate_recommendations():
    """Demonstrate how to get AI-driven recommendations."""
    
    # Initialize the AI optimizer
    optimizer = await init_cad_ai_optimizer()
    
    # Get recommendations for a new project
    project_context = {
        "chip_type": "ASIC",
        "technology_node": "7nm",
        "application_domain": "machine_learning",
        "power_constraints": "low_power",
        "performance_target": "high_performance"
    }
    
    recommendations = await optimizer.get_recommendations(
        tool_name="yosys",
        project_context=project_context
    )
    
    print("AI-Driven Recommendations:")
    print(json.dumps(recommendations, indent=2))
    print()

if __name__ == "__main__":
    print("HoloMesh Interaction Modes Example")
    print("==================================")
    print()
    
    # Run all examples
    asyncio.run(demonstrate_holomesh_modes())
    asyncio.run(demonstrate_project_database_updates())
    asyncio.run(demonstrate_recommendations())
    
    print("All examples completed successfully!")
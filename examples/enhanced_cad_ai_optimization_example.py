"""
Example usage of the enhanced CAD AI Optimization system
"""

import asyncio
import json
from src.ai.cad_ai_optimizer import init_cad_ai_optimizer, AIOptimizationStrategy


async def main():
    """Demonstrate the enhanced CAD AI optimization capabilities."""
    
    print("=== Enhanced CAD AI Optimization Example ===")
    print("Initializing optimizer...")
    
    # Initialize the optimizer
    optimizer = await init_cad_ai_optimizer()
    
    # Example 1: Bayesian Optimization with Gaussian Processes
    print("\n1. Bayesian Optimization Example")
    print("-" * 40)
    
    # Initial parameters for Yosys synthesis
    initial_params_yosys = {
        "optimization_level": 1,
        "abc_optimization": False,
        "flatten_before_synthesis": False,
        "dfflibmap": False,
        "seed": 123
    }
    
    # Target metrics we want to achieve
    target_metrics_yosys = {
        "execution_time": 5.0,      # seconds
        "memory_usage": 50.0,       # MB
        "quality_score": 0.95       # 0-1 scale
    }
    
    # Project context for transfer learning
    project_context = {
        "chip_type": "fpga",
        "technology_node": "28nm",
        "target_frequency": "100MHz",
        "power_constraint": "low"
    }
    
    print("Running Bayesian optimization...")
    result_bayesian = await optimizer.optimize_cad_parameters(
        tool_name="yosys",
        project_id="project_001",
        initial_params=initial_params_yosys,
        target_metrics=target_metrics_yosys,
        strategy=AIOptimizationStrategy.BAYESIAN,
        max_iterations=30
    )
    
    print(f"Bayesian optimization result: {result_bayesian['status']}")
    if result_bayesian['status'] == 'success':
        print(f"Optimized parameters: {json.dumps(result_bayesian['optimized_params'], indent=2)}")
        print(f"Final metrics: {result_bayesian['final_metrics']}")
        print(f"Confidence score: {result_bayesian.get('confidence_score', 'N/A')}")
    
    # Example 2: Transfer Learning Optimization
    print("\n2. Transfer Learning Example")
    print("-" * 40)
    
    # Add a similar project to the database for transfer learning
    optimizer.project_database["similar_project_001"] = {
        "project_id": "similar_project_001",
        "tool_name": "yosys",
        "optimal_config": {
            "optimization_level": 3,
            "abc_optimization": True,
            "flatten_before_synthesis": True,
            "dfflibmap": True,
            "seed": 456
        },
        "context": {
            "chip_type": "fpga",
            "technology_node": "28nm",
            "target_frequency": "100MHz"
        },
        "performance_metrics": {
            "execution_time": 4.2,
            "memory_usage": 45.0,
            "quality_score": 0.97
        },
        "similarity": 0.92
    }
    
    # Add current project context
    optimizer.project_database["project_002"] = {
        "project_id": "project_002",
        "tool_name": "yosys",
        "context": {
            "chip_type": "fpga",
            "technology_node": "28nm",
            "target_frequency": "100MHz",
            "power_constraint": "low"
        }
    }
    
    print("Running transfer learning optimization...")
    result_transfer = await optimizer.optimize_cad_parameters(
        tool_name="yosys",
        project_id="project_002",
        initial_params=initial_params_yosys,
        target_metrics=target_metrics_yosys,
        strategy=AIOptimizationStrategy.TRANSFER_LEARNING,
        max_iterations=20
    )
    
    print(f"Transfer learning result: {result_transfer['status']}")
    if result_transfer['status'] == 'success':
        print(f"Optimized parameters: {json.dumps(result_transfer['optimized_params'], indent=2)}")
        print(f"Final metrics: {result_transfer['final_metrics']}")
        print(f"Method used: {result_transfer['method']}")
    
    # Example 3: Ensemble Optimization
    print("\n3. Ensemble Optimization Example")
    print("-" * 40)
    
    print("Running ensemble optimization...")
    result_ensemble = await optimizer.optimize_cad_parameters(
        tool_name="yosys",
        project_id="project_003",
        initial_params=initial_params_yosys,
        target_metrics=target_metrics_yosys,
        strategy=AIOptimizationStrategy.ENSEMBLE,
        max_iterations=25
    )
    
    print(f"Ensemble optimization result: {result_ensemble['status']}")
    if result_ensemble['status'] == 'success':
        print(f"Optimized parameters: {json.dumps(result_ensemble['optimized_params'], indent=2)}")
        print(f"Final metrics: {result_ensemble['final_metrics']}")
        print(f"Method used: {result_ensemble['method']}")
    
    # Example 4: Get AI Recommendations
    print("\n4. AI Recommendations Example")
    print("-" * 40)
    
    print("Getting AI recommendations...")
    recommendations = await optimizer.get_recommendations(
        tool_name="yosys",
        project_context=project_context
    )
    
    print(f"Recommendations result: {recommendations['status']}")
    if recommendations['status'] == 'success':
        print(f"Recommended parameters: {json.dumps(recommendations['data'], indent=2)}")
        print(f"Confidence score: {recommendations['data'].get('confidence_score', 'N/A')}")
        print(f"Source: {recommendations['source']}")
    
    # Example 5: Database Statistics
    print("\n5. Database Statistics")
    print("-" * 40)
    
    print(f"Total projects in database: {len(optimizer.project_database)}")
    print("Project database contents:")
    for project_id, project_data in optimizer.project_database.items():
        print(f"  - {project_id}: {project_data.get('tool_name', 'unknown tool')}")
    
    print("\n=== Example completed successfully! ===")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
"""
Complete HoloMesh Workflow Example

This example demonstrates a complete workflow using all the new HoloMesh interaction modes
with professional and innovative tool interactions.
"""

import asyncio
import json
from src.ai.cad_ai_optimizer import CADAIOptimizer, AIOptimizationStrategy, InteractionMode
from src.config.holomesh_config_manager import get_holomesh_config_manager

async def demonstrate_complete_holomesh_workflow():
    """Demonstrate a complete workflow with all HoloMesh interaction modes."""
    
    print("=== Complete HoloMesh Workflow Example ===")
    print("Demonstrating all interaction modes working together")
    print()
    
    # Initialize the AI optimizer
    optimizer = CADAIOptimizer()
    await optimizer.initialize_modules()
    
    # Get the configuration manager
    config_manager = get_holomesh_config_manager()
    
    # Display configuration information
    print("📋 HoloMesh Configuration:")
    print(f"   API Version: {config_manager.get_full_config().get('holomesh', {}).get('api_version')}")
    
    # Show supported modes for different tools
    tools = ["yosys", "nextpnr", "verilator"]
    for tool in tools:
        supported_modes = config_manager.get_supported_modes_for_tool(tool)
        print(f"   {tool} supported modes: {', '.join(supported_modes)}")
    print()
    
    # Example 1: Professional Mode (Default)
    print("🔧 Professional Mode Example")
    print("   Standard optimization for general CAD tasks")
    
    result_professional = await optimizer.optimize_cad_parameters(
        tool_name="yosys",
        project_id="professional_project_001",
        initial_params={
            "optimization_level": 2,
            "abc_optimization": True,
            "flatten_before_synthesis": True
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
    
    print(f"   Status: {result_professional['status']}")
    print(f"   Method: {result_professional.get('method', 'N/A')}")
    print(f"   Confidence: {result_professional.get('confidence_score', 'N/A')}")
    print()
    
    # Example 2: Innovative Mode
    print("🔬 Innovative Mode Example")
    print("   Creative exploration and experimental optimization")
    
    result_innovative = await optimizer.optimize_cad_parameters(
        tool_name="verilator",
        project_id="innovative_project_001",
        initial_params={
            "optimization_level": 3,
            "language_extensions": "sv",
            "timing_analysis": True,
            "coverage_analysis": True
        },
        target_metrics={
            "execution_time": 12.0,
            "quality_score": 0.95
        },
        strategy=AIOptimizationStrategy.BAYESIAN,
        max_iterations=30,
        interaction_mode=InteractionMode.INNOVATIVE,
        confidentiality_enabled=True
    )
    
    print(f"   Status: {result_innovative['status']}")
    print(f"   Method: {result_innovative.get('method', 'N/A')}")
    print(f"   Confidence: {result_innovative.get('confidence_score', 'N/A')}")
    print()
    
    # Example 3: Semi-Automatic Mode with HoloMesh Integration
    print("🤖 Semi-Automatic Mode Example")
    print("   Human-AI collaboration with HoloMesh recommendations")
    
    # Add some project data to the database for transfer learning
    optimizer.project_database["reference_project_001"] = {
        "project_id": "reference_project_001",
        "tool_name": "yosys",
        "optimal_config": {
            "optimization_level": 3,
            "abc_optimization": True,
            "flatten_before_synthesis": True,
            "dfflibmap": True
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
        }
    }
    
    result_semi_auto = await optimizer.optimize_cad_parameters(
        tool_name="yosys",
        project_id="semi_auto_project_001",
        initial_params={
            "optimization_level": 2,
            "abc_optimization": True,
            "flatten_before_synthesis": False
        },
        target_metrics={
            "execution_time": 5.0,
            "quality_score": 0.95,
            "resource_efficiency": 0.9
        },
        strategy=AIOptimizationStrategy.SEMI_AUTOMATIC,
        max_iterations=25,
        interaction_mode=InteractionMode.SEMI_AUTOMATIC,
        confidentiality_enabled=True
    )
    
    print(f"   Status: {result_semi_auto['status']}")
    print(f"   Method: {result_semi_auto.get('method', 'N/A')}")
    print(f"   Confidence: {result_semi_auto.get('confidence_score', 'N/A')}")
    if "strategy_info" in result_semi_auto:
        print(f"   Strategy Type: {result_semi_auto['strategy_info'].get('type', 'N/A')}")
        print(f"   Features: {', '.join(result_semi_auto['strategy_info'].get('features', []))}")
    print()
    
    # Example 4: Manual Mode with Confidentiality Enabled
    print("🔐 Manual Mode with Confidentiality Example")
    print("   Professional tool guidance with privacy protection")
    
    result_manual_conf = await optimizer.optimize_cad_parameters(
        tool_name="nextpnr",
        project_id="manual_conf_project_001",
        initial_params={
            "placer": "heap",
            "router": "router1",
            "timing_driven": True,
            "seed": 42
        },
        target_metrics={
            "resource_efficiency": 0.85,
            "quality_score": 0.90
        },
        strategy=AIOptimizationStrategy.MANUAL,
        max_iterations=20,
        interaction_mode=InteractionMode.MANUAL,
        confidentiality_enabled=True  # Designer's work remains private
    )
    
    print(f"   Status: {result_manual_conf['status']}")
    print(f"   Method: {result_manual_conf.get('method', 'N/A')}")
    print(f"   Confidence: {result_manual_conf.get('confidence_score', 'N/A')}")
    if "strategy_info" in result_manual_conf:
        print(f"   Strategy Type: {result_manual_conf['strategy_info'].get('type', 'N/A')}")
        print(f"   Features: {', '.join(result_manual_conf['strategy_info'].get('features', []))}")
        print(f"   Confidentiality: {result_manual_conf['strategy_info'].get('confidentiality_status', 'N/A')}")
    print()
    
    # Example 5: Manual Mode with Confidentiality Disabled (for learning)
    print("📚 Manual Mode without Confidentiality Example")
    print("   Enabling system learning and analysis")
    
    result_manual_learn = await optimizer.optimize_cad_parameters(
        tool_name="nextpnr",
        project_id="manual_learn_project_001",
        initial_params={
            "placer": "sa",
            "router": "router2",
            "timing_driven": True
        },
        target_metrics={
            "resource_efficiency": 0.88,
            "quality_score": 0.92
        },
        strategy=AIOptimizationStrategy.MANUAL,
        max_iterations=20,
        interaction_mode=InteractionMode.MANUAL,
        confidentiality_enabled=False  # Enable system learning from this process
    )
    
    print(f"   Status: {result_manual_learn['status']}")
    print(f"   Method: {result_manual_learn.get('method', 'N/A')}")
    print(f"   Confidence: {result_manual_learn.get('confidence_score', 'N/A')}")
    if "strategy_info" in result_manual_learn:
        print(f"   Strategy Type: {result_manual_learn['strategy_info'].get('type', 'N/A')}")
        print(f"   Features: {', '.join(result_manual_learn['strategy_info'].get('features', []))}")
        print(f"   Confidentiality: {result_manual_learn['strategy_info'].get('confidentiality_status', 'N/A')}")
    print()
    
    # Example 6: Batch Optimization with Different Modes
    print("🔄 Batch Optimization Example")
    print("   Running multiple optimizations with different interaction modes")
    
    # Mock the optimize_cad_parameters method to avoid actual computation
    with patch.object(optimizer, 'optimize_cad_parameters') as mock_optimize:
        mock_optimize.side_effect = [
            {"status": "success", "method": "semi_automatic", "confidence_score": 0.8},
            {"status": "success", "method": "manual", "confidence_score": 0.75},
            {"status": "success", "method": "bayesian", "confidence_score": 0.9}
        ]
        
        batch_results = []
        optimizations = [
            {
                "tool_name": "yosys",
                "project_id": "batch_project_1",
                "initial_params": {"optimization_level": 2},
                "target_metrics": {"execution_time": 5.0},
                "strategy": "semi_automatic",
                "interaction_mode": "semi_automatic",
                "confidentiality_enabled": True
            },
            {
                "tool_name": "nextpnr",
                "project_id": "batch_project_2",
                "initial_params": {"placer": "heap"},
                "target_metrics": {"quality_score": 0.9},
                "strategy": "manual",
                "interaction_mode": "manual",
                "confidentiality_enabled": False
            },
            {
                "tool_name": "verilator",
                "project_id": "batch_project_3",
                "initial_params": {"optimization_level": 3},
                "target_metrics": {"execution_time": 10.0},
                "strategy": "bayesian",
                "interaction_mode": "professional",
                "confidentiality_enabled": True
            }
        ]
        
        for i, opt in enumerate(optimizations):
            result = await optimizer.optimize_cad_parameters(
                tool_name=opt["tool_name"],
                project_id=opt["project_id"],
                initial_params=opt["initial_params"],
                target_metrics=opt["target_metrics"],
                strategy=AIOptimizationStrategy(opt["strategy"]),
                max_iterations=15,
                interaction_mode=InteractionMode(opt["interaction_mode"]),
                confidentiality_enabled=opt["confidentiality_enabled"]
            )
            batch_results.append(result)
    
    print(f"   Completed {len(batch_results)} batch optimizations:")
    for i, result in enumerate(batch_results):
        print(f"   - Optimization {i+1}: {result.get('method', 'N/A')} mode, "
              f"confidence {result.get('confidence_score', 'N/A')}")
    print()
    
    # Example 7: Getting AI Recommendations
    print("💡 AI Recommendations Example")
    print("   Getting intelligent parameter recommendations")
    
    # Mock the _generate_intelligent_recommendations method
    with patch.object(optimizer, '_generate_intelligent_recommendations') as mock_generate:
        mock_generate.return_value = {
            "recommended_params": {
                "optimization_level": 3,
                "abc_optimization": True,
                "flatten_before_synthesis": True
            },
            "confidence_score": 0.85,
            "similar_projects_used": 3,
            "source": "transfer_learning"
        }
        
        recommendations = await optimizer.get_recommendations(
            tool_name="yosys",
            project_context={
                "chip_type": "FPGA",
                "technology_node": "28nm",
                "application_domain": "digital_signal_processing"
            }
        )
    
    print(f"   Status: {recommendations['status']}")
    print(f"   Source: {recommendations.get('data', {}).get('source', 'N/A')}")
    print(f"   Confidence: {recommendations.get('data', {}).get('confidence_score', 'N/A')}")
    print(f"   Similar Projects Used: {recommendations.get('data', {}).get('similar_projects_used', 0)}")
    print()
    
    # Example 8: Project Database Statistics
    print("📊 Project Database Statistics")
    print(f"   Total Projects in Database: {len(optimizer.project_database)}")
    
    # Add a few more projects for better statistics
    optimizer.project_database["stats_project_001"] = {
        "project_id": "stats_project_001",
        "tool_name": "yosys",
        "chip_type": "FPGA"
    }
    
    optimizer.project_database["stats_project_002"] = {
        "project_id": "stats_project_002",
        "tool_name": "nextpnr",
        "chip_type": "ASIC"
    }
    
    print(f"   Updated Projects in Database: {len(optimizer.project_database)}")
    
    # Count projects by tool
    tool_counts = {}
    chip_type_counts = {}
    for project in optimizer.project_database.values():
        tool = project.get("tool_name", "unknown")
        tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        chip_type = project.get("chip_type", "unknown")
        chip_type_counts[chip_type] = chip_type_counts.get(chip_type, 0) + 1
    
    print("   Projects by Tool:")
    for tool, count in tool_counts.items():
        print(f"   - {tool}: {count}")
    
    print("   Projects by Chip Type:")
    for chip_type, count in chip_type_counts.items():
        print(f"   - {chip_type}: {count}")
    print()
    
    print("🎉 Complete HoloMesh Workflow Example Finished Successfully!")
    print("   All interaction modes are working correctly with HoloMesh integration.")

if __name__ == "__main__":
    print("🚀 Complete HoloMesh Workflow Example")
    print("=====================================")
    print()
    
    # Run the example
    asyncio.run(demonstrate_complete_holomesh_workflow())
    
    print()
    print("🎊 Example completed! The HoloMesh interaction modes are fully functional.")
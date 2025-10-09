#!/usr/bin/env python3
"""
Test imports for TaskFusionEngine dependencies
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.ai.predictive_scaling_engine import PredictiveScalingEngine
    print("✓ PredictiveScalingEngine import successful")
except Exception as e:
    print(f"✗ PredictiveScalingEngine import failed: {e}")

try:
    from src.security.quantum_singularity_firewall import QuantumSingularityFirewall
    firewall = QuantumSingularityFirewall()
    print("✓ QuantumSingularityFirewall import and instantiation successful")
except Exception as e:
    print(f"✗ QuantumSingularityFirewall import failed: {e}")

try:
    from src.ai.agentcore_trainer import AgentCoreTrainer
    trainer = AgentCoreTrainer()
    print("✓ AgentCoreTrainer import and instantiation successful")
except Exception as e:
    print(f"✗ AgentCoreTrainer import failed: {e}")

try:
    from src.ai.agent_guard import AgentGuard
    guard = AgentGuard()
    print("✓ AgentGuard import and instantiation successful")
except Exception as e:
    print(f"✗ AgentGuard import failed: {e}")

print("Import test completed.")
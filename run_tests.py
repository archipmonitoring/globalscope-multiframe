#!/usr/bin/env python3
"""
Test runner script for GlobalScope MultiFrame 11.0
This script runs all tests and generates reports.
"""
import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ FAILED")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Main test runner function"""
    print("GlobalScope MultiFrame 11.0 - Comprehensive Test Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Test categories
    test_categories = [
        {
            "name": "Unit Tests",
            "command": "python -m pytest tests/test_optimized_redis_client.py tests/test_enhanced_firewall.py tests/test_error_handler.py tests/test_extended_monitor.py -v",
            "description": "Unit tests for all new modules"
        },
        {
            "name": "Integration Tests",
            "command": "python -m pytest tests/test_redis_integration.py tests/test_security_integration.py tests/test_reliability_integration.py tests/test_monitoring_integration.py -v",
            "description": "Integration tests for module interactions"
        },
        {
            "name": "Chip Design Integration Tests",
            "command": "python -m pytest tests/test_chip_design_integration.py -v",
            "description": "Integration tests for chip design components"
        },
        {
            "name": "Performance Tests",
            "command": "python -m pytest tests/test_redis_performance.py tests/test_security_performance.py tests/test_reliability_performance.py tests/test_monitoring_performance.py -v",
            "description": "Performance tests for all modules"
        },
        {
            "name": "Regression Tests",
            "command": "python -m pytest tests/test_regression.py -v",
            "description": "Regression tests for backward compatibility"
        },
        {
            "name": "All Tests",
            "command": "python -m pytest tests/ -v",
            "description": "All tests combined"
        }
    ]
    
    # Run each test category
    results = []
    for category in test_categories:
        success = run_command(category["command"], category["description"])
        results.append({
            "name": category["name"],
            "success": success
        })
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["success"])
    failed_tests = total_tests - passed_tests
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status} {result['name']}")
    
    print(f"\nTotal: {total_tests} | Passed: {passed_tests} | Failed: {failed_tests}")
    
    if failed_tests == 0:
        print("\n🎉 All tests passed! The system is ready for production.")
        return 0
    else:
        print(f"\n❌ {failed_tests} test category(s) failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
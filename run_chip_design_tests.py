#!/usr/bin/env python3
"""
Test runner for chip design integration tests
"""
import subprocess
import sys
import os

def run_test():
    """Run the chip design integration test"""
    print("Running Chip Design Integration Tests...")
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Run the specific test
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_chip_design_integration.py", 
            "-v"
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running test: {e}")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
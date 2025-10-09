#!/usr/bin/env python3
"""
Verification script for CAD tools installation
This script checks that all required CAD tools are properly installed and accessible.
"""

import subprocess
import sys
import os

def check_tool_version(tool_name, version_command):
    """Check if a tool is installed and get its version."""
    try:
        result = subprocess.run(version_command, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ {tool_name}: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {tool_name}: Failed to get version (exit code {result.returncode})")
            print(f"  Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {tool_name}: Command timed out")
        return False
    except Exception as e:
        print(f"✗ {tool_name}: {str(e)}")
        return False

def check_directory_permissions(path):
    """Check if a directory exists and is writable."""
    try:
        if not os.path.exists(path):
            print(f"Creating directory: {path}")
            os.makedirs(path, exist_ok=True)
        
        if os.access(path, os.W_OK):
            print(f"✓ Directory {path}: Writable")
            return True
        else:
            print(f"✗ Directory {path}: Not writable")
            return False
    except Exception as e:
        print(f"✗ Directory {path}: {str(e)}")
        return False

def main():
    """Main verification function."""
    print("Verifying CAD tools installation...\n")
    
    # Check CAD tools
    tools = [
        ("Verilator", "verilator --version"),
        ("Yosys", "yosys -V"),
        ("NextPNR", "nextpnr-generic --version"),
        ("Icarus Verilog", "iverilog -V"),
        ("GTKWave", "gtkwave --version")
    ]
    
    all_tools_ok = True
    for tool_name, version_command in tools:
        if not check_tool_version(tool_name, version_command):
            all_tools_ok = False
    
    print("\nVerifying directory permissions...\n")
    
    # Check directories
    directories = [
        "/app/projects",
        "/app/chip_designs"
    ]
    
    all_dirs_ok = True
    for directory in directories:
        if not check_directory_permissions(directory):
            all_dirs_ok = False
    
    print("\n" + "="*50)
    if all_tools_ok and all_dirs_ok:
        print("✓ All CAD tools and directories are properly configured!")
        return 0
    else:
        print("✗ Some issues were detected with the CAD tools installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
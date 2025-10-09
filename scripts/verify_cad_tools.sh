#!/bin/bash
#
# Verification script for CAD tools installation
# This script checks that all required CAD tools are properly installed and accessible.

echo "Verifying CAD tools installation..."
echo "==================================="

# Function to check tool version
check_tool() {
    local tool_name=$1
    local version_cmd=$2
    
    echo -n "Checking $tool_name... "
    if command -v "$tool_name" >/dev/null 2>&1; then
        version_output=$($version_cmd 2>&1)
        if [ $? -eq 0 ]; then
            echo "✓ Installed ($version_output)"
        else
            echo "✗ Installed but version check failed"
        fi
    else
        echo "✗ Not found"
    fi
}

# Check CAD tools
check_tool "verilator" "verilator --version"
check_tool "yosys" "yosys -V"
check_tool "nextpnr-generic" "nextpnr-generic --version"
check_tool "iverilog" "iverilog -V"
check_tool "gtkwave" "gtkwave --version"

echo ""
echo "Verifying directory permissions..."
echo "=================================="

# Check directories
for dir in "/app/projects" "/app/chip_designs"; do
    echo -n "Checking $dir... "
    if [ -d "$dir" ]; then
        if [ -w "$dir" ]; then
            echo "✓ Exists and writable"
        else
            echo "✗ Exists but not writable"
        fi
    else
        echo "✗ Does not exist"
    fi
done

echo ""
echo "Verification complete."
#!/bin/bash

# Demo Data Initialization Script for GlobalScope MultiFrame 11.0
# This script initializes Redis with demo data

echo "Initializing demo data for GlobalScope MultiFrame 11.0..."
echo "======================================================"

# Check if Redis is running
if ! command -v redis-cli &> /dev/null
then
    echo "Redis CLI could not be found. Please install Redis."
    exit 1
fi

# Check if Redis server is accessible
if redis-cli ping &> /dev/null
then
    echo "Redis server is running."
else
    echo "Redis server is not accessible. Please start Redis server."
    exit 1
fi

# Run the Python script to initialize demo data
echo "Running demo data initialization script..."
python init_demo_data.py

echo "======================================================"
echo "Demo data initialization completed!"
echo "Use 'python verify_demo_data.py' to verify the data."
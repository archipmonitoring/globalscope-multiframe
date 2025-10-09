@echo off
title Demo Data Initialization - GlobalScope MultiFrame 11.0

echo Initializing demo data for GlobalScope MultiFrame 11.0...
echo ======================================================

REM Check if Redis is running
redis-cli ping >nul 2>&1
if %errorlevel% neq 0 (
    echo Redis server is not accessible. Please start Redis server.
    pause
    exit /b 1
) else (
    echo Redis server is running.
)

REM Run the Python script to initialize demo data
echo Running demo data initialization script...
python init_demo_data.py

echo ======================================================
echo Demo data initialization completed!
echo Use 'python verify_demo_data.py' to verify the data.
pause
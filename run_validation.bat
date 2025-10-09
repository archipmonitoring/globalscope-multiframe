@echo off
title GlobalScope MultiFrame Enhanced Validation

echo 🚀 GlobalScope MultiFrame Enhanced Validation
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Python is not installed.
    pause
    exit /b 1
)

echo ✓ Python is installed

REM Run enhanced validation
echo.
echo 🔍 Running enhanced validation...
python run_enhanced_validation.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Enhanced validation completed successfully!
    exit /b 0
) else (
    echo.
    echo ❌ Enhanced validation failed. Please check the output above.
    exit /b 1
)

pause
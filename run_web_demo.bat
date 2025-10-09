@echo off
TITLE HoloMesh Web Demo Launcher
ECHO ======================================
ECHO HoloMesh Web Demo Launcher
ECHO ======================================

ECHO Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    ECHO ERROR: Python is not installed or not in PATH
    ECHO Please install Python 3.7+ and try again
    pause
    exit /b 1
)

ECHO Checking Flask installation...
pip show flask >nul 2>&1
if errorlevel 1 (
    ECHO Flask not found. Installing Flask...
    pip install flask
    if errorlevel 1 (
        ECHO ERROR: Failed to install Flask
        pause
        exit /b 1
    )
)

ECHO.
ECHO ======================================
ECHO Starting HoloMesh Web Demo Server
ECHO ======================================
ECHO Server will be available at: http://localhost:5000
ECHO Press CTRL+C to stop the server
ECHO ======================================
ECHO.

cd /d "e:\papka_fail\MG\GlobalScope MultiFrame-13\web_demo"

python app.py

pause
@echo off
echo HoloMesh Marketplace Complete Setup
echo =================================
echo This script will run the complete setup process for the HoloMesh Marketplace system.
echo.

echo Step 1: Installing database dependencies...
python install_db_deps.py
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully
echo.

echo Step 2: Initializing database...
python init_database.py
if %errorlevel% neq 0 (
    echo ❌ Failed to initialize database
    pause
    exit /b 1
)
echo ✅ Database initialized successfully
echo.

echo Step 3: Verifying database models...
python verify_models.py
if %errorlevel% neq 0 (
    echo ❌ Failed to verify models
    pause
    exit /b 1
)
echo ✅ Models verified successfully
echo.

echo Step 4: Running database tests...
python test_database.py
if %errorlevel% neq 0 (
    echo ❌ Database tests failed
    pause
    exit /b 1
)
echo ✅ Database tests passed successfully
echo.

echo =================================
echo 🎉 Complete Setup Successful!
echo =================================
echo.
echo Next steps:
echo 1. Configure your PostgreSQL connection in src/db/database.py
echo 2. Start the web demo: cd web_demo && python app.py
echo 3. Visit http://localhost:5000 in your browser
echo.
echo Documentation:
echo - DATABASE_INTEGRATION_SUMMARY.md
echo - HOLOMESH_MARKETPLACE_ROADMAP.md
echo - IMPLEMENTATION_SUMMARY.md
echo - ALL_REQUIREMENTS_IMPLEMENTED.md
echo.
echo For detailed instructions, run: python setup_holomesh.py
echo.
pause
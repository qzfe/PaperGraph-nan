@echo off
echo ====================================
echo PaperGraph Server Starter
echo ====================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Cannot find virtual environment£¬please run setup.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

echo.
echo Activating FastAPI server...
echo Visit http://localhost:8000/docs to check API document
echo.
echo Press Ctrl+C to stop server
echo.

python -m app.main

pause
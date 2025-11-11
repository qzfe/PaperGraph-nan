@echo off
echo ====================================
echo PaperGraph Celery Worker Starter
echo ====================================
echo.

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Cannot find virtual environment, please run setup.bat first
    pause
    exit /b 1
)

echo.
echo Activating Celery Worker...
echo.
echo Press Ctrl+C to stop Worker
echo.

celery -A app.tasks.celery_app worker --loglevel=info --pool=solo

pause
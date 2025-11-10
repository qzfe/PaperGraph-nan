@echo off
echo ====================================
echo 论文知识图谱系统 - 启动 Celery Worker
echo ====================================
echo.

REM 激活虚拟环境
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] 虚拟环境已激活
) else (
    echo [ERROR] 找不到虚拟环境，请先运行 setup.bat
    pause
    exit /b 1
)

REM 启动 Celery Worker
echo.
echo 正在启动 Celery Worker...
echo.
echo 按 Ctrl+C 停止 Worker
echo.

celery -A app.tasks.celery_app worker --loglevel=info --pool=solo

pause


@echo off
echo ====================================
echo 论文知识图谱系统 - 启动服务器
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

REM 启动服务器
echo.
echo 正在启动 FastAPI 服务器...
echo 访问 http://localhost:8000/docs 查看 API 文档
echo.
echo 按 Ctrl+C 停止服务器
echo.

python app/main.py

pause


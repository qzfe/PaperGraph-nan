@echo off
chcp 65001 >nul
echo ====================================
echo 论文知识图谱系统 - 环境设置
echo ====================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)
echo [OK] Python 已安装

REM 创建虚拟环境
if not exist venv (
    echo.
    echo 正在创建虚拟环境...
    python -m venv venv
    echo [OK] 虚拟环境创建成功
) else (
    echo [OK] 虚拟环境已存在
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 升级 pip
echo.
echo 正在升级 pip...
python -m pip install --upgrade pip

REM 安装依赖
echo.
echo 正在安装依赖包...
pip install -r requirements.txt

REM 创建必要目录
if not exist logs mkdir logs
if not exist exports mkdir exports
echo [OK] 目录结构创建完成

REM 检查 .env 文件
if not exist .env (
    echo.
    echo [警告] 未找到 .env 文件
    echo 请手动创建 .env 文件并配置数据库连接信息
    echo 参考 README.md 中的配置说明
    echo.
)

echo.
echo ====================================
echo 环境设置完成！
echo ====================================
echo.
echo 下一步：
echo 1. 配置 .env 文件
echo 2. 运行 python scripts/init_database.py 初始化数据库
echo 3. 运行 python scripts/load_sample_data.py 加载示例数据
echo 4. 运行 start_server.bat 启动服务器
echo.
pause


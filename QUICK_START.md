# 快速开始指南 / Quick Start Guide

## 🎯 5分钟快速启动 / 5-Minute Quick Start

### 前提条件 / Prerequisites

✓ Python 3.9+ 已安装 (当前: 3.10.5)  
⚠ MySQL 8.0+ 需要安装  
⚠ Neo4j Desktop 需要安装  
⚠ Redis/Memurai 需要安装  

---

## Windows 用户 / Windows Users

### 1️⃣ 安装依赖环境

下载并安装（如未安装）/ Download and install (if not installed):

1. MySQL: https://dev.mysql.com/downloads/installer/
2. Neo4j Desktop: https://neo4j.com/download/
3. Memurai (Redis for Windows): https://www.memurai.com/get-memurai

### 2️⃣ 一键配置环境

```cmd
setup.bat
```

这个脚本会自动完成 / This script will automatically:
- ✓ 创建虚拟环境
- ✓ 安装所有 Python 依赖
- ✓ 创建必要的目录

### 3️⃣ 配置数据库密码

```cmd
# 1. 复制配置文件
copy .env.example .env

# 2. 用记事本编辑 .env
notepad .env

# 3. 修改以下两行：
MYSQL_PASSWORD=你的MySQL密码
NEO4J_PASSWORD=你的Neo4j密码
```

### 4️⃣ 创建 MySQL 数据库

打开 MySQL 命令行 / Open MySQL Command Line:

```sql
CREATE DATABASE paper_kg CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 5️⃣ 启动 Neo4j

1. 打开 Neo4j Desktop
2. 创建一个新项目
3. 添加一个数据库
4. 点击 "Start" 启动数据库
5. 设置密码（与 .env 中的密码一致）

### 6️⃣ 初始化数据库

```cmd
venv\Scripts\activate
python scripts\init_database.py
python scripts\load_sample_data.py
```

### 7️⃣ 启动服务

打开两个命令行窗口 / Open two command line windows:

**窗口 1: 启动主服务**
```cmd
start_server.bat
```

**窗口 2: 启动 Celery（可选）**
```cmd
start_celery.bat
```

### 8️⃣ 访问系统

在浏览器中打开 / Open in browser:

http://localhost:8000/docs

🎉 完成！/ Done!

---

## Linux/Mac 用户 / Linux/Mac Users

### 1️⃣ 安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-venv mysql-server redis-server

# macOS
brew install python mysql redis
```

### 2️⃣ 安装 Neo4j Desktop

从 https://neo4j.com/download/ 下载并安装

### 3️⃣ 设置项目

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建目录
mkdir -p logs exports
```

### 4️⃣ 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置
nano .env  # 或使用你喜欢的编辑器

# 修改密码
MYSQL_PASSWORD=你的MySQL密码
NEO4J_PASSWORD=你的Neo4j密码
```

### 5️⃣ 创建数据库

```bash
# MySQL
mysql -u root -p
```

```sql
CREATE DATABASE paper_kg CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 6️⃣ 启动服务

```bash
# 启动 MySQL
sudo systemctl start mysql  # Linux
# brew services start mysql  # macOS

# 启动 Redis
sudo systemctl start redis  # Linux
# brew services start redis  # macOS

# 启动 Neo4j Desktop 中的数据库
```

### 7️⃣ 初始化数据库

```bash
source venv/bin/activate
python scripts/init_database.py
python scripts/load_sample_data.py
```

### 8️⃣ 启动应用

```bash
# 终端 1: 主服务
source venv/bin/activate
python app/main.py

# 终端 2: Celery Worker
source venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info
```

### 9️⃣ 访问系统

http://localhost:8000/docs

---

## 🧪 测试 API / Test the API

### 1. 健康检查 / Health Check

```bash
curl http://localhost:8000/health
```

应该返回 / Should return:
```json
{"status": "healthy"}
```

### 2. 获取根节点图谱 / Get Root Graph

```bash
curl http://localhost:8000/api/v1/graph/root?limit=10
```

### 3. 查询统计数据 / Query Statistics

```bash
curl -X POST http://localhost:8000/api/v1/statistics/query -H "Content-Type: application/json" -d "{\"metric\": \"top_authors\", \"limit\": 5}"
```

### 4. 访问 API 文档 / Visit API Docs

在浏览器打开 / Open in browser:

http://localhost:8000/docs

这里有完整的交互式 API 文档！/ Full interactive API documentation here!

---

## ⚠️ 常见错误及解决 / Common Errors & Solutions

### 错误 1: `ModuleNotFoundError: No module named 'fastapi'`

**原因**: 依赖未安装  
**解决**: 
```bash
pip install -r requirements.txt
```

### 错误 2: MySQL 连接失败

**原因**: MySQL 服务未启动或密码错误  
**解决**:
```bash
# Windows
net start MySQL

# Linux
sudo systemctl start mysql
```
检查 `.env` 文件中的密码是否正确

### 错误 3: Neo4j 连接失败

**原因**: Neo4j 数据库未启动  
**解决**: 
1. 打开 Neo4j Desktop
2. 确认数据库状态为 "Active"
3. 检查 `.env` 中的密码

### 错误 4: Redis 连接失败

**原因**: Redis 服务未启动  
**解决**:
```bash
# Windows
net start Memurai

# Linux
sudo systemctl start redis
```

### 错误 5: 端口 8000 被占用

**原因**: 其他程序占用端口  
**解决**:
```bash
# Windows - 查找并结束进程
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# Linux - 查找并结束进程
lsof -i :8000
kill -9 <进程ID>
```

---

## 📖 API 端点快速参考 / API Endpoints Quick Reference

| 功能 / Feature | 方法 / Method | 端点 / Endpoint | 说明 / Description |
|---------------|--------------|----------------|-------------------|
| 根节点图谱 | GET | `/api/v1/graph/root` | 获取知识图谱根节点 |
| 展开节点 | GET | `/api/v1/graph/children/{node_id}` | 获取子节点 |
| 节点详情 | GET | `/api/v1/graph/node/{node_id}` | 查看节点信息 |
| 保存布局 | POST | `/api/v1/graph/layout/persist` | 保存节点位置 |
| 查询统计 | POST | `/api/v1/statistics/query` | 获取统计数据 |
| 清除缓存 | DELETE | `/api/v1/statistics/cache` | 清除统计缓存 |
| 创建导出 | POST | `/api/v1/export/file` | 创建导出任务 |
| 任务状态 | GET | `/api/v1/export/job/{job_id}` | 查询导出状态 |
| 下载文件 | GET | `/api/v1/export/download/{job_id}` | 下载导出文件 |

---

## 🎓 学习资源 / Learning Resources

- **FastAPI 官方文档**: https://fastapi.tiangolo.com/
- **Neo4j 文档**: https://neo4j.com/docs/
- **SQLAlchemy 文档**: https://docs.sqlalchemy.org/
- **Celery 文档**: https://docs.celeryq.dev/

---

## 💡 提示 / Tips

1. **首次运行**: 建议先运行示例数据脚本，确保系统正常工作
2. **开发模式**: 修改代码后会自动重载（DEBUG=True）
3. **日志文件**: 在 `logs/` 目录查看详细日志
4. **导出文件**: 生成的文件在 `exports/` 目录
5. **API 测试**: 使用 http://localhost:8000/docs 进行交互式测试

---

## 🆘 需要帮助？/ Need Help?

1. 查看 `README.md` 获取完整文档
2. 查看 `PROJECT_STATUS.md` 了解项目状态
3. 检查 `logs/` 目录中的日志文件
4. 访问 http://localhost:8000/health 检查服务状态

---

**祝你使用愉快！/ Enjoy!** 🚀


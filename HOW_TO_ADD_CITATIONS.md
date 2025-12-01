# 如何添加论文之间的引用关系

## 1. 系统现状

当前系统已经支持论文引用关系（CITES）的展示：
- 后端已经在查询中包含了引用关系
- 前端已经有引用边的样式（红色虚线）
- 点击引用边会显示"（引用）"提示

## 2. 添加引用关系的方法

### 方法一：使用自动脚本添加示例引用关系

我们提供了一个脚本可以自动为现有论文添加示例引用关系：

```bash
# 激活虚拟环境
venv\Scripts\activate

# 运行添加引用数据的脚本
python scripts/add_citations.py
```

这个脚本会：
- 查找数据库中的论文节点
- 创建论文之间的引用关系（CITES）
- 创建一些交叉引用使图谱更真实

### 方法二：手动添加特定引用关系

如果你想手动添加特定的引用关系，可以使用以下方法：

#### 使用 Neo4j 浏览器
1. 打开 Neo4j 浏览器（通常在 http://localhost:7474）
2. 运行以下 Cypher 查询：

```cypher
MATCH (p1:Paper {title: "论文标题1"}), (p2:Paper {title: "论文标题2"})
MERGE (p1)-[r:CITES]->(p2)
ON CREATE SET r.citation_count = 1, r.year = 2023
ON MATCH SET r.citation_count = r.citation_count + 1
RETURN r
```

#### 使用 Python 脚本
你也可以修改 `scripts/add_citations.py` 脚本，添加你需要的特定引用关系。

## 3. 查看引用关系

添加完成后，你可以在知识图谱页面中：
1. 展开作者节点查看其论文
2. 论文之间会显示红色虚线表示引用关系
3. 点击引用边可以查看详细信息

## 4. 注意事项

- 引用关系是有方向的：`p1-[:CITES]->p2` 表示 p1 引用了 p2
- 脚本会自动处理重复的引用关系
- 可以根据需要修改脚本中的引用模式
- 确保 Neo4j 服务已经启动并且可以正常连接

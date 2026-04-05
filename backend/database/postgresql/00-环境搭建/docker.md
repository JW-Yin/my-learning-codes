# 🚀 Fedora + Docker 快速部署 **pgvector** 极简速查流程
（另一台设备**直接按顺序复制粘贴**，30秒跑通，数据持久化+插件就绪）

## 一、前提
另一台电脑已装好 **Docker**（用你之前保存的 Docker 安装流程即可）

---

# 二、核心部署流程（**全程可直接复制**）
## 1. 拉取 pgvector 镜像（PostgreSQL 17 + vector 插件）
```bash
docker pull pgvector/pgvector:pg17-trixie
```

## 2. 创建数据卷（**必做**：删容器不丢数据）
```bash
docker volume create pgvector-data
```

## 3. 启动 pgvector 容器（端口+密码+持久化一站式）
```bash
docker run -d \
  --name pgvector \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=postgres \
  -v pgvector-data:/var/lib/postgresql/data \
  --restart always \
  pgvector/pgvector:pg17-trixie
```

## 4. 进入数据库并启用向量插件
```bash
docker exec -it pgvector psql -U postgres
```
在 psql 中执行：
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 5. 验证插件（看到 vector 即成功）
```sql
\dx
```

---

# 三、连接信息（直接用）
```
主机: localhost
端口: 5432
用户: postgres
密码: 123456
数据库: postgres
插件: vector (0.8.2)
```

退出 psql：
```sql
\q
```

---

# 四、常用运维命令（备用）
```bash
# 查看运行状态
docker ps

# 重启
docker restart pgvector

# 停止
docker stop pgvector

# 启动
docker start pgvector

# 查看日志
docker logs pgvector

# 再次进入数据库
docker exec -it pgvector psql -U postgres
```

---

# ✅ 一句话总结
**拉镜像 → 建数据卷 → 启动容器 → 装插件**
另一台 Fedora 照抄这套，**pgvector 立刻可用**，适配 AI 向量库/RAG 场景。
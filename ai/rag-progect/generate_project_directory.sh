#!/bin/bash

# 定义项目根目录名称（可自定义，默认是project）
PROJECT_NAME=${1:-project}

# 提示开始生成目录结构
echo "开始生成项目目录结构，根目录：$PROJECT_NAME"

# ====================== 创建所有目录（-p确保多级目录递归创建） ======================
mkdir -p \
  $PROJECT_NAME/api \
  $PROJECT_NAME/config \
  $PROJECT_NAME/db \
  $PROJECT_NAME/model \
  $PROJECT_NAME/rag \
  $PROJECT_NAME/data/docs \
  $PROJECT_NAME/data/logs \
  $PROJECT_NAME/docker

# ====================== 创建所有空文件 ======================
touch \
  $PROJECT_NAME/api/main.py \
  $PROJECT_NAME/config/config.py \
  $PROJECT_NAME/db/mongo_db.py \
  $PROJECT_NAME/db/milvus_db.py \
  $PROJECT_NAME/db/neo4j_db.py \
  $PROJECT_NAME/model/embedding.py \
  $PROJECT_NAME/model/llm.py \
  $PROJECT_NAME/model/reranker.py \
  $PROJECT_NAME/rag/basic_rag.py \
  $PROJECT_NAME/rag/enhanced_rag.py \
  $PROJECT_NAME/docker/docker-compose.yml \
  $PROJECT_NAME/requirements.txt

# 提示生成完成
echo "✅ 目录结构生成完成！"
echo "项目路径：$(pwd)/$PROJECT_NAME"

# 可选：列出生成的目录结构（验证结果）
echo -e "\n生成的目录结构预览："
tree $PROJECT_NAME --dirsfirst 2>/dev/null || ls -R $PROJECT_NAME


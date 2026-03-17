# model/embedding.py
from langchain_community.embeddings import DashScopeEmbeddings
from config.config import DASHSCOPE_API_KEY

# 初始化通义千问Embedding
def get_embedding_model():
    """获取Embedding模型实例（极简版）"""
    return DashScopeEmbeddings(
        model="text-embedding-v1",  # 通义千问轻量嵌入模型
        api_key=DASHSCOPE_API_KEY
    )

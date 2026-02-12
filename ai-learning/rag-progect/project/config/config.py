# config/config.py
import os
from dotenv import load_dotenv

# 加载.env文件（可选，也可直接写死）
load_dotenv()

# 阿里云通义千问API Key（替换成你自己的！）
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "你的通义千问API Key")

# 基础RAG配置
RAG_CONFIG = {
    "chunk_size": 500,  # 文本分割长度
    "chunk_overlap": 50,  # 文本重叠长度
    "top_k": 3,  # 检索Top-K条结果
}

# 检查API Key是否配置
if not DASHSCOPE_API_KEY or DASHSCOPE_API_KEY == "你的通义千问API Key":
    raise ValueError("请先配置通义千问API Key！可在阿里云百炼平台申请：https://dashscope.aliyun.com/")

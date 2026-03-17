from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
# 加载 .env 文件
load_dotenv()


class Settings(BaseSettings):
    # 项目
    PROJECT_NAME: str = "Enhanced RAG System"
    VERSION: str = "1.0.0"
    
    # 数据库
    MONGO_URI: str = "mongodb://admin:admin123@localhost:27017/"
    MONGO_DB_NAME: str = "rag_kb"
    MONGO_COLLECTION: str = "documents"
    
    MILVUS_URI: str = "http://localhost:19530"
    MILVUS_COLLECTION: str = "langchain_chunks"
    
    # 模型
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "API出问题了，请检查环境变量")
    LLM_MODEL: str = "qwen-plus"
    EMBEDDING_MODEL: str = "text-embedding-v3"
    VECTOR_DIM: int = 1024

settings = Settings()

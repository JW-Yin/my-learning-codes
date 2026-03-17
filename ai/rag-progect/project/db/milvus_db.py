from pymilvus import connections, utility
from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import DashScopeEmbeddings
from config.config import settings

class MilvusManager:
    def __init__(self):
        # 1. 初始化 Embedding
        self.embeddings = DashScopeEmbeddings(
            model=settings.EMBEDDING_MODEL,
            dashscope_api_key=settings.DASHSCOPE_API_KEY
        )
        
        # 2. 连接 Milvus
        connections.connect("default", uri=settings.MILVUS_URI)
        
        # 3. 初始化 LangChain VectorStore
        self.vector_store = Milvus(
            embedding_function=self.embeddings,
            connection_args={"uri": settings.MILVUS_URI},
            collection_name=settings.MILVUS_COLLECTION,
            auto_id=True,
            drop_old=False # 设为 False，重启服务数据不丢失
        )

    def get_vector_store(self):
        return self.vector_store

    def get_retriever(self, k: int = 3):
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    def reset_collection(self):
        """清空集合（慎用）"""
        if utility.has_collection(settings.MILVUS_COLLECTION):
            utility.drop_collection(settings.MILVUS_COLLECTION)
            self.__init__() # 重新初始化

milvus_manager = MilvusManager()

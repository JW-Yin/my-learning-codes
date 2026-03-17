from pymongo import MongoClient
from datetime import datetime
from config.config import settings

class MongoDBManager:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db[settings.MONGO_COLLECTION]

    def add_doc_metadata(self, doc_id: str, title: str, content: str, source: str = "manual"):
        """保存文档的原始信息和元数据"""
        doc = {
            "_id": doc_id,
            "title": title,
            "content": content,
            "source": source,
            "created_at": datetime.utcnow()
        }
        return self.collection.insert_one(doc)

    def get_doc_by_id(self, doc_id: str):
        return self.collection.find_one({"_id": doc_id})

mongo_manager = MongoDBManager()

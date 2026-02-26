from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config.config import settings
from rag.basic_rag import basic_rag
from db.mongo_db import mongo_manager
import uuid

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# --- 数据模型 ---
class AddDocRequest(BaseModel):
    title: str
    content: str

class QueryRequest(BaseModel):
    question: str

# --- 接口 ---

@app.get("/")
def root():
    return {"message": "RAG System Online", "docs": "/docs"}

@app.post("/admin/add_knowledge")
def add_knowledge(req: AddDocRequest):
    """
    1. 先把元数据存入 MongoDB
    2. 再把内容切分向量化存入 Milvus (通过 LangChain)
    """
    try:
        # 生成唯一 ID
        doc_id = str(uuid.uuid4())
        
        # 1. 存 MongoDB (留底)
        mongo_manager.add_doc_metadata(doc_id, req.title, req.content)
        
        # 2. 存 Milvus (用于检索)
        basic_rag.add_documents(
            texts=[req.content],
            metadatas=[{"doc_id": doc_id, "title": req.title}]
        )
        
        return {"status": "success", "doc_id": doc_id, "title": req.title}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(req: QueryRequest):
    """
    基础 RAG 问答
    """
    try:
        result = basic_rag.query(req.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

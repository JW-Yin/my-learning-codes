# api/main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from rag.basic_rag import init_basic_rag, basic_rag_query

# 初始化FastAPI应用
app = FastAPI(title="极简RAG Demo", version="0.1")

# 启动时初始化RAG（加载文档+构建向量库）
@app.on_event("startup")
def startup_event():
    """服务启动时初始化RAG"""
    init_basic_rag()

# 暴露RAG查询接口
@app.get("/rag/query")
def rag_query(question: str):
    """
    极简RAG查询接口
    :param question: 用户问题（如：重疾险和医疗险有什么区别？）
    """
    if not question:
        raise HTTPException(status_code=400, detail="问题不能为空！")
    try:
        result = basic_rag_query(question)
        return {
            "code": 200,
            "message": "查询成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败：{str(e)}")

# 本地运行入口
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

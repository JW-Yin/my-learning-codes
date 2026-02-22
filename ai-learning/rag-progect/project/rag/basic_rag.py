# rag/basic_rag.py（最简RAG版，替换你原来的伪RAG逻辑）
import os
import numpy as np
import faiss
from config.config import DASHSCOPE_API_KEY, RAG_CONFIG
from model.embedding import get_embedding_model
from model.llm import get_llm_model
from langchain.prompts import PromptTemplate

# 全局变量：文本块 + Faiss向量库 + Embedding/LLM模型
DOC_CHUNKS = []
FAISS_INDEX = None
EMBEDDING_MODEL = get_embedding_model()
LLM_MODEL = get_llm_model()

# 最简回答模板
PROMPT_TEMPLATE = """
请根据以下参考信息回答用户问题，仅使用参考信息中的内容，不要编造：

参考信息：
{context}

用户问题：{question}

回答要求：简洁、清晰，用中文回答。
"""
PROMPT = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])

def init_basic_rag(doc_path: str = "data/docs/test_doc.txt"):
    """初始化最简RAG：加载文档→切分→向量化→存入Faiss"""
    global DOC_CHUNKS, FAISS_INDEX
    
    # 1. 加载并切分文档（复用你原来的切分逻辑）
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"文档不存在：{doc_path}")
    
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    DOC_CHUNKS = []
    start = 0
    chunk_size = RAG_CONFIG["chunk_size"]
    while start < len(text):
        chunk = text[start:start+chunk_size].strip()
        if chunk:
            DOC_CHUNKS.append(chunk)
        start += chunk_size
    
    # 2. 文本块向量化（通义千问Embedding）
    chunk_vectors = EMBEDDING_MODEL.embed_documents(DOC_CHUNKS)
    chunk_vectors = np.array(chunk_vectors).astype("float32")
    
    # 3. 初始化Faiss向量库并入库
    FAISS_INDEX = faiss.IndexFlatL2(chunk_vectors.shape[1])  # L2距离等价余弦相似度
    FAISS_INDEX.add(chunk_vectors)
    
    print(f"✅ 最简RAG初始化完成：文本块数={len(DOC_CHUNKS)}，向量维度={chunk_vectors.shape[1]}")

def basic_rag_query(question: str):
    """最简RAG查询：问题向量化→Faiss检索→LLM生成回答"""
    global DOC_CHUNKS, FAISS_INDEX
    
    # 1. 问题向量化
    q_vector = EMBEDDING_MODEL.embed_query(question)
    q_vector = np.array([q_vector]).astype("float32")
    
    # 2. Faiss检索Top-K相似文本
    distances, indices = FAISS_INDEX.search(q_vector, RAG_CONFIG["top_k"])
    top_chunks = [DOC_CHUNKS[i] for i in indices[0] if distances[0][list(indices[0]).index(i)] < 1.0]
    
    # 3. 生成回答
    if not top_chunks:
        answer = "抱歉，未找到相关信息。"
    else:
        context = "\n".join(top_chunks)
        prompt = PROMPT.format(context=context, question=question)
        answer = LLM_MODEL.invoke(prompt).content
    
    return {
        "answer": answer,
        "source_documents": top_chunks
    }

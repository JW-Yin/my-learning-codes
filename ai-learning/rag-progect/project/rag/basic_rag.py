# rag/basic_rag.py
import os
import math
from collections import Counter

# Minimal dependency-free RAG implementation.
# It loads documents, splits them into chunks, and does a simple
# TF (term-frequency) based cosine-similarity retrieval. This avoids
# external API keys and langchain dependencies so the demo can run locally.

# Global storage
DOC_CHUNKS = []  # list of strings (chunks)

def _tokenize(text: str):
    # very small tokenizer: split on whitespace and punctuation
    if not text:
        return []
    tokens = []
    cur = []
    for ch in text:
        # If Chinese character, emit it as its own token
        if '\u4e00' <= ch <= '\u9fff':
            if cur:
                tokens.append(''.join(cur).lower())
                cur = []
            tokens.append(ch)
        elif ch.isalnum():
            cur.append(ch)
        else:
            if cur:
                tokens.append(''.join(cur).lower())
                cur = []
    if cur:
        tokens.append(''.join(cur).lower())
    return tokens

def _tf_vector(tokens):
    return Counter(tokens)

def _cosine_sim(c1: Counter, c2: Counter):
    # compute cosine similarity between two term-frequency counters
    if not c1 or not c2:
        return 0.0
    # dot product
    dot = 0
    for k, v in c1.items():
        dot += v * c2.get(k, 0)
    norm1 = math.sqrt(sum(v * v for v in c1.values()))
    norm2 = math.sqrt(sum(v * v for v in c2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def init_basic_rag(doc_path: str = "data/docs/test_docs.txt", chunk_size: int = 500):
    """
    Initialize minimal RAG: ensure doc exists, split into chunks and store them.
    """
    global DOC_CHUNKS
    if not os.path.exists(doc_path):
        os.makedirs(os.path.dirname(doc_path), exist_ok=True)
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write("""
保险基础知识：
1. 重疾险：保障重大疾病（如癌症、心梗），确诊后一次性赔付保额。
2. 医疗险：报销医疗费用，实报实销，通常有免赔额。
3. 意外险：保障意外身故/伤残、意外医疗，保费低，杠杆高。
            """)
        print(f"⚠️ 未找到测试文档，已自动创建：{doc_path}")

    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()

    # simple chunking by fixed character size
    DOC_CHUNKS = []
    start = 0
    while start < len(text):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            DOC_CHUNKS.append(chunk)
        start += chunk_size

    print(f"✅ 基础RAG初始化完成！分割后片段数：{len(DOC_CHUNKS)}")

def basic_rag_query(question: str, top_k: int = 3):
    """
    Perform a simple retrieval based on term-overlap cosine similarity
    and return the top_k chunks concatenated as the "answer".
    """
    global DOC_CHUNKS
    if not DOC_CHUNKS:
        init_basic_rag()

    q_tokens = _tokenize(question)
    q_vec = _tf_vector(q_tokens)

    scored = []
    for chunk in DOC_CHUNKS:
        tokens = _tokenize(chunk)
        vec = _tf_vector(tokens)
        sim = _cosine_sim(q_vec, vec)
        scored.append((sim, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [c for s, c in scored[:top_k] if s > 0]

    # Simple answer: concatenate top chunks; if none matched, return a fallback
    if top:
        answer = "\n".join(top)
    else:
        answer = "抱歉，未找到相关信息。"

    return {
        "answer": answer,
        "source_documents": top
    }

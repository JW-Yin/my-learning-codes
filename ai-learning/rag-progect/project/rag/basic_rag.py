# rag/basic_rag.py
import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from model.embedding import get_embedding_model
from model.llm import get_llm_model
from config.config import RAG_CONFIG

# 全局变量：存储向量库（避免每次查询都重新加载）
vector_db = None

def init_basic_rag(doc_path: str = "data/docs/test_docs.txt"):
    """
    初始化基础RAG：加载文档→分割→向量化→构建向量库
    :param doc_path: 测试文档路径（需提前创建）
    """
    global vector_db
    # 1. 检查测试文档是否存在，不存在则创建示例文档
    if not os.path.exists(doc_path):
        os.makedirs(os.path.dirname(doc_path), exist_ok=True)
        # 写入示例保险文档内容（极简测试用）
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write("""
保险基础知识：
1. 重疾险：保障重大疾病（如癌症、心梗），确诊后一次性赔付保额。
2. 医疗险：报销医疗费用，实报实销，通常有免赔额。
3. 意外险：保障意外身故/伤残、意外医疗，保费低，杠杆高。
            """)
        print(f"⚠️ 未找到测试文档，已自动创建：{doc_path}")

    # 2. 加载文档
    loader = TextLoader(doc_path, encoding="utf-8")
    documents = loader.load()

    # 3. 文本分割
    text_splitter = CharacterTextSplitter(
        chunk_size=RAG_CONFIG["chunk_size"],
        chunk_overlap=RAG_CONFIG["chunk_overlap"],
        separator="\n"
    )
    splits = text_splitter.split_documents(documents)

    # 4. 构建向量库（FAISS，本地轻量存储）
    embedding = get_embedding_model()
    vector_db = FAISS.from_documents(splits, embedding)
    print(f"✅ 基础RAG初始化完成！加载文档数：{len(documents)}，分割后片段数：{len(splits)}")

def basic_rag_query(question: str) -> str:
    """
    极简RAG查询：检索+生成回答
    :param question: 用户问题
    :return: LLM生成的回答
    """
    global vector_db
    # 检查向量库是否初始化
    if vector_db is None:
        init_basic_rag()

    # 1. 构建检索链
    llm = get_llm_model()
    # 极简提示词：只告诉LLM用检索到的信息回答问题
    prompt = PromptTemplate(
        template="""请根据以下参考信息回答用户问题，只使用参考信息中的内容，不要编造：
参考信息：
{context}

用户问题：{question}
        """,
        input_variables=["context", "question"]
    )

    # 2. 构建RAG链
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # 极简模式：把所有检索结果拼接给LLM
        retriever=vector_db.as_retriever(search_kwargs={"k": RAG_CONFIG["top_k"]}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True  # 返回检索到的源文档（方便调试）
    )

    # 3. 执行查询
    result = qa_chain({"query": question})
    # 4. 返回回答（简化版，只返回核心内容）
    return {
        "answer": result["result"],
        "source_documents": [doc.page_content for doc in result["source_documents"]]
    }

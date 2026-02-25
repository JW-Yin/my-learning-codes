from langchain.chains import RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from db.milvus_db import milvus_manager
from model.llm import llm_service

class BasicRAG:
    def __init__(self):
        # 获取组件
        self.llm = llm_service.get_llm()
        self.prompt = llm_service.get_rag_prompt()
        self.retriever = milvus_manager.get_retriever(k=3)
        
        # 构建 Chain (LangChain 新版本写法)
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.combine_docs_chain)

    def query(self, question: str):
        """
        输入问题，返回答案和来源
        """
        result = self.rag_chain.invoke({"input": question})
        
        return {
            "question": question,
            "answer": result['answer'],
            "source_documents": [doc.page_content for doc in result['context']]
        }

    def add_documents(self, texts: list, metadatas: list = None):
        """
        批量添加文档到知识库
        """
        return milvus_manager.vector_store.add_texts(texts=texts, metadatas=metadatas)

basic_rag = BasicRAG()

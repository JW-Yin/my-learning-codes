from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate
from config.config import settings

class LLMService:
    def __init__(self):
        self.llm = Tongyi(
            model_name=settings.LLM_MODEL,
            dashscope_api_key=settings.DASHSCOPE_API_KEY,
            temperature=0.1 # 越低越严谨
        )
        
        # 定义 RAG 提示词模板
        self.rag_prompt = PromptTemplate(
            template="""你是一个专业的知识助手。请仅根据以下【参考资料】回答用户的问题。
            如果参考资料中没有答案，请直接回答“知识库中暂无相关信息”。
            不要编造内容。
            
            【参考资料】：
            {context}
            
            【用户问题】：
            {question}
            """,
            input_variables=["context", "question"]
        )

    def get_llm(self):
        return self.llm

    def get_rag_prompt(self):
        return self.rag_prompt

llm_service = LLMService()

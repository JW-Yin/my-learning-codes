# model/llm.py
from langchain_community.chat_models import ChatDashScope
from config.config import DASHSCOPE_API_KEY

# 初始化通义千问LLM
def get_llm_model():
    """获取LLM模型实例（极简版）"""
    return ChatDashScope(
        model="qwen-turbo",  # 通义千问轻量版（免费额度足够）
        api_key=DASHSCOPE_API_KEY,
        temperature=0.1,  # 低随机性，保证回答稳定
    )

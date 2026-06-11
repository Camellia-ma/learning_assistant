""" 配置 RAG 使用的模型以及提示词 """
# 阿里云向量化模型
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI  # 接口
from app.config import *

# RAG流程模型配置
def create_rag_model():
        model = ChatOpenAI(
                base_url=ALIYUN_URL,
                api_key=API_KEY,
                model=RAG_MODEL,
        )

        return model

# 向量化模型配置
def create_embedding_model():
        model = DashScopeEmbeddings(
                model= EMBEDDING_MODEL,
                dashscope_api_key=API_KEY
        )
        return model

# RAG 流程提示词
rag_system_prompt = (
        "你是一个专业、严谨的学习助手。\n"
        "请结合以下检索到的参考资料来回答学生的问题。如果你不知道，就明确说不知道，不要瞎编。\n"
        "请用清晰的逻辑、分条理地回答，适合学生理解。\n\n"
        "【参考资料】:\n{context}"
        )
prompt = ChatPromptTemplate.from_messages([
        ("system", rag_system_prompt),
        ("human", "{input}"),
])
""" RAG API控制路由 """
"""AI 对话、Agent 规划、RAG 问答 API（核心）"""
from fastapi import APIRouter, HTTPException, status
from app.api.rag.result import ChatRequest, ChatResponse, InitDBResponse
from app.services.ai.rag.RAG import RAG

router = APIRouter(prefix="/rag", tags=["AI 学习助手 -- rag 流程"])

# 实例化 RAG 核心类
RAGBot = RAG()

# 初始化知识库 -- 向知识库传入新文件时调用以重新加载知识库以及向量库
@router.post("/init-knowledge-base", response_model=InitDBResponse, status_code=status.HTTP_200_OK)
async def init_knowledge_base():
    try:
        # 在线程池中执行耗时的 CPU 绑定和网络绑定操作，避免阻塞异步主线程
        result_message = RAGBot.init_knowledge_base()
        return InitDBResponse(message=result_message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"知识库构建失败: {str(e)}"
        )

"""
    【学生端】基于知识库的非流式标准问答接口
    接收前端传来的 question，返回包含完整 answer 的 JSON 数据。
"""
@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def rag_chat(payload: ChatRequest):

    if not payload.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="提问内容不能为空"
        )

    try:
        # 调用 RAG 实例获取大模型回答
        ai_answer = RAGBot.query(payload.question,payload.chat_name)
        return ChatResponse(answer=ai_answer, status="success")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI 问答服务异常: {str(e)}"
        )
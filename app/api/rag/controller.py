""" RAG API控制路由 """
from fastapi import APIRouter, HTTPException, status
from app.api.rag.result import ChatRequest, ChatResponse, InitDBResponse, ChatHistoryListResponse, ChatHistoryRequest, ChatHistoryResponse, ChatMessage, CreateChatRequest, CreateChatResponse
from app.services.ai.rag.RAG import RAG
from app.services.ai.rag.history_message_manage import load_history_message
from pathlib import Path

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

""" 
    获取data/history/目录下的所有对话（历史）列表
"""
@router.get("/history", response_model=ChatHistoryListResponse, status_code=status.HTTP_200_OK)
async def get_all_chat_name():
    try:
        HISTORY_BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent / "data" / "history"
        HISTORY_BASE_PATH.mkdir(parents=True, exist_ok=True)
        # 获取所有 .json 文件，去掉扩展名
        chat_names = [f.stem for f in HISTORY_BASE_PATH.glob("*.json")]
        return ChatHistoryListResponse(chat_names=chat_names)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取对话列表失败: {str(e)}"
        )

"""
    获取特定对话的对话历史
"""
@router.post("/history/detail", response_model=ChatHistoryResponse, status_code=status.HTTP_200_OK)
async def get_chat_message(payload: ChatHistoryRequest):
    if not payload.chat_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="对话名称不能为空"
        )

    try:
        # 加载历史消息
        history = load_history_message(payload.chat_name)
        # 转换为响应格式
        messages = []
        for msg in history:
            msg_type = "human" if hasattr(msg, 'type') and msg.type == "human" else "ai"
            messages.append(ChatMessage(type=msg_type, content=msg.content))
        return ChatHistoryResponse(messages=messages)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取对话历史失败: {str(e)}"
        )


"""
    新建对话
"""
@router.post("/history/create", response_model=CreateChatResponse, status_code=status.HTTP_201_CREATED)
async def create_new_chat(payload: CreateChatRequest):
    if not payload.chat_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="对话名称不能为空"
        )

    try:
        HISTORY_BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent / "data" / "history"
        HISTORY_BASE_PATH.mkdir(parents=True, exist_ok=True)
        
        safe_name = Path(payload.chat_name).name
        if not safe_name.endswith('.json'):
            safe_name += '.json'
        
        chat_file = HISTORY_BASE_PATH / safe_name
        
        if chat_file.exists():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"对话 '{payload.chat_name}' 已存在"
            )
        
        import json
        with open(chat_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)
        
        return CreateChatResponse(message=f"对话 '{payload.chat_name}' 创建成功", chat_name=payload.chat_name)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建对话失败: {str(e)}"
        )
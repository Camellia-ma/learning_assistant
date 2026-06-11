""" Agent API控制路由 """
from fastapi import APIRouter, HTTPException, status
from app.api.agent.result import AgentChatRequest, AgentChatResponse
from app.services.ai.agent.homework_agent import HomeworkAgentService

router = APIRouter(prefix="/agent", tags=["AI 学习助手 -- agent 流程"])

# 实例化 Agent 核心类
HomeworkAgent = HomeworkAgentService()


"""
    【学生端】Agent 作业管理对话接口
    接收前端传来的 question，返回包含完整 answer 的 JSON 数据。
"""
@router.post("/chat", response_model=AgentChatResponse, status_code=status.HTTP_200_OK)
async def agent_chat(payload: AgentChatRequest):

    if not payload.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="提问内容不能为空"
        )

    try:
        # 调用 Agent 实例获取大模型回答
        ai_answer = HomeworkAgent.run(
            user_input=payload.question,
        )
        return AgentChatResponse(answer=ai_answer, status="success")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent 服务异常: {str(e)}"
        )

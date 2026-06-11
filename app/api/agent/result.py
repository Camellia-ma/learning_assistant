""" 后端统一返回结果 """
from pydantic import BaseModel, Field
from typing import List, Optional, Any


# 接收格式
class AgentChatRequest(BaseModel):
    question: str = Field(..., description="用户的提问内容")


# 返回格式
class AgentChatResponse(BaseModel):
    answer: str = Field(..., description="Agent 给出的完整回答")
    status: str = Field("success", description="状态码")

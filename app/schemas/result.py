""" 后端统一返回结果 """
from pydantic import BaseModel, Field


# 接收格式
class ChatRequest(BaseModel):
    question: str = Field(..., description="学生的提问内容")

# 返回格式
class ChatResponse(BaseModel):
    answer: str = Field(..., description="AI 结合知识库给出的完整回答")
    status: str = Field("success", description="状态码")

class InitDBResponse(BaseModel):
    message: str = Field(..., description="初始化结果提示信息")
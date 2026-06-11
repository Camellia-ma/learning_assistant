""" 后端统一返回结果 """
from typing import List
from pydantic import BaseModel, Field


# 接收格式
class ChatRequest(BaseModel):
    question: str = Field(..., description="学生的提问内容")
    chat_name: str = Field(..., description="对话名称")

# 返回格式
class ChatResponse(BaseModel):
    answer: str = Field(..., description="AI 结合知识库给出的完整回答")
    status: str = Field("success", description="状态码")

class InitDBResponse(BaseModel):
    message: str = Field(..., description="初始化结果提示信息")

# 获取所有对话历史返回列表
class ChatHistoryListResponse(BaseModel):
    chat_names: List[str] = Field(..., description="所有对话名称列表")

# 获取特定对话历史 - 请求格式
class ChatHistoryRequest(BaseModel):
    chat_name: str = Field(..., description="对话名称")

# 获取特定对话历史 - 单条消息格式
class ChatMessage(BaseModel):
    type: str = Field(..., description="消息类型: human 或 ai")
    content: str = Field(..., description="消息内容")

# 获取特定对话历史 - 返回格式
class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessage] = Field(..., description="对话历史消息列表")

# 新建对话 - 请求格式
class CreateChatRequest(BaseModel):
    chat_name: str = Field(..., description="新对话名称")

# 新建对话 - 返回格式
class CreateChatResponse(BaseModel):
    message: str = Field(..., description="创建结果提示信息")
    chat_name: str = Field(..., description="新创建的对话名称")
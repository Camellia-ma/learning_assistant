""" 上传接口统一返回结果 """
from typing import List
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    message: str = Field(..., description="上传结果提示信息")
    file_names: List[str] = Field(..., description="成功上传的文件名列表")


class KnowledgeFileResponse(BaseModel):
    file_names: List[str] = Field(..., description="知识库中所有文件列表")
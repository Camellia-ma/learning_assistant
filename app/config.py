""" 定义常量 """

import os

# 模型URL
ALIYUN_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"        # 阿里云百炼平台基础路径
LOCAL_URL = "http://localhost:11434"                    # 本地部署模型端口号
API_KEY = os.getenv("DASHSCOPE_API_KEY")                # Api key设置

# 模型名称
RAG_MODEL = "deepseek-v4-flash"      # RAG 流程使用deepseek-v4-flash
EMBEDDING_MODEL = "text-embedding-v4"     # 阿里云最新通用文本向量化模型
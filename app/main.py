from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rag.controller import router as rag_router
from app.api.agent.controller import router as agent_router
import uvicorn
app = FastAPI(
    title="AI 学习助手后端 API",
    description="基于 FastAPI + RAG + Agent 的学习助手系统",
    version="1.0.0"
)

# 配置跨域，允许 Vue 前端访问 -- 使用前后端分离的开发模式
origins = [
    "http://localhost:5173",  # Vue3 Vite 默认开发端口
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # 允许所有 HTTP 方法 (POST, GET 等)
    allow_headers=["*"],      # 允许所有请求头
)

# 注册 RAG 模块路由
app.include_router(rag_router, prefix="/api")

# 注册 Agent 模块路由
app.include_router(agent_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": " 欢迎使用学习助手 "}


""" 启动后端项目 """
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
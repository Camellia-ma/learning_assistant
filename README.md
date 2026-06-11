# AI 学习助手后端系统

基于 FastAPI + RAG（Retrieval-Augmented Generation）+ Agent 的智能学习助手后端服务。

## 项目架构

```
learning_assistant/
├── app/                              # 应用主目录
│   ├── __init__.py                   # 包初始化
│   ├── config.py                     # 配置常量定义
│   ├── main.py                       # FastAPI 主入口
│   ├── api/                          # API 控制层
│   │   ├── __init__.py
│   │   ├── agent/                    # Agent 模块
│   │   │   ├── __init__.py
│   │   │   ├── controller.py         # Agent API 路由控制器
│   │   │   └── result.py             # 请求/响应数据模型
│   │   ├── rag/                      # RAG 模块
│   │   │   ├── __init__.py
│   │   │   ├── controller.py         # RAG API 路由控制器
│   │   │   └── result.py             # 请求/响应数据模型
│   │   └── upload/                   # 文件上传模块
│   │       ├── __init__.py
│   │       ├── controller.py         # 上传 API 路由控制器
│   │       └── result.py             # 请求/响应数据模型
│   └── services/                     # 业务服务层
│       ├── __init__.py
│       ├── ai/                       # AI 服务模块
│       │   ├── __init__.py
│       │   ├── agent/                # Agent 服务
│       │   │   ├── __init__.py
│       │   │   ├── homework_agent.py # 作业管理 Agent
│       │   │   ├── tools.py          # Agent 工具定义
│       │   │   └── model_config.py   # Agent 模型配置
│       │   └── rag/                  # RAG 核心服务
│       │       ├── __init__.py
│       │       ├── RAG.py            # RAG 核心类
│       │       ├── document_operation.py  # 文档操作工具
│       │       ├── history_message_manage.py  # 历史消息管理
│       │       └── model_config.py   # 模型配置
│       └── homework/                 # 作业服务
│           ├── __init__.py
│           └── homework_services.py  # 作业数据操作
├── data/                             # 数据目录（运行时自动创建）
│   ├── knowledge_base/               # 知识库文档目录
│   ├── vector_store/                 # 向量库存储目录
│   └── history/                      # RAG对话历史存储目录
├── requirements.txt                  # 项目依赖
├── 接口文档.md                        # API 接口文档
└── README.md                         # 项目说明文档
```

## 核心功能模块

### 1. 主入口模块 (`app/main.py`)

**功能说明**：FastAPI 应用的主入口，负责初始化应用、配置跨域、注册路由。

**关键函数/组件**：

| 组件 | 类型 | 说明 |
|------|------|------|
| `app` | FastAPI 实例 | 应用主对象，配置了标题、描述和版本 |
| `CORSMiddleware` | 中间件 | 配置跨域访问，允许 Vue3 前端（localhost:5173）访问 |
| `rag_router` | 路由 | 注册 RAG 模块的 API 路由，前缀为 `/api` |
| `agent_router` | 路由 | 注册 Agent 模块的 API 路由，前缀为 `/api` |
| `upload_router` | 路由 | 注册文件上传模块的 API 路由，前缀为 `/api` |
| `root()` | 接口 | GET `/` - 健康检查接口，返回欢迎信息 |
| `uvicorn.run()` | 启动函数 | 运行服务于 `localhost:8000` |

### 2. 配置模块 (`app/config.py`)

**功能说明**：定义系统常量配置，包括模型服务地址和 API Key。

**配置项**：

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `ALIYUN_URL` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 阿里云百炼平台 API 地址（兼容 OpenAI 协议） |
| `LOCAL_URL` | `http://localhost:11434` | 本地模型服务地址（预留） |
| `API_KEY` | 环境变量 `DASHSCOPE_API_KEY` | 阿里云 API 密钥 |
| `RAG_MODEL` | `deepseek-v4-flash` | RAG 流程使用的大语言模型 |
| `AGENT_MODEL` | `deepseek-v4-flash` | Agent 使用的大语言模型 |
| `EMBEDDING_MODEL` | `text-embedding-v4` | 文本向量化模型 |

### 3. RAG API 控制器 (`app/api/rag/controller.py`)

**功能说明**：定义 RAG 相关的 RESTful API 接口，处理 HTTP 请求和响应。

**API 接口**：

| 接口路径 | HTTP 方法 | 功能 |
|----------|----------|------|
| `/api/rag/init-knowledge-base` | POST | 初始化知识库，扫描文档并构建向量索引 |
| `/api/rag/chat` | POST | 基于知识库的问答接口，接收问题返回 AI 回答 |

### 4. Agent API 控制器 (`app/api/agent/controller.py`)

**功能说明**：定义 Agent 作业管理相关的 RESTful API 接口。

**API 接口**：

| 接口路径 | HTTP 方法 | 功能 |
|----------|----------|------|
| `/api/agent/chat` | POST | Agent 作业管理对话接口，支持自然语言交互 |

**Agent 支持功能**：
- 添加作业："帮我添加一项数学作业，截止日期是明天"
- 查询全部作业："我有哪些作业？"
- 查询未完成作业："我还有哪些作业没做？"
- 完成作业："我已经完成了数学作业"
- 学习计划："帮我安排一下学习计划"

### 5. 文件上传 API 控制器 (`app/api/upload/controller.py`)

**功能说明**：定义文件上传相关的 RESTful API 接口。

**API 接口**：

| 接口路径 | HTTP 方法 | 功能 |
|----------|----------|------|
| `/api/upload/file` | POST | 上传文件到服务器（不更新知识库） |
| `/api/upload/file-to-knowledge` | POST | 上传文件并更新知识库 |
| `/api/upload/knowledge-files` | GET | 获取知识库文件列表 |
| `/api/upload/knowledge-file/{filename}` | DELETE | 删除知识库中的文件 |

**支持的文件类型**：`.txt`、`.docx`、`.pdf`

### 6. 数据模型

**RAG 数据模型** (`app/api/rag/result.py`)：

| 模型类 | 用途 | 字段 |
|--------|------|------|
| `ChatRequest` | 问答请求 | `question`（问题内容）、`chat_name`（对话名称） |
| `ChatResponse` | 问答响应 | `answer`（AI 回答）、`status`（状态，默认为 success） |
| `InitDBResponse` | 初始化响应 | `message`（结果提示信息） |

**Agent 数据模型** (`app/api/agent/result.py`)：

| 模型类 | 用途 | 字段 |
|--------|------|------|
| `AgentChatRequest` | Agent 对话请求 | `question`、`chat_name`、`chat_history`（可选） |
| `AgentChatResponse` | Agent 对话响应 | `answer`（Agent 回答）、`status` |

**上传数据模型** (`app/api/upload/result.py`)：

| 模型类 | 用途 | 字段 |
|--------|------|------|
| `UploadResponse` | 上传响应 | `message`、`file_names`（上传的文件名列表） |
| `KnowledgeFileResponse` | 文件列表响应 | `file_names`（知识库文件列表） |

### 7. RAG 核心类 (`app/services/ai/rag/RAG.py`)

**功能说明**：RAG 系统的核心类，负责文档加载、向量检索、问答生成和历史管理。

**方法**：

| 方法 | 功能 | 参数 | 返回值 |
|------|------|------|--------|
| `__init__()` | 构造函数，初始化模型并尝试加载本地向量库 | 无 | 无 |
| `init_knowledge_base()` | 扫描知识库目录，构建向量索引 | 无 | 状态消息字符串 |
| `query(user_question, chat_name)` | 执行 RAG 问答，返回 AI 回答 | `user_question`: 用户问题；`chat_name`: 对话名称 | AI 回答字符串 |

**核心流程**：

```
用户提问 → 加载历史消息 → 向量检索相关文档 → RAG Chain 生成回答 → 保存历史记录 → 返回回答
```

### 8. Agent 核心类 (`app/services/ai/agent/homework_agent.py`)

**功能说明**：作业管理 Agent，基于大语言模型实现自然语言交互的作业管理功能。

**类成员**：

| 成员 | 类型 | 说明 |
|------|------|------|
| `tools` | list | Agent 可用的工具列表 |
| `model` | ChatOpenAI | 大语言模型实例 |
| `system_prompt` | string | Agent 系统提示词 |
| `agent` | Agent | LangChain Agent 实例 |

**方法**：

| 方法 | 功能 | 参数 | 返回值 |
|------|------|------|--------|
| `__init__()` | 构造函数，初始化工具和 Agent | 无 | 无 |
| `run(user_input, chat_history)` | 执行 Agent 对话，返回回答 | `user_input`: 用户输入；`chat_history`: 历史对话（可选） | Agent 回答字符串 |

### 9. Agent 工具模块 (`app/services/ai/agent/tools.py`)

**功能说明**：定义 Agent 可用的工具函数。

**工具函数**：

| 工具 | 功能 | 参数 | 返回值 |
|------|------|------|--------|
| `add_new_homework_tool` | 添加新作业 | `homework_name`: 作业名称；`deadline`: 截止日期 | 成功消息 |
| `get_all_homework_tool` | 获取所有作业 | 无 | 作业列表 |
| `get_pending_homework_tool` | 获取未完成作业 | 无 | 未完成作业列表 |
| `update_homework_status_tool` | 更新作业状态 | `homework_id`: 作业ID；`status`: 状态 | 成功消息 |
| `get_now_time_tool` | 获取当前时间 | 无 | 当前时间字符串 |

### 10. 文档操作工具 (`app/services/ai/rag/document_operation.py`)

**功能说明**：提供文档加载、切分和向量库构建的工具函数。

**支持的文档类型**：`.txt`、`.pdf`、`.docx`

### 11. 历史消息管理 (`app/services/ai/rag/history_message_manage.py`)

**功能说明**：管理对话历史消息，支持从 JSON 文件加载和保存。

### 12. 作业服务 (`app/services/homework/homework_services.py`)

**功能说明**：作业数据的 CRUD 操作服务。

## 安装与运行

### 环境要求

- Python 3.10+
- 阿里云百炼 API Key（需在阿里云平台申请）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置环境变量

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY="your-api-key-here"

# Linux/Mac
export DASHSCOPE_API_KEY="your-api-key-here"
```

### 运行服务

```bash
python app/main.py
```

服务将运行在 `http://localhost:8000`

### API 文档

启动服务后，访问以下地址查看自动生成的 API 文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API 使用示例

### 1. 初始化知识库

**请求**：
```bash
POST /api/rag/init-knowledge-base
Content-Type: application/json

{}
```

**响应**：
```json
{
    "message": "知识库构建成功，共处理了 42 个文本切片"
}
```

### 2. RAG 问答接口

**请求**：
```bash
POST /api/rag/chat
Content-Type: application/json

{
    "question": "什么是 RAG？",
    "chat_name": "default"
}
```

**响应**：
```json
{
    "answer": "RAG（Retrieval-Augmented Generation）是一种检索增强生成技术...",
    "status": "success"
}
```

### 3. Agent 作业管理

**请求**：
```bash
POST /api/agent/chat
Content-Type: application/json

{
    "question": "帮我添加一项数学作业，截止日期是2026-06-15",
    "chat_name": "作业管理",
    "chat_history": []
}
```

**响应**：
```json
{
    "answer": "好的，已为您添加数学作业，截止日期为2026年6月15日。",
    "status": "success"
}
```

### 4. 上传文件到知识库

**请求**：
```bash
POST /api/upload/file-to-knowledge
Content-Type: multipart/form-data

files: [document1.txt, report.pdf]
```

**响应**：
```json
{
    "message": "知识库构建成功，共处理了 15 个文本切片，成功上传 2 个文件",
    "file_names": ["document1.txt", "report.pdf"]
}
```

### 5. 获取知识库文件列表

**请求**：
```bash
GET /api/upload/knowledge-files
```

**响应**：
```json
{
    "file_names": ["document1.txt", "report.pdf", "notes.docx"]
}
```

### 6. 删除知识库文件

**请求**：
```bash
DELETE /api/upload/knowledge-file/document1.txt
```

**响应**：
```json
{
    "message": "文件 document1.txt 删除成功，知识库已更新"
}
```

## 数据目录结构

```
data/
├── knowledge_base/   # 存放学习资料文档
│   ├── lesson1.pdf
│   ├── notes.txt
│   └── reference.docx
├── vector_store/     # FAISS 向量库（自动生成）
│   ├── index.faiss
│   └── index.pkl
└── history/          # 对话历史（自动生成）
    ├── default.json
    └── math_class.json
```

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| FastAPI | 最新 | 高性能 Web 框架 |
| LangChain | 最新 | LLM 应用开发框架 |
| LangChain OpenAI | 最新 | OpenAI 兼容接口 |
| LangChain Community | 最新 | 第三方集成组件 |
| FAISS | 最新 | 开源向量数据库 |
| Pydantic | 最新 | 数据校验和序列化 |
| Uvicorn | 最新 | ASGI 服务器 |

## 工作原理

### RAG 流程

1. **文档加载**：从 `data/knowledge_base` 目录加载所有支持的文档格式
2. **文档切分**：将长文档切分为固定大小的文本块（500字符），保留重叠部分
3. **向量化**：使用 `text-embedding-v4` 模型将文本块转换为向量
4. **向量存储**：使用 FAISS 构建向量索引并保存到本地
5. **检索**：用户提问时，将问题向量化后在向量库中检索最相关的 3 个文本块
6. **生成**：将检索到的上下文和历史对话传入大语言模型生成回答
7. **保存**：将对话历史保存到 JSON 文件，支持上下文记忆

### Agent 流程

1. **用户输入**：接收用户的自然语言请求
2. **工具选择**：Agent 根据系统提示词和用户输入，判断是否需要调用工具
3. **工具执行**：调用相应的工具函数（如添加作业、查询作业等）
4. **结果汇总**：将工具执行结果汇总后，生成自然语言回答
5. **返回回答**：将回答返回给用户

## 注意事项

1. **API Key 安全**：请妥善保管 API Key，不要硬编码到代码中，使用环境变量
2. **知识库更新**：添加新文档后需调用 `/api/rag/init-knowledge-base` 或 `/api/upload/file-to-knowledge` 重新构建向量库
3. **文档格式**：支持 txt、pdf、docx 格式，其他格式需要扩展 `document_operation.py`
4. **向量库持久化**：向量库保存在 `data/vector_store`，删除后需重新构建

## 接口文档

完整的 API 接口文档请参考：[接口文档.md](接口文档.md)

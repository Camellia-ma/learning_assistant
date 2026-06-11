# AI 学习助手后端系统

基于 FastAPI + RAG（Retrieval-Augmented Generation）+ LangChain 的智能学习助手后端服务。

## 项目架构

```
learning_assistant/
├── app/                              # 应用主目录
│   ├── __init__.py                   # 包初始化
│   ├── config.py                     # 配置常量定义
│   ├── main.py                       # FastAPI 主入口
│   ├── api/                          # API 控制层
│   │   ├── __init__.py
│   │   ├── agent/                    # Agent 模块（预留）
│   │   │   └── __init__.py
│   │   └── rag/                      # RAG 模块
│   │       ├── __init__.py
│   │       ├── controller.py         # RAG API 路由控制器
│   │       └── result.py             # 请求/响应数据模型
│   └── services/                     # 业务服务层
│       ├── __init__.py
│       └── ai/                       # AI 服务模块
│           ├── __init__.py
│           ├── agent/                # Agent 服务（预留）
│           │   ├── __init__.py
│           │   └── tools.py          # Agent 工具定义
│           └── rag/                  # RAG 核心服务
│               ├── __init__.py
│               ├── RAG.py            # RAG 核心类
│               ├── document_operation.py  # 文档操作工具
│               ├── history_message_manage.py  # 历史消息管理
│               └── model_config.py   # 模型配置
├── data/                             # 数据目录（运行时自动创建）
│   ├── knowledge_base/               # 知识库文档目录
│   ├── vector_store/                 # 向量库存储目录
│   └── history/                      # RAG对话历史存储目录
├── requirements.txt                  # 项目依赖
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
| `EMBEDDING_MODEL` | `text-embedding-v4` | 文本向量化模型 |

### 3. RAG API 控制器 (`app/api/rag/controller.py`)

**功能说明**：定义 RAG 相关的 RESTful API 接口，处理 HTTP 请求和响应。

**API 接口**：

| 接口路径 | HTTP 方法 | 功能 |
|----------|----------|------|
| `/api/rag/init-knowledge-base` | POST | 初始化知识库，扫描文档并构建向量索引 |
| `/api/rag/chat` | POST | 基于知识库的问答接口，接收问题返回 AI 回答 |

**关键代码逻辑**：

- `init_knowledge_base()`：调用 `RAG.init_knowledge_base()` 构建知识库，返回处理的文本切片数量
- `rag_chat(payload)`：接收 `ChatRequest`，调用 `RAG.query()` 获取回答，返回 `ChatResponse`

### 4. 数据模型 (`app/api/rag/result.py`)

**功能说明**：使用 Pydantic 定义请求和响应的数据结构，确保数据校验。

**数据模型**：

| 模型类 | 用途 | 字段 |
|--------|------|------|
| `ChatRequest` | 问答请求 | `question`（问题内容）、`chat_name`（对话名称） |
| `ChatResponse` | 问答响应 | `answer`（AI 回答）、`status`（状态，默认为 success） |
| `InitDBResponse` | 初始化响应 | `message`（结果提示信息） |

### 5. RAG 核心类 (`app/services/ai/rag/RAG.py`)

**功能说明**：RAG 系统的核心类，负责文档加载、向量检索、问答生成和历史管理。

**类成员**：

| 成员 | 类型 | 说明 |
|------|------|------|
| `embedding_model` | DashScopeEmbeddings | 文本嵌入模型实例 |
| `model` | ChatOpenAI | 大语言模型实例 |
| `vector_store` | FAISS | 向量库实例（可选，初始化为 None） |

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

### 6. 文档操作工具 (`app/services/ai/rag/document_operation.py`)

**功能说明**：提供文档加载、切分和向量库构建的工具函数。

**函数**：

| 函数 | 功能 | 参数 | 返回值 |
|------|------|------|--------|
| `load_documents()` | 加载知识库目录中的所有文档（支持 txt、pdf、docx） | 无 | 文档列表 `List[Document]` |
| `split_documents(documents)` | 将文档切分为文本块 | `documents`: 文档列表 | 切分后的文本块列表 |
| `build_vector_store(chunks, embedding_model)` | 使用 FAISS 构建向量库并保存到本地 | `chunks`: 文本块列表；`embedding_model`: 嵌入模型 | FAISS 向量库实例 |

**支持的文档类型**：

- `.txt` - 使用 `TextLoader`
- `.pdf` - 使用 `PyPDFLoader`
- `.docx` - 使用 `Docx2txtLoader`

**切分参数**：

- `chunk_size`: 500（每个文本块的字符数）
- `chunk_overlap`: 100（相邻文本块的重叠字符数）

### 7. 历史消息管理 (`app/services/ai/rag/history_message_manage.py`)

**功能说明**：管理对话历史消息，支持从 JSON 文件加载和保存。

**函数**：

| 函数 | 功能 | 参数 | 返回值 |
|------|------|------|--------|
| `ensure_dir()` | 确保历史记录目录存在 | 无 | 无 |
| `get_history_file(file_name)` | 获取历史文件路径（防止目录穿越攻击） | `file_name`: 文件名 | 文件路径 `Path` |
| `load_history_message(file_name)` | 从 JSON 文件加载历史消息 | `file_name`: 文件名 | 消息列表 `List[BaseMessage]` |
| `save_history_message(file_name, history_message)` | 将历史消息保存为 JSON 文件 | `file_name`: 文件名；`history_message`: 消息列表 | 无 |
| `get_history_file_path(file_name)` | 返回历史文件完整路径（调试用） | `file_name`: 文件名 | 文件路径字符串 |

**消息类型**：

- `HumanMessage`: 用户消息
- `AIMessage`: AI 回答消息

### 8. 模型配置 (`app/services/ai/rag/model_config.py`)

**功能说明**：配置和创建 RAG 使用的大语言模型和嵌入模型。

**函数**：

| 函数 | 功能 | 参数 | 返回值 |
|------|------|------|--------|
| `create_rag_model()` | 创建大语言模型实例（使用阿里云百炼） | 无 | `ChatOpenAI` 实例 |
| `create_embedding_model()` | 创建文本嵌入模型实例 | 无 | `DashScopeEmbeddings` 实例 |

**提示词模板**：

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", rag_system_prompt),      # 系统提示词
    MessagesPlaceholder("history"),     # 历史消息占位符
    ("human", "{input}")                # 用户输入占位符
])
```

系统提示词要求助手：
- 专业、严谨
- 基于参考资料回答
- 不知道就说不知道，不要瞎编
- 逻辑清晰、分条理

### 9. Agent 工具模块 (`app/services/ai/agent/tools.py`)

**功能说明**：预留的 Agent 工具定义模块（当前为空，用于未来扩展）。

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

### 2. 问答接口

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

## 注意事项

1. **API Key 安全**：请妥善保管 API Key，不要硬编码到代码中，使用环境变量
2. **知识库更新**：添加新文档后需调用 `/api/rag/init-knowledge-base` 重新构建向量库
3. **文档格式**：支持 txt、pdf、docx 格式，其他格式需要扩展 `document_operation.py`
4. **向量库持久化**：向量库保存在 `data/vector_store`，删除后需重新构建

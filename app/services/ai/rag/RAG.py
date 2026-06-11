# RAG 类
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from app.services.ai.rag.document_operation import load_documents, split_documents, build_vector_store
from app.services.ai.rag.model_config import create_rag_model, create_embedding_model,prompt
import os
# 开源本地向量库
from langchain_community.vectorstores import FAISS

# 获取知识库目录
knowledge_dir = os.path.join(os.path.dirname(__file__), "../../../../data/knowledge_base")
# 本地向量库保存路径
vector_store_dir = os.path.join(os.path.dirname(__file__), "../../../../data/vector_store")

class RAG:
    def __init__(self):
        self.embedding_model = create_embedding_model()      # 文本嵌入模型
        self.model = create_rag_model()    # 对话模型
        self.vector_store = None
        # 初始化时尝试加载本地已有的向量库
        if os.path.exists(vector_store_dir):
            self.vector_store = FAISS.load_local(
                vector_store_dir,
                self.embedding_model,
                allow_dangerous_deserialization=True  # FAISS本地加载安全声明
            )

    """扫描 data/knowledge_base 目录，解析文档并建立向量索引 """
    def init_knowledge_base(self):
        # 检查有没有资料
        if not os.path.exists(knowledge_dir):
            os.makedirs(knowledge_dir)
            return "请先在 data/knowledge_base 放入学习资料"
        # 加载文档
        documents = load_documents()
        # 切分文档
        chunks = split_documents(documents)
        # 构建向量库
        self.vector_store = build_vector_store(chunks,self.embedding_model)
        return f"知识库构建成功，共处理了 {len(chunks)} 个文本切片"

    # 问答函数
    def query(self,user_question:str):

        if not self.vector_store:
            return "系统知识库尚未初始化，请联系老师上传资料。"

        # 将向量库转为检索器 -- 返回最相关的k个文本
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # 组装 RAG 链 (Chain)
        question_answer_chain = create_stuff_documents_chain(self.model, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        # 执行检索并生成回答
        response = rag_chain.invoke({"input": user_question})

        # 返回最终文本回答
        return response["answer"]

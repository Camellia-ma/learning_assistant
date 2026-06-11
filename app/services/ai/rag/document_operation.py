""" 定义文档操作 """

import os
# 目录文档加载器
from langchain_community.document_loaders import DirectoryLoader
# 可根据文档类型导入不同的处理器：如PDF、MD、HTML、WORD等文档处理器
from langchain_community.document_loaders import TextLoader, Docx2txtLoader,PyPDFLoader
# 文档切分器 -- 用于切分文档（大模型不能一次处理太多文字）
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 开源本地向量库
from langchain_community.vectorstores import FAISS

# 加载本地知识库中的文档
def load_documents():
    # 获取知识库目录
    knowledge_dir = os.path.join(os.path.dirname(__file__), "../../../../data/knowledge_base")
    # 针对目录下不同类型的文件使用不同的文档加载器
    txt_loader = DirectoryLoader(knowledge_dir,
                                 glob="**/*.txt",
                                 loader_cls=TextLoader,
                                 loader_kwargs={"encoding": "utf-8"
                                })
    pdf_loader = DirectoryLoader(knowledge_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
    docx_loader = DirectoryLoader(knowledge_dir, glob="**/*.docx", loader_cls=Docx2txtLoader)
    # 汇总文档加载结果
    documents = txt_loader.load() + pdf_loader.load() + docx_loader.load()
    return documents

# 切分文档
def split_documents(documents):
    # 定义切分器（文本块大小，重叠字符数）
    splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
    # 切分并返回结果
    chunks = splitter.split_documents(documents)
    return chunks

# 创建索引器
def build_vector_store(chunks,embedding_model):
    # 本地向量库保存路径
    vector_store_dir = os.path.join(os.path.dirname(__file__), "../../../../data/vector_store")
    # 文本块向量化
    vector_store = FAISS.from_documents(chunks, embedding_model)
    # 保存本地
    vector_store.save_local(vector_store_dir)
    return vector_store
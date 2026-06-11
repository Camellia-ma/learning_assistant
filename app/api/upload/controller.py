""" 文件上传 API 控制路由 """
from fastapi import APIRouter, HTTPException, status, File, UploadFile
from app.api.upload.result import UploadResponse, KnowledgeFileResponse
from app.services.ai.rag.RAG import RAG, knowledge_dir
import os

router = APIRouter(prefix="/upload", tags=["文件上传"])

RAGBot = RAG()

ALLOWED_EXTENSIONS = {".txt", ".docx", ".pdf"}


def allowed_file(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/file", response_model=UploadResponse, status_code=status.HTTP_200_OK)
async def upload_file(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请选择要上传的文件"
        )

    uploaded_files = []
    for file in files:
        if not allowed_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件类型不支持: {file.filename}。仅支持 txt、docx、pdf 格式"
            )

        try:
            file_path = os.path.join(knowledge_dir, file.filename)
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            uploaded_files.append(file.filename)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"文件 {file.filename} 上传失败: {str(e)}"
            )

    return UploadResponse(
        message=f"成功上传 {len(uploaded_files)} 个文件",
        file_names=uploaded_files
    )


@router.post("/file-to-knowledge", response_model=UploadResponse, status_code=status.HTTP_200_OK)
async def upload_file_to_knowledge(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请选择要上传的文件"
        )

    uploaded_files = []
    for file in files:
        if not allowed_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件类型不支持: {file.filename}。仅支持 txt、docx、pdf 格式"
            )

        try:
            file_path = os.path.join(knowledge_dir, file.filename)
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            uploaded_files.append(file.filename)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"文件 {file.filename} 上传失败: {str(e)}"
            )

    try:
        init_result = RAGBot.init_knowledge_base()
        return UploadResponse(
            message=f"{init_result}，成功上传 {len(uploaded_files)} 个文件",
            file_names=uploaded_files
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"知识库初始化失败: {str(e)}"
        )


@router.get("/knowledge-files", response_model=KnowledgeFileResponse, status_code=status.HTTP_200_OK)
async def get_knowledge_files():
    try:
        if not os.path.exists(knowledge_dir):
            os.makedirs(knowledge_dir)
            return KnowledgeFileResponse(file_names=[])

        files = [f for f in os.listdir(knowledge_dir) if allowed_file(f)]
        return KnowledgeFileResponse(file_names=files)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取知识库文件列表失败: {str(e)}"
        )


@router.delete("/knowledge-file/{filename}", status_code=status.HTTP_200_OK)
async def delete_knowledge_file(filename: str):
    if not allowed_file(filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件类型不支持"
        )

    file_path = os.path.join(knowledge_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"文件不存在: {filename}"
        )

    try:
        os.remove(file_path)
        RAGBot.init_knowledge_base()
        return {"message": f"文件 {filename} 删除成功，知识库已更新"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除文件失败: {str(e)}"
        )
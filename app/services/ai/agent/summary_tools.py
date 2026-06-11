""" summary-agent 工具箱 """
from langchain_core.tools import tool
from pathlib import Path
import json

SUMMARY_BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "data" / "summary"
HISTORY_BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "data" / "history"


def ensure_dir():
    SUMMARY_BASE_PATH.mkdir(parents=True, exist_ok=True)
    HISTORY_BASE_PATH.mkdir(parents=True, exist_ok=True)


@tool
def load_chat_history(chat_name: str) -> str:
    """
    加载指定对话名称的历史消息
    :param chat_name: 对话名称（不带.json扩展名）
    :return: 格式化的对话历史文本
    """
    ensure_dir()
    safe_name = Path(chat_name).name
    if not safe_name.endswith('.json'):
        safe_name += '.json'
    history_file = HISTORY_BASE_PATH / safe_name
    
    if not history_file.exists():
        return f"对话 '{chat_name}' 不存在"
    
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        history_text = []
        for i, msg in enumerate(data, 1):
            role = "学生" if msg.get("type") == "human" else "AI助手"
            content = msg.get("content", "")
            history_text.append(f"【{role}】\n{content}\n")
        
        return "\n".join(history_text)
    except Exception as e:
        return f"加载对话历史失败: {str(e)}"


@tool
def save_summary(summary_content: str, file_name: str) -> str:
    """
    将总结内容保存为 Markdown 文件
    :param summary_content: 总结内容（Markdown格式）
    :param file_name: 文件名（不带.md扩展名，默认为summary）
    :return: 保存结果信息
    """
    ensure_dir()
    safe_name = Path(file_name).name
    if not safe_name.endswith('.md'):
        safe_name += '.md'
    summary_file = SUMMARY_BASE_PATH / safe_name
    
    try:
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary_content)
        return f"总结已成功保存到: {summary_file}"
    except Exception as e:
        return f"保存总结失败: {str(e)}"


@tool
def get_all_chat_names() -> str:
    """
    获取所有可用的对话名称列表
    :return: 对话名称列表（换行分隔）
    """
    ensure_dir()
    chat_names = []
    for file in HISTORY_BASE_PATH.glob("*.json"):
        chat_names.append(file.stem)
    
    if not chat_names:
        return "暂无对话历史"
    
    return "\n".join(chat_names)
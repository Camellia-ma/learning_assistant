""" 历史消息管理 -- json格式"""
import os
import json
from pathlib import Path
from typing import List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

# 使用 pathlib 更安全、现代
HISTORY_BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "data" / "history"


def ensure_dir():
    """确保历史记录目录存在"""
    HISTORY_BASE_PATH.mkdir(parents=True, exist_ok=True)


def get_history_file(file_name: str) -> Path:
    """获取历史文件路径，并防止目录穿越"""
    # 清理文件名，防止安全问题
    safe_name = os.path.basename(file_name)
    if not safe_name.endswith('.json'):
        safe_name += '.json'
    return HISTORY_BASE_PATH / safe_name


def load_history_message(file_name: str) -> List[BaseMessage]:
    """从 JSON 文件加载历史消息"""
    ensure_dir()
    history_file = get_history_file(file_name)

    if not history_file.exists():
        return []

    try:
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        history = []
        for msg in data:
            if msg.get("type") == "human":
                history.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("type") == "ai":
                history.append(AIMessage(content=msg.get("content", "")))
            # 可后续扩展其他类型如 SystemMessage 等
        return history
    except (json.JSONDecodeError, IOError, Exception) as e:
        print(f"加载历史记录失败 {history_file}: {e}")
        return []


def save_history_message(file_name: str, history_message: List[BaseMessage]):
    """将历史消息保存为 JSON 文件"""
    ensure_dir()
    history_file = get_history_file(file_name)

    data = []
    for msg in history_message:
        if isinstance(msg, HumanMessage):
            data.append({
                "type": "human",
                "content": msg.content
            })
        elif isinstance(msg, AIMessage):
            data.append({
                "type": "ai",
                "content": msg.content
            })
        # 其他类型消息可在此扩展

    try:
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存历史记录失败 {history_file}: {e}")



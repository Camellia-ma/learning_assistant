"""作业事务管理"""

import json
from datetime import datetime
from pathlib import Path

# 确定作业的存放位置：严格对应规划文档的 data/homework/homework.json
HOMEWORK_PATH = Path(__file__).resolve().parent.parent.parent.parent / "data" / "homework" / "homework.json"

"""确保作业目录存在，并初始化空的 JSON 文件"""
def ensure_dir():
    homework_dir = HOMEWORK_PATH.parent
    homework_dir.mkdir(parents=True, exist_ok=True)
    # 如果文件不存在，初始化为一个空列表的 JSON
    if not HOMEWORK_PATH.exists():
        with open(HOMEWORK_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

"""从 JSON 文件加载所有作业数据"""
def load_homework() -> list:
    ensure_dir()
    try:
        with open(HOMEWORK_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # 如果文件不幸损坏或为空，返回空列表防止系统崩溃
        return []

"""将作业数据完整写入 JSON 文件"""
def save_homework(homework: list):
    ensure_dir()
    with open(HOMEWORK_PATH, "w", encoding="utf-8") as f:
        json.dump(homework, f, ensure_ascii=False, indent=4)

"""
    筛选出所有未完成的作业（状态为 pending 或 doing 的作业）
    :param homework: 传入的作业列表
    :return: 过滤后的未完成作业列表
"""
def get_not_done_homework(homework: list) -> list:
    return [item for item in homework if item.get("status") == "pending"]


"""新增作业并自动计算 ID 与创建时间"""
def add_homework(title: str, subject: str, description: str, deadline: str) -> dict:
    homework_list = load_homework()
    # 自动生成自增 ID
    next_id = max([item.get("id", 0) for item in homework_list], default=0) + 1
    new_item = {
        "id": next_id,
        "title": title,
        "subject": subject,
        "description": description,
        "deadline": deadline,
        "status": "pending",  # 默认状态
        "created_at": datetime.now().isoformat()  # 生成标准的 ISO 时间字符串
    }

    homework_list.append(new_item)
    save_homework(homework_list)
    return new_item

"""根据 ID 更新作业状态"""
def update_homework_status(homework_id: int, status: str) -> bool:
    if status not in ["pending", "completed"]:
        return False

    homework_list = load_homework()
    for item in homework_list:
        if item.get("id") == homework_id:
            item["status"] = status
            save_homework(homework_list)
            return True
    return False

""" 将作业列表转换为字符串 """
def format_homework_list(homework: list) -> str:
    """将作业列表转化字符串"""
    if not homework:
        return "当前作业列表为空。"

    status_mapping = {
        "pending": "未开始",
        "completed": "已完成"
    }

    lines = []
    for item in homework:
        # 使用 .get() 并提供默认值，防止由于大模型误填数据导致系统崩溃
        line = (
            f"作业ID: {item.get('id', '未知')}\n"
            f"学科: 【{item.get('subject', '未分类')}】\n"
            f"标题: {item.get('title', '无标题')}\n"
            f"要求: {item.get('description', '无明确要求')}\n"
            f"截止日期: {item.get('deadline', '未设置')}\n"
            f"当前状态: {status_mapping.get(item.get('status'), '未知')}\n"
            f"---"
        )
        lines.append(line)
    return "\n".join(lines)
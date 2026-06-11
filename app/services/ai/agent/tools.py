""" homework-agent 工具箱 """

""" 
Agent 工具箱定义 (app/services/ai/agent/tools.py)
"""
from langchain_core.tools import tool
from app.services.homework.homework_services import *
from datetime import datetime

@tool
def add_new_homework_tool(title: str, subject: str, description: str, deadline: str) -> str:
    """
    当用户想要『手动添加作业』、『新增一项任务』、『布置新作业』时，调用此工具。
    新作业被添加后，其默认状态将自动设为 'pending'（未开始）。

    Args:
        title (str): 作业的简短标题，例如 "数学课后习题"、"语文作文"
        subject (str): 作业所属的学科分类，例如 "数学"、"语文"、"英语"、"物理" 等
        description (str): 作业的具体要求和详细描述
        deadline (str): 截止日期，必须是格式为 'YYYY-MM-DD' 的字符串（例如 '2026-06-20'）

    Returns:
        str: 提示作业是否成功添加的确认消息
    """
    new_item = add_homework(
        title=title,
        subject=subject,
        description=description,
        deadline=deadline
    )
    return f" 成功添加作业！[ID: {new_item['id']}] 【{new_item['subject']}】{new_item['title']}，截止日期：{new_item['deadline']}。"


@tool
def get_all_homework_tool() -> str:
    """
    当用户想要查看、查询、列出『全部作业』、『所有作业』、『作业清单』时，调用此工具。
    包含所有已经完成和未完成的作业。
    不需要任何输入参数。返回包含所有作业详细信息的排版字符串。
    """
    homework_data = load_homework()
    return format_homework_list(homework_data)


@tool
def get_pending_homework_tool() -> str:
    """
    当用户问到『还有哪些作业没做』、『还有什么作业没完成』、『查询剩下的作业』、『有什么任务』时，调用此工具。
    专门用来筛选状态为 'pending'（未开始）的作业。
    不需要任何输入参数。返回未完成作业的排版字符串。
    """
    homework_data = load_homework()
    not_done_list = get_not_done_homework(homework_data)
    return format_homework_list(not_done_list)


@tool
def update_homework_status_tool(homework_id: int, status: str) -> str:
    """
    当用户想要修改作业状态、标记作业完成情况时调用此工具。
    例如：『把数学作业改为已完成』、『英语作业做完了』。

    Args:
        homework_id (int): 想要修改的作业对应的唯一整数 ID
        status (str): 目标状态，必须是且只能是以下两个字符串之一:
                      - 'pending' (表示未开始)
                      - 'completed' (表示已完成、做完了)

    Returns:
        str: 状态修改结果的提示语
    """
    # 严格限制参数
    if status not in ["pending", "completed"]:
        return f"状态修改失败：输入的状态值 '{status}' 不合法。系统仅支持 'pending' (未开始) 或 'completed' (已完成)。"

    success = update_homework_status(homework_id=homework_id, status=status)

    if success:
        status_text = "未开始" if status == "pending" else "已完成"
        return f" 状态更新成功！作业 [ID: {homework_id}] 的状态已变更为【{status_text}】。"
    else:
        return f"未找到 ID 为 {homework_id} 的作业，请先确认作业 ID 是否正确。"

@tool
def get_now_time_tool() -> str:
    """
        获取当前系统时间
        agent无法获取时间 -- 需要提醒它获取当前时间
    """
    now = datetime.now()
    # 自定义格式
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    return time
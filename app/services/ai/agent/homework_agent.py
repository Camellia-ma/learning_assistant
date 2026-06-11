""" 作业处理agent """
from typing import List, Any
from langchain.agents import create_agent
from app.services.ai.agent.model_config import *

# 导入工具箱
from app.services.ai.agent.tools import (
    add_new_homework_tool,
    get_all_homework_tool,
    get_pending_homework_tool,
    update_homework_status_tool,
    get_now_time_tool
)


class HomeworkAgentService:
    def __init__(self):
        # 收集并打包所有工具
        self.tools = [
            add_new_homework_tool,
            get_all_homework_tool,
            get_pending_homework_tool,
            update_homework_status_tool,
            get_now_time_tool
        ]
        # 设置模型
        self.model = agent_model

        # 构建 Agent 的系统提示词 (System Prompt)
        self.system_prompt = homework_agent_prompt
        # 构建agent
        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_prompt
        )

    def run(self, user_input: str) -> str:
        """
        运行 Agent 响应用户提问
        """
        messages = []
        messages.append({"role": "user", "content": user_input})
        response = self.agent.invoke({"messages": messages})

        if isinstance(response, dict):
            if "output" in response:
                return response["output"]
            elif "messages" in response and response["messages"]:
                last_msg = response["messages"][-1]
                if hasattr(last_msg, 'content'):
                    content = last_msg.content
                    if content:
                        return content
                    else:
                        return "抱歉，我刚刚走神了，没能处理您的请求。"
                elif isinstance(last_msg, dict) and "content" in last_msg:
                    return last_msg["content"]
                else:
                    return str(last_msg)
            else:
                return "抱歉，我刚刚走神了，没能处理您的请求。"
        elif hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
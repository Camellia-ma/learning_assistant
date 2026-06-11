""" 对话总结 agent """
from langchain.agents import create_agent
from app.services.ai.agent.model_config import *
from app.services.ai.agent.summary_tools import (
    save_summary,
    load_chat_history,
    get_all_chat_names
)


class SummaryAgentService:
    def __init__(self):
        self.tools = [
            get_all_chat_names,
            load_chat_history,
            save_summary,
        ]
        self.model = agent_model
        self.system_prompt = summary_agent_prompt
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
"""
Homework Agent 模块自动化与交互式集成测试脚本 (test_agent_flow.py)
"""
import os
import sys
import json
from pathlib import Path

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.ai.agent.homework_agent import HomeworkAgentService
    from app.services.homework.homework_services import HOMEWORK_PATH, save_homework
except ImportError as e:
    print(f"导入失败，请检查目录结构是否正确。错误信息: {e}")
    sys.exit(1)


def reset_test_database():
    """测试前置动作：重置测试数据库，保证测试结果可预测"""
    print("\n正在初始化/重置测试数据库...")
    save_homework([])  # 清空旧数据
    print("数据库已清空")


def run_automated_tests(agent: HomeworkAgentService):
    """运行预设的自动化黄金用例，检测 Agent 核心能力"""
    print("\n" + "=" * 20 + " 开始自动化核心能力测试 " + "=" * 20)

    # -----------------------------------------------------------------
    # 用例 1: 测试自然语言提取、工具触发与模糊日期换算
    # -----------------------------------------------------------------
    print("\n[测试用例 1]意图：添加作业 | 预期行为：触发 add_new_homework_tool 并自动推算截止日期")
    test_input_1 = "帮我记一下，老师布置了数学作业，要求完成课后习题1到10道，下周一之前要交。"
    print(f"学生输入: '{test_input_1}'")

    response_1 = agent.run(test_input_1)
    print(f"Agent回复: \n{response_1}")

    # 验证底层的 JSON 变化
    with open(HOMEWORK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if data:
        added_item = data[0]
        print(
            f"底层JSON验证成功! 成功写入 ID: {added_item['id']} | 截止日期自动换算结果: {added_item['deadline']} | 状态: {added_item['status']}")
    else:
        print("错误：底层 JSON 没有写入任何数据！")

    # -----------------------------------------------------------------
    # 用例 2: 测试条件过滤查询（查询未完成）
    # -----------------------------------------------------------------
    print("\n[测试用例 2] 意图：查询未完成作业 | 预期行为：触发 get_pending_homework_tool")
    test_input_2 = "我还有什么作业没做完吗？"
    print(f"学生输入: '{test_input_2}'")

    response_2 = agent.run(test_input_2)
    print(f"Agent回复: \n{response_2}")

    # -----------------------------------------------------------------
    # 用例 3: 测试状态变更控制（联动修改）
    # -----------------------------------------------------------------
    print(
        "\n[测试用例 3] 意图：修改作业状态 | 预期行为：自动推断 ID 并触发 update_homework_status_tool，将状态改为 completed")
    test_input_3 = "刚刚那个数学作业我已经写完了，帮我改一下状态。"
    print(f"学生输入: '{test_input_3}'")

    response_3 = agent.run(test_input_3)
    print(f"Agent回复: \n{response_3}")

    # 验证底层状态是否真的变为 completed
    with open(HOMEWORK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if data and data[0]['status'] == 'completed':
        print("底层JSON验证成功! 该作业状态已成功变更为 'completed'")
    else:
        print(f"错误：底层 JSON 状态未发生改变，当前状态为: {data[0]['status'] if data else '无数据'}")

    print("\n" + "=" * 20 + " 自动化核心能力测试结束 " + "=" * 20)


def run_interactive_loop(agent: HomeworkAgentService):
    """切入实时交互模式，允许手动自由对话"""
    print("\n" + "-" * 3 + " 进入实时自由交互模式 " + "-" * 3)
    print("你可以输入任何与作业相关的口语命令（例如：'再帮我加个英语作业'、'看下全部清单' 等）。")
    print("提示：输入 'exit' 或 'quit' 可退出测试。")
    print("-" * 60)

    while True:
        try:
            user_input = input("\n学生: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("退出测试脚本，测试结束。")
                break

            print("Agent 思考并执行中...")
            reply = agent.run(user_input)
            print(f"\nAI助手:\n{reply}")
            print("-" * 40)
        except KeyboardInterrupt:
            print("\n强行退出测试。")
            break
        except Exception as e:
            print(f"运行中发生预期外的异常: {e}")


if __name__ == "__main__":
    print("正在启动作业管理 Agent 测试套件...")

    # 检查环境变量
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("警告: 未检测到 DASHSCOPE_API_KEY 环境变量，请确保 app/config.py 中已硬编码或已正确加载。")

    # 初始化 Agent 服务
    try:
        homework_agent = HomeworkAgentService()
        print("Agent 模型与工具链成功绑定。")
    except Exception as e:
        print(f"Agent 初始化发生致命错误: {e}")
        sys.exit(1)

    # 1. 重置数据库
    reset_test_database()

    # 2. 执行全自动功能流水线测试
    run_automated_tests(homework_agent)

    # 3. 切换至手动聊天模式
    run_interactive_loop(homework_agent)
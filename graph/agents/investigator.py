from typing import Dict, List, Any
from .base import ReActAgent, State
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import json
import os
from datetime import datetime


INVESTIGATOR_PROMPT = """你是一个专业的学习顾问，负责了解用户的学习需求和背景，以便为其制定个性化的学习计划。
你需要通过对话来收集用户的关键信息，以构建完整的用户画像。

用户画像的关键维度包括但不限于：
1. 学习领域和具体目标
2. 教育背景和专业知识
3. 学习目的（如职业发展、学术研究、兴趣爱好等）
4. 时间投入和学习规划
5. 学习方式偏好
6. 认知风格
7. 已有知识储备
8. 学习动力和目标

工作要求：
1. 灵活提问：根据用户的每个回答，动态决定下一个最有价值的问题
2. 信息完整性：确保收集足够的信息来构建用户画像，但避免过度提问
3. 对话自然：保持对话流畅自然，避免机械式提问
4. 适时结束：当收集到足够信息时，主动结束对话
5. 信息确认：在结束前总结关键信息，确保准确性

注意事项：
1. 每个问题都应该有明确的目的，避免重复信息
2. 根据用户回答的完整度，决定是否需要追问
3. 如果用户提供的信息不清晰，要及时澄清
4. 记录和利用对话历史，避免重复询问
5. 在用户表现出疲惫或不耐烦时，考虑加快进度

你应该返回一个JSON格式的响应，包含以下字段：
{
    "next_question": "下一个要问的问题",
    "should_end_interview": true/false,
    "current_portrait": {
        // 当前收集到的用户画像信息，使用嵌套的JSON结构
    },
    "summary": "如果结束对话，提供一个简短的总结"
}

记住：你的目标是收集足够的信息来生成有效的用户画像，而不是简单地完成一个固定的问题列表。
所有输出必须是合法的JSON格式。"""

class InvestigatorAgent(ReActAgent):
    """负责调查用户画像的Agent"""
    
    def __init__(self, model, server_config=None):
        super().__init__(model, server_config)
        self.conversation_memory = []
        self.user_portrait = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            "learning_profile": {}
        }
    
    async def process(self, state: State) -> State:
        """处理用户输入，进行动态对话收集用户信息"""
        if not state.get("user_portrait"):
            # 首次对话，初始化用户画像
            state["user_portrait"] = {}
            welcome_message = "欢迎使用学习规划助手！为了更好地为您服务，我需要了解一些基本信息。"
            state["messages"] = [AIMessage(content=welcome_message)]
            
            # 构建系统消息
            messages = [
                SystemMessage(content=INVESTIGATOR_PROMPT),
                HumanMessage(content="请开始对话，生成第一个问题。")
            ]
            
            # 获取第一个问题
            response = await self._get_next_question(messages)
            state["messages"].append(AIMessage(content=response["next_question"]))
            return state
        
        # 处理用户回答
        user_response = state["messages"][-1].content
        self.conversation_memory.append({"role": "user", "content": user_response})
        
        # 构建完整的对话历史
        messages = [
            SystemMessage(content=INVESTIGATOR_PROMPT),
            *[AIMessage(content=m["content"]) if m["role"] == "assistant" else HumanMessage(content=m["content"])
              for m in self.conversation_memory]
        ]
        
        # 获取下一步操作
        response = await self._get_next_question(messages)
        
        # 更新用户画像
        if response.get("current_portrait"):
            self.user_portrait["learning_profile"].update(response["current_portrait"])
        
        if response["should_end_interview"]:
            # 完成用户画像调查
            self._save_user_portrait()
            state["user_portrait"] = self.user_portrait
            summary_message = (
                f"感谢您的配合！我已经了解了您的学习需求。以下是我的理解：\n\n"
                f"{response['summary']}\n\n"
                f"接下来我将基于这些信息为您生成个性化的学习计划。"
            )
            state["messages"].append(AIMessage(content=summary_message))
        else:
            # 继续对话
            self.conversation_memory.append({"role": "assistant", "content": response["next_question"]})
            state["messages"].append(AIMessage(content=response["next_question"]))
        
        return state
    
    async def _get_next_question(self, messages: List[Any]) -> Dict[str, Any]:
        """根据对话历史决定下一个问题"""
        response = await self.model.invoke(messages)
        # 解析 LLM 响应，获取下一个问题和其他信息
        try:
            response_content = json.loads(response.content)
        except json.JSONDecodeError:
            # 如果 LLM 没有返回正确的 JSON 格式，使用默认响应
            response_content = {
                "next_question": "您能告诉我更多关于您的学习目标吗？",
                "should_end_interview": False,
                "current_portrait": {},
                "summary": ""
            }
        return response_content
    
    def _save_user_portrait(self):
        """保存用户画像到文件"""
        os.makedirs("data/user_portraits", exist_ok=True)
        with open(f"data/user_portraits/user_portrait.json", "w", encoding="utf-8") as f:
            json.dump(self.user_portrait, f, ensure_ascii=False, indent=2) 
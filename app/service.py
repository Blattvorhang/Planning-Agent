from graph.workflow.graph_builder import build_graph, State
import asyncio
import time
from collections import defaultdict


class LearningService:
    def __init__(self, session_timeout=1800):  # 默认会话超时时间30分钟
        self.graph = None
        self.agents = []
        # 存储所有用户会话的字典，键为会话ID
        self.sessions = {}
        self.session_timeout = session_timeout
        self.last_cleanup = time.time()
        self.cleanup_interval = 300  # 每5分钟清理一次过期会话

    async def startup(self):
        self.graph, self.agents = await build_graph()

    async def shutdown(self):
        # 清理 client 连接
        await asyncio.gather(*(agent.close() for agent in self.agents))
        
    def _cleanup_expired_sessions(self):
        """清理过期的会话以防止内存泄漏"""
        current_time = time.time()
        # 只在特定间隔时间执行清理，避免每次请求都执行
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
            
        expired_sessions = []
        for session_id, session_data in self.sessions.items():
            if current_time - session_data["last_access"] > self.session_timeout:
                expired_sessions.append(session_id)
                
        for session_id in expired_sessions:
            del self.sessions[session_id]
            
        self.last_cleanup = current_time

    async def run(self, user_prompt: str, session_id: str = None) -> dict:
        # 如果没有提供会话ID，则使用默认值
        if not session_id:
            session_id = "default"
            
        # 执行会话清理
        self._cleanup_expired_sessions()
        
        # 获取现有状态或创建新状态
        if session_id in self.sessions:
            # 更新现有状态
            current_state = self.sessions[session_id]["state"]
            current_state["user_input"].append(user_prompt)
        else:
            # 创建新的会话初始状态
            current_state = {
                "user_input": [user_prompt],
                "learning_goal": [],
                "feedback": [],
                "learning_plan": [],
                "evaluation_result": [],
                "exam_questions": [],
            }
        
        config = {"configurable": {"thread_id": session_id}}
        final_state = None
        
        async for state in self.graph.astream(
            current_state,
            config,
            stream_mode="values"
        ):
            final_state = state
            
        # 更新会话状态
        self.sessions[session_id] = {
            "state": final_state,
            "last_access": time.time()
        }

        return final_state
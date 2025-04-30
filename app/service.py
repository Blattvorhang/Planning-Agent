from .graph_builder import build_graph, State
import asyncio


class LearningService:
    def __init__(self):
        self.graph = None
        self.agents = []

    async def startup(self):
        self.graph, self.agents = await build_graph()

    async def shutdown(self):
        # 清理 client 连接
        await asyncio.gather(*(agent.close() for agent in self.agents))

    async def run(self, user_prompt: str) -> dict:
        init_state: State = {
            "user_input": [user_prompt],
            "learning_goal": [],
            "feedback": [],
            "learning_plan": [],
            "evaluation_result": [],
            "exam_questions": [],
        }
        config = {"configurable": {"thread_id": "frontend"}}  # 你可以塞前端会话 ID
        final_state = None               # 用来接收最后一次产出的 state
        async for state in self.graph.astream(
            init_state,
            config,
            stream_mode="values"         # 👈 每一步执行完返回“整个 state”
        ):
            final_state = state          # 每次循环都会覆盖，最后一次就是终态

        return final_state               # ← 返回真正的终态
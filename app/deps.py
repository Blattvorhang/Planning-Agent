# app/deps.py
from .service import LearningService

svc = LearningService()            # 单例

def get_service() -> LearningService:
    """FastAPI Depends 依赖：返回全局 svc"""
    return svc
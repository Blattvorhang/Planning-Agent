# app/api.py
from fastapi import APIRouter, HTTPException, Depends
import json
import logging

from .models import LearnRequest, LearnResponse
from .deps import get_service    # 引入依赖
from .deps import svc            # 可选：如果确实想直接用实例也行
from .question import ExamQuestions

router = APIRouter()
logger = logging.getLogger(__name__)


def latest_content(msg_list):
    """取列表最后一条消息的 content。列表为空则返回空串。"""
    if not msg_list:
        return ""
    msg = msg_list[-1]
    return msg.content


@router.post("/learn", response_model=LearnResponse)
async def learn(
    req: LearnRequest,
    svc = Depends(get_service),      # 注入 svc
):
    try:
        # 将会话 ID 传递给 service.run 方法
        state = await svc.run(req.prompt, req.session_id)

        learning_goal   = latest_content(state["learning_goal"])
        answer          = latest_content(state["learning_plan"])      # 最后一条计划视为最终回答
        exam_questions  = latest_content(state["exam_questions"])
        
        # 将 exam_questions 转换为 ExamQuestions 对象
        try:
            exam_questions_obj = ExamQuestions(**json.loads(exam_questions))
        except Exception as e:
            logger.error(f"Failed to parse exam questions JSON: {e}")
            raise HTTPException(500, str(e))

        logger.info(f"--------------------------------")
        logger.info(f"learning_goal: \n{learning_goal}")
        logger.info(f"answer: \n{answer}")
        logger.info(f"exam_questions: \n{exam_questions}")
        logger.info(f"--------------------------------")
        
        return LearnResponse(
            learning_goal=learning_goal,
            answer=answer,
            exam_questions=exam_questions_obj,
            session_id=req.session_id,  # 在响应中返回会话 ID
        )
    except Exception as e:
        raise HTTPException(500, str(e))
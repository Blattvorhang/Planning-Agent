# app/api.py
from fastapi import APIRouter, HTTPException, Depends
from .models import LearnRequest, LearnResponse
from .deps import get_service    # 引入依赖
from .deps import svc            # 可选：如果确实想直接用实例也行


router = APIRouter()

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
        state = await svc.run(req.prompt)

        learning_goal   = latest_content(state["learning_goal"])
        answer          = latest_content(state["learning_plan"])      # 最后一条计划视为最终回答
        exam_question   = latest_content(state["exam_questions"])
        print(f"learning_goal:{learning_goal}")
        print(f"answer:{answer}")
        print(f"exam_question:{exam_question}")
        
        return LearnResponse(
            learning_goal=learning_goal,
            answer=answer,
            exam_questions=exam_question,
        )
    except Exception as e:
        raise HTTPException(500, str(e))
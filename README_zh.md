# Planning Agent

## 项目概述

Planning-Agent 是一个基于FastAPI的学习规划智能代理系统，主要功能包括：
- 了解用户的基础情况(user_portrait)
- 接收用户的学习请求(prompt)
- 基于用户画像，生成**个性化**的学习方案
  - 生成学习目标(learning_goal)
  - 制定学习计划(learning_plan)
  - 提供测试问题(exam_questions)

## 环境配置
想要克隆这个仓库，需要运行以下命令：
```bash
git clone https://github.com/Blattvorhang/Planning-Agent.git --recursive
```

如果克隆时忘记添加参数 `--recursive` ，需要执行
```bash
git submodule update --init --recursive
```

接下来，安装所需的依赖：
```bash
pip install -r requirements.txt
uv pip install -e "./tools/arxiv-mcp-server/[test]"
```

最终，需要把相应的LLM API key填写到`.env`文件中，格式可以参考[`.env.example`](./.env.example)。

## FastAPI 接口说明

### 核心API

#### 学习规划接口
- 路径: `POST /api/learn`
- 请求体:
  ```json
  {
    "prompt": "学习目标描述"
  }
响应:

json
Apply
{
  "learning_goal": "生成的学习目标",
  "answer": "学习计划",
  "exam_questions": "测试问题"
}
项目结构

```plainText
Planning-Agent/
├── app/
│   ├── api.py        # FastAPI路由定义
│   ├── deps.py       # 依赖注入
│   └── models.py     # 数据模型
├── main.py           # FastAPI应用入口
└── tools/            # 工具集成
```
FastAPI 使用说明
1. 创建FastAPI应用
在main.py中初始化应用：


```python
Apply
from fastapi import FastAPI
from app.api import router as learn_router

app = FastAPI(
    title="Learning Agent Service",
    docs_url="/docs"  # 自动生成API文档
)
app.include_router(learn_router, prefix="/api")
```
2. 定义路由
在app/api.py中定义API端点：


```python
Apply
from fastapi import APIRouter
router = APIRouter()

@router.post("/learn")
async def learn_endpoint(request: LearnRequest):
    # 处理逻辑
    return response
```
3. 运行服务
使用uvicorn运行服务：


```bash
uvicorn main:app --reload
```
访问API文档：


```plainText
http://localhost:8000/docs
```

扩展功能
项目集成了arXiv论文搜索工具(arxiv-mcp-server)，可用于：

搜索学术论文
下载论文内容
分析研究资料
如需使用，请参考tools/arxiv-mcp-server/README.md


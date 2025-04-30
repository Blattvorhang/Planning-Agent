# Planning Agent

[简体中文](./README_zh.md)

## Project Overview

**Planning-Agent** is an intelligent learning planning agent system based on **FastAPI**. Its main functions include:
- Investigating user basic information (user_portrait)
- Receiving user learning requests (prompt)
- Generating **personalized** learning methodology based on user portrait:
  - Generating learning goals (`learning_goal`)
  - Creating learning plans (`learning_plan`)
  - Providing test questions (`exam_questions`)

## Environment Setup
To clone the entire repository, you will need to run the following command:
```bash
git clone https://github.com/Blattvorhang/Planning-Agent.git --recursive
```

If you forgot to add the parameter `--recursive`, you should run
```bash
git submodule update --init --recursive
```

Then install required packages:
```bash
pip install -r requirements.txt
uv pip install -e "./tools/arxiv-mcp-server/[test]"
```

Finally, you need to fill out your personal LLM API key in the `.env` file, as shown in [`.env.example`](./.env.example).

## FastAPI API Description

### Core API

#### Learning Planning Endpoint
- **Path:** `POST /api/learn`
- **Request Body:**
  ```json
  {
    "prompt": "Description of the learning goal"
  }
  ```
- **Response:**
  ```json
  {
    "learning_goal": "Generated learning goal",
    "answer": "Learning plan",
    "exam_questions": "Test questions"
  }
  ```

## Project Structure

```plaintext
Planning-Agent/
├── app/
│   ├── api.py        # FastAPI route definitions
│   ├── deps.py       # Dependency injection
│   └── models.py     # Data models
├── main.py           # Entry point for the FastAPI app
└── tools/            # Tool integrations
```

## FastAPI Usage Guide

### 1. Create the FastAPI Application  
Initialize the app in `main.py`:

```python
from fastapi import FastAPI
from app.api import router as learn_router

app = FastAPI(
    title="Learning Agent Service",
    docs_url="/docs"  # Auto-generated API documentation
)
app.include_router(learn_router, prefix="/api")
```

### 2. Define the Routes  
Define API endpoints in `app/api.py`:

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/learn")
async def learn_endpoint(request: LearnRequest):
    # Processing logic
    return response
```

### 3. Run the Service  
Use `uvicorn` to run the service:

```bash
uvicorn main:app --reload
```

Visit the API documentation at:

```plaintext
http://localhost:8000/docs
```

## Extended Features  
The project integrates with the `arxiv-mcp-server`, a tool for:
- Searching academic papers  
- Downloading paper content  
- Analyzing research materials  

For usage instructions, refer to `tools/arxiv-mcp-server/README.md`.
# main.py
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app import svc, learn_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await svc.startup()                  # 初始化图
    yield
    await svc.shutdown()                 # 释放资源

app = FastAPI(
    title="Learning Agent Service",
    docs_url="/docs",
    lifespan=lifespan,
)
app.include_router(learn_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI
from app.api.routes import agent  

app = FastAPI(
    title="AI Agent API Tester",
    description="LangGraph 기반 API 자동화 테스트",
    version="1.0.0"
)

app.include_router(agent.router, prefix="/api/v1/agent", tags=["AI Test Agent"])
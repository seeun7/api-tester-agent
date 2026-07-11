from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from agent.graph import agent_app  

router = APIRouter()

# 요청 데이터 구조
class AgentRunRequest(BaseModel):
    openapi_spec: str = Field(..., description="테스트할 API의 OpenAPI(Swagger) 명세서 내용")

@router.post("/run")
def run_test_agent(request: AgentRunRequest):
    try:
        # 에이전트에 주입할 초기 상태
        initial_state = {
            "openapi_spec": request.openapi_spec
        }
        # 에이전트 실행 (MVP 단계에서만 동기 방식)
        result = agent_app.invoke(initial_state)
        
        generated_cases = result.get("generated_test_cases", [])
        execution_results = result.get("execution_results", [])
        
        return {
            "status": "success",
            "message": "AI 에이전트 테스트 완료",
            "summary": {
                "total_generated_cases": len(generated_cases),
                "total_executed_cases": len(execution_results),
            },
            "results": execution_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"에이전트 실행 중 오류 발생: {str(e)}")
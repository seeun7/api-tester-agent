from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TestCase(BaseModel):
    endpoint: str = Field(..., description="API 엔드포인트 경로")
    method: str = Field(..., description="HTTP 메서드")
    payload: Optional[Dict[str, Any]] = Field(None, description="요청 Body")
    expected_status: int = Field(..., description="예상 응답 코드")
    description: str = Field(..., description="테스트 목적")
    is_edge_case: bool = Field(..., description="엣지 케이스 여부")

class TestScenario(BaseModel):
    test_cases: List[TestCase]

class TestResult(BaseModel):
    test_case: TestCase
    actual_status: int
    latency_ms: float
    is_passed: bool

class TestState(TypedDict):
    openapi_spec: str
    generated_test_cases: List[TestCase]
    execution_results: List[TestResult]
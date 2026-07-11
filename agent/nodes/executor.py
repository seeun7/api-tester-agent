import httpx
import time
from agent.state import TestState, TestResult

def execute_tests(state: TestState) -> dict:
    """생성된 테스트 케이스를 실제로 실행하고 결과를 기록하는 노드"""
    results = []
    # 테스트 대상 서버의 기본 URL (현재는 로컬 FastAPI 서버 기준)
    base_url = "http://localhost:8000" 
    
    # httpx Client를 사용하여 세션 유지 및 통신
    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        for case in state.get("generated_test_cases", []):
            start_time = time.time()
            actual_status = 500
            error_msg = None
            response_body = None
            
            try:
                # HTTP 메서드에 따른 분기 처리
                if case.method.upper() == "POST":
                    response = client.post(case.endpoint, json=case.payload)
                elif case.method.upper() == "GET":
                    response = client.get(case.endpoint)
                else:
                    continue # MVP에서는 GET, POST만 우선 지원
                
                actual_status = response.status_code
                response_body = response.json() if response.text else None
                
            except httpx.RequestError as e:
                error_msg = f"요청 실패: {str(e)}"
                
            # 응답 시간(ms) 계산
            latency = round((time.time() - start_time) * 1000, 2)
            
            # 예상한 상태 코드와 실제 상태 코드가 일치하는지 확인
            is_passed = (actual_status == case.expected_status)
            
            # 결과 저장
            results.append(TestResult(
                test_case=case,
                actual_status=actual_status,
                latency_ms=latency,
                is_passed=is_passed,
                response_body=response_body,
                error_message=error_msg
            ))
            
    # LangGraph State 업데이트
    return {"execution_results": results}
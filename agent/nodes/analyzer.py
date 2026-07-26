from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from agent.state import TestState

def analyze_results(state: TestState) -> dict: # 테스트 실행 결과를 분석하여 마크다운 형태의 최종 종합 리포트를 생성합니다.
  
    execution_results = state.get("execution_results", [])
    
    # 실패한 케이스만 따로 필터링하여 프롬프트에 강조
    failed_cases = [res for res in execution_results if not res.get("is_passed", False)]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """당신은 시니어 백엔드 QA 엔지니어이자 아키텍트입니다.
제공된 API 테스트 실행 결과를 분석하여 다음 항목이 포함된 마크다운 리포트를 작성하세요:
1. **테스트 요약**: 총 실행 건수, 성공/실패 건수, 평균 지연 시간(Latency)
2. **에러 원인 분석**: 실패한 케이스(예상 상태 코드와 실제 코드가 다르거나 500 에러 발생)의 페이로드와 응답을 대조하여 원인 추론
3. **Self-Healing 제안**: 서버 코드에서 수정해야 할 사항(예: 입력값 검증 로직 추가, 예외 처리 등)에 대한 구체적인 가이드

전문적이고 명확한 어조로 작성하세요."""),
        ("user", "전체 테스트 결과: {results}\n\n실패한 케이스: {failed_cases}")
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm
    
    response = chain.invoke({
        "results": execution_results,
        "failed_cases": failed_cases
    })
    
    # State 업데이트를 위해 딕셔너리 반환
    return {"final_report": response.content}
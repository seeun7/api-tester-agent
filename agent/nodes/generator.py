import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from agent.state import TestState, TestScenario

def generate_test_cases(state: TestState) -> dict:
    """OpenAPI 명세를 읽고 테스트 케이스를 생성하는 노드"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    structured_llm = llm.with_structured_output(TestScenario)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """당신은 백엔드 API QA 엔지니어입니다. 주어진 OpenAPI 명세서를 보고 다음을 생성하세요:
1. 정상적인 요청 2개
2. 예외 처리(400, 422 에러)를 유도하는 엣지 케이스 요청 3개"""),
        ("human", "OpenAPI 명세서:\n{openapi_spec}")
    ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"openapi_spec": state["openapi_spec"]})
    
    # 생성된 케이스를 상태(State)에 업데이트
    return {"generated_test_cases": result.test_cases}
from langgraph.graph import StateGraph, START, END
from agent.state import TestState
from agent.nodes.generator import generate_test_cases
from agent.nodes.executor import execute_tests  # 새로 구현한 모듈 임포트

# 그래프 빌드
workflow = StateGraph(TestState)

# 노드 추가 (이제 dummy 대신 진짜 executor 사용)
workflow.add_node("generator", generate_test_cases)
workflow.add_node("executor", execute_tests)

# 흐름(Edge) 연결
workflow.add_edge(START, "generator")
workflow.add_edge("generator", "executor")
workflow.add_edge("executor", END)

# 에이전트 컴파일
agent_app = workflow.compile()
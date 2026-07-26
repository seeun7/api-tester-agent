from langgraph.graph import StateGraph, START, END
from agent.state import TestState
from agent.nodes.generator import generate_test_cases
from agent.nodes.executor import execute_tests
from agent.nodes.analyzer import analyze_results

# 그래프 빌드
workflow = StateGraph(TestState)

workflow.add_node("generator", generate_test_cases)
workflow.add_node("executor", execute_tests)
workflow.add_node("analyzer", analyze_results)

# Edge 연결
workflow.add_edge("generator", "executor")
workflow.add_edge("executor", "analyzer") 
workflow.add_edge("analyzer", END)

# 에이전트 컴파일
agent_app = workflow.compile()
from langgraph.graph import StateGraph
from .graph_state import GraphState
from .nodes import (
    planner_node,
    executor_node,
    verifier_node,
    check_verification,
)

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("checker", check_verification)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "verifier")
    graph.add_edge("verifier", "checker")

    graph.add_conditional_edges(
        "checker",
        lambda state: state.status,
        {
            "success": None,
            "retry": "planner",
            "failed": None
        }
    )

    return graph.compile()

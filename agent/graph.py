from langgraph.graph import StateGraph
from .graph_state import GraphState
from .nodes import (
    planner_node,
    executor_node,
    verifier_node,
    check_verification,
    end_node,
)

def build_graph():
    graph = StateGraph(GraphState)

    # Add all nodes
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("checker", check_verification)
    graph.add_node("end", end_node)  # terminal node

    # Set entry point
    graph.set_entry_point("planner")

    # Normal edges
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "verifier")
    graph.add_edge("verifier", "checker")

    # Conditional edges from checker
    graph.add_conditional_edges(
        "checker",
        lambda state: state.status,
        {
            "success": "end",   # go to terminal node
            "retry": "planner", # retry planning
            "failed": "end",    # go to terminal node
        }
    )

    # Compile graph
    return graph.compile()

from agent.graph import build_graph
from agent.graph_state import GraphState

graph = build_graph()

def solve(question: str):
    initial_state = GraphState(question=question)
    final_state = graph.invoke(initial_state)

    # Build final user-facing JSON
    result = {
        "answer": (
            final_state.executor_output.get("intermediate_result")
            if final_state.status == "success"
            else "Unable to produce a verified answer."
        ),
        "status": final_state.status,
        "reasoning_visible_to_user": (
            "I solved this by planning, executing, and verifying the result."
            if final_state.status == "success"
            else "The agent attempted multiple verification passes but failed."
        ),
        "metadata": {
            "plan": final_state.plan,
            "checks": [final_state.verification],
            "retries": final_state.retries,
        },
    }

    return result


if __name__ == "__main__":
    while True:
        q = input("\nEnter a question: ")
        print(solve(q))

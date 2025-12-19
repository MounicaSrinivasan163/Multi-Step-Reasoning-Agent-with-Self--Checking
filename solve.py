# solve.py
from agent.graph import build_graph
from agent.graph_state import GraphState

graph = build_graph()

def solve(question: str):
    """
    Solve a question using the multi-step reasoning agent.
    Returns a contract-compliant JSON with answer, status, reasoning, and metadata.
    """

    # 1. Initialize state (GraphState is only for input)
    initial_state = GraphState(question=question)

    # 2. Run graph
    # LangGraph RETURNS AddableValuesDict (dict-like), NOT GraphState
    final_state = graph.invoke(initial_state)

    # 3. Safely extract status
    status = final_state.get("status", "failed")

    # 4. Safely extract answer
    answer = (
        final_state.get("verification", {}).get("final_answer")
        or final_state.get("executor_output", {}).get("intermediate_result")
        or "Unable to produce a verified answer."
    )

    # 5. User-facing reasoning
    reasoning = (
        "I solved this by planning, executing, and verifying the result."
        if status == "success"
        else "The agent attempted multiple verification passes but failed."
    )

    # 6. Final JSON output
    result = {
        "answer": answer,
        "status": status,
        "reasoning_visible_to_user": reasoning,
        "metadata": {
            "plan": final_state.get("plan"),
            "checks": final_state.get("checks", []),
            "retries": final_state.get("retries", 0),
        },
    }

    return result


if __name__ == "__main__":
    while True:
        q = input("\nEnter a question: ")
        print(solve(q))

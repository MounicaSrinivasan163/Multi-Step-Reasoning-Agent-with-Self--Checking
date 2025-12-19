# ------------------ solve.py ------------------
from agent.graph import build_graph
from agent.graph_state import GraphState
import json

graph = build_graph()

def solve(question: str):
    """
    Solve a question using the multi-step reasoning agent.
    Returns a contract-compliant JSON with answer, status, reasoning, and metadata.
    """

    # 1️⃣ Initialize state
    initial_state = GraphState(question=question)

    # 2️⃣ Run the LangGraph pipeline
    final_state = graph.invoke(initial_state)

    # 3️⃣ Extract status safely
    status = final_state.get("status", "failed")

    # 4️⃣ Extract answer safely
    verification = final_state.get("verification", {}) or {}
    executor_output = final_state.get("executor_output", {}) or {}

    answer = (
        verification.get("final_answer")
        or executor_output.get("intermediate_result")
        or "Unable to produce a verified answer."
    )

    # 5️⃣ User-facing reasoning
    reasoning = (
        "I solved this by planning, executing, and verifying the result."
        if status == "success"
        else "The agent attempted multiple verification passes but failed."
    )

    # 6️⃣ Compile final JSON output
    result = {
        "answer": answer,
        "status": status,
        "reasoning_visible_to_user": reasoning,
        "metadata": {
            "plan": final_state.get("plan") or {},
            "checks": final_state.get("checks") or [],
            "verification": verification,
            "executor_output": executor_output,
            "retries": final_state.get("retries", 0),
        },
    }

    return result


if __name__ == "__main__":
    while True:
        q = input("\nEnter a question: ")
        if q.strip():
            output = solve(q)
            print(json.dumps(output, indent=2))
        else:
            print("Please enter a non-empty question.")

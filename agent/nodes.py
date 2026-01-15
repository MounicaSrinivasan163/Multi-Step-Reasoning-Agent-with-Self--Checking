from __future__ import annotations

import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .graph_state import GraphState

# -----------------------------
# Load environment
# -----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found. Create a .env file or set environment variable.")

# -----------------------------
# Load prompts
# -----------------------------
def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

planner_prompt = load_prompt("prompts/planner_prompt.txt")
executor_prompt = load_prompt("prompts/executor_prompt.txt")
verifier_prompt = load_prompt("prompts/verifier_prompt.txt")

# -----------------------------
# Initialize LLM
# -----------------------------
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=OPENAI_API_KEY)

# -----------------------------
# Planner Node
# -----------------------------
def planner_node(state: GraphState) -> GraphState:
    prompt = f"""{planner_prompt}

Question:
{state.question}
"""
    response = llm.invoke(prompt)
    state.plan = json.loads(response.content)
    return state

# -----------------------------
# Executor Node
# -----------------------------
def executor_node(state: GraphState) -> GraphState:
    prompt = f"""{executor_prompt}

Question:
{state.question}

Plan:
{json.dumps(state.plan, indent=2)}
"""
    response = llm.invoke(prompt)
    state.executor_output = json.loads(response.content)
    return state

# -----------------------------
# Verifier Node (general-purpose)
# -----------------------------
def verifier_node(state: GraphState) -> GraphState:
    """
    General-purpose verifier that works across domains.
    Uses:
    1. Structural validation
    2. Constraint checks
    3. Independent LLM re-solve
    4. Consistency analysis
    """
    checks = []
    executor = state.executor_output or {}
    result = executor.get("intermediate_result")

    # 1️⃣ Structural Validation
    structural_pass = result is not None
    checks.append({
        "check_name": "structural_validation",
        "passed": structural_pass,
        "details": "intermediate_result present" if structural_pass else "missing result"
    })
    if not structural_pass:
        state.verification = {"passed": False, "final_answer": None, "checks": checks}
        return state

    # 2️⃣ Constraint Validation (generic)
    constraint_pass = True
    constraint_details = []

    if isinstance(result, (int, float)):
        if result < 0:
            constraint_pass = False
            constraint_details.append("Negative numeric result")
    if isinstance(result, str):
        if "hours" in result and "minutes" in result:
            constraint_details.append("Time format validated")

    checks.append({
        "check_name": "constraint_validation",
        "passed": constraint_pass,
        "details": "; ".join(constraint_details) or "Basic constraints satisfied"
    })

    # 3️⃣ Independent Re-solve (LLM)
    verification_prompt = f"""
You are an independent verifier.
Solve the following question from scratch.
Do NOT use any prior reasoning.
Return only JSON.

Question:
{state.question}

Output format:
{{
  "final_answer": "...",
  "confidence": "high | medium | low"
}}
"""
    try:
        response = llm.invoke(verification_prompt)
        llm_verdict = json.loads(response.content)
        verifier_answer = llm_verdict.get("final_answer")
    except Exception:
        verifier_answer = None

    import re

    def normalize_numeric_answer(value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
    
        matches = re.findall(r"\d+\.?\d*", str(value))
        if not matches:
            return None
    
        return float(matches[0])

    agreement = (
    normalize_numeric_answer(verifier_answer)
    == normalize_numeric_answer(result) )


    checks.append({
        "check_name": "independent_resolve",
        "passed": agreement,
        "details": f"Verifier answer = {verifier_answer}"
    })

    # 4️⃣ Final Decision
    passed = structural_pass and constraint_pass and agreement
    state.verification = {
        "passed": passed,
        "final_answer": result,
        "checks": checks
    }
    return state

# -----------------------------
# Retry / Checker Node
# -----------------------------
def check_verification(state: GraphState) -> GraphState:
    passed = state.verification.get("passed", False)

    state.checks.append({
        "check_name": "verification_passed",
        "passed": passed,
        "details": state.verification.get("message", "")
    })

    if passed:
        state.status = "success"
        return state
    if state.retries < 2:
        state.retries += 1
        state.status = "retry"
        return state

    state.status = "failed"
    return state

# -----------------------------
# Terminal Node
# -----------------------------
def end_node(state: GraphState) -> GraphState:
    return state

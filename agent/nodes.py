import json
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from .graph_state import GraphState

# Load prompts
def load_prompt(path):
    with open(path, "r") as f:
        return f.read()

planner_prompt = load_prompt("prompts/planner_prompt.txt")
executor_prompt = load_prompt("prompts/executor_prompt.txt")
verifier_prompt = load_prompt("prompts/verifier_prompt.txt")

llm = ChatOpenAI(model="gpt-4.1", temperature=0)

# ⬇️ Planner Node
def planner_node(state: GraphState):
    prompt = f"""{planner_prompt}

Question:
{state.question}
"""
    response = llm.invoke(prompt)
    state.plan = json.loads(response.content)
    return state


# ⬇️ Executor Node
def executor_node(state: GraphState):
    prompt = f"""{executor_prompt}

Question:
{state.question}

Plan:
{json.dumps(state.plan, indent=2)}
"""
    response = llm.invoke(prompt)
    state.executor_output = json.loads(response.content)
    return state


# ⬇️ Verifier Node
def verifier_node(state: GraphState):
    prompt = f"""{verifier_prompt}

Question:
{state.question}

Proposed Solution:
{json.dumps(state.executor_output, indent=2)}
"""
    response = llm.invoke(prompt)
    state.verification = json.loads(response.content)
    return state


# ⬇️ Retry Logic Node
def check_verification(state: GraphState):
    if state.verification.get("passed"):
        state.status = "success"
        return "done"

    # If failed but retries remain
    if state.retries < 2:
        state.retries += 1
        return "retry"

    # If failed and retries exhausted
    state.status = "failed"
    return "done"

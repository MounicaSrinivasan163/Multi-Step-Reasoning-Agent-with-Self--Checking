import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .graph_state import GraphState

# Load .env file
load_dotenv()

# Read OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "❌ OPENAI_API_KEY not found. Create a .env file or set environment variable."
    )

# Load prompts
def load_prompt(path):
    with open(path, "r") as f:
        return f.read()

planner_prompt = load_prompt("prompts/planner_prompt.txt")
executor_prompt = load_prompt("prompts/executor_prompt.txt")
verifier_prompt = load_prompt("prompts/verifier_prompt.txt")

# Initialize LLM with API key
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=OPENAI_API_KEY)


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





# ⬇️ Terminal Node
def end_node(state: GraphState):
    # Terminal node just returns the state
    return state

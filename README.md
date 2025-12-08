# 🧠 Multi-Step Reasoning Agent with Self-Checking  
A lightweight reasoning agent that solves structured word problems using **Planner → Executor → Verifier** architecture.  
It provides a clean JSON output with a user-facing answer and internal metadata (plan, checks, retries).  
Supports easy extension to any LLM provider (OpenAI, Anthropic, Gemini, etc.).

---

## 🚀 Features

### ✅ Multi-Phase Agent  
1. **Planner**  
   - Reads question  
   - Generates structured plan  
   - Example: parse → extract values → compute → format  

2. **Executor**  
   - Executes plan  
   - Uses Python for calculations  
   - Runs LLM if required  
   - Stores intermediate results  

3. **Verifier**  
   - Independently verifies answer  
   - Recomputes / validates constraints  
   - Flags inconsistencies  
   - Supports retries  

## ✅ Clean JSON Output  
Example:
```json
{
  "answer": "3 hours 35 minutes",
  "status": "success",
  "reasoning_visible_to_user": "Calculated time difference between 14:30 and 18:05.",
  "metadata": {
    "plan": "...",
    "checks": [...],
    "retries": 0
  }
}
```

## 📁 Project Structure

```
reasoning-agent/
│
├── agent.py                # Main agent loop
├── prompts.py              # Planner, executor, verifier prompts
├── llm_client.py           # Wrapper for OpenAI/Gemini APIs
├── solver.py               # Planner/Executor/Verifier orchestrator
├── tests/
│   ├── easy_tests.py       # Basic arithmetic/time tests
│   ├── tricky_tests.py     # Edge cases & ambiguous problems

```

## 🧩 Prompts

Prompts are stored in `prompts.py`:

## 1. Planner Prompt
- Generates numbered steps  
- Output must be JSON-friendly  

## 2. Executor Prompt
- Follows plan exactly  
- Returns intermediate calculations  

## 3. Verifier Prompt
- Re-computes result  
- Returns pass/fail + explanation  

Each prompt includes 2–3 few-shot examples.

---

# ▶️ How to Run

### Option A: CLI  
python agent.py  

### Option B: Use the function  
from solver import solve  
print(solve("Alice has 3 red apples and twice as many green apples. How many apples?"))

---

# 🧪 Tests

Run all tests:  
python tests/easy_tests.py  
python tests/tricky_tests.py  

Test logs include:  
- Question  
- Final JSON output  
- Whether verifier passed  
- If retries occurred  

---

# 📚 Prompt Design Notes

## What Worked
- Separating plan generation improves determinism  
- Executor runs cleanly with Python arithmetic  
- Verifier catches inconsistent LLM reasoning  

## What Didn’t Work Initially
- Allowing executor to interpret the plan caused drift  
- Verifier needed strict JSON format to avoid false failures  

## Future Improvements
- Add caching to avoid repeated planner calls  
- Add streaming responses  
- Improve handling of ambiguous time formats  

├── README.md
```













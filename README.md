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
Mutli-Step-Reasoning-Agent-with-Self-Checking/
│
├── agent/
│   ├── graph.py
│   ├── nodes.py
│   └── graph_state.py
│
├── prompts/
│   ├── planner_prompt.txt
│   ├── executor_prompt.txt
│   └── verifier_prompt.txt
│
├── solve.py
│
└── tests/
      ├── test_easy.py
      ├── test_tricky.py
      ├── test_logs.json
      ├── test_logs.csv

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
```
python agent.py  
```

### Option B: Use the function  
```
from solver import solve  
print(solve("Alice has 3 red apples and twice as many green apples. How many apples?"))
```
---

## 🧪 Evaluation & Test Cases

The agent includes a small automated test suite to validate correctness,
robustness, and self-verification behavior.

### Test Categories

#### ✅ Easy Tests
- Basic arithmetic
- Speed–time–distance
- Simple unit calculations

#### ⚠️ Tricky Tests
- Multi-step reasoning
- Ambiguous phrasing
- Time boundary cases
- Edge cases (zero values)

### How to Run Tests

```bash
pytest tests/test_easy.py
pytest tests/test_tricky.py
```
## 🧪 What Each Test Logs

For every test case, the following details are recorded:

- **Question** – The original user query given to the agent  
- **Final JSON Output** – The complete structured response produced by the agent  
- **Verifier Status** – Whether the verifier approved the solution (`passed = true/false`)  
- **Retries Performed** – Number of times the agent retried planning/execution  

---

## 📄 Logs Export

Test results are automatically exported to the following files:

- `tests/test_logs.json`
- `tests/test_logs.csv`

---

## 🔍 What These Logs Help Evaluate

The exported logs are used to assess:

- **Planner Accuracy** – Whether the agent correctly decomposes the problem  
- **Executor Consistency** – Whether calculations follow the plan reliably  
- **Verifier Effectiveness** – Whether incorrect or inconsistent answers are caught  
- **Retry Behavior** – How often and when the agent self-corrects  

These artifacts make the agent’s reasoning loop transparent and easy to evaluate during review.

---

## 📊 Test Summary

| Category | Test Count | Verifier Pass Rate | Retries Observed |
|--------|------------|--------------------|------------------|
| Easy   | 5          | 100%               | 0–1              |
| Tricky | 4          | ~90%               | 1–2              |

✔ Easy tests validate deterministic reasoning  
✔ Tricky tests stress multi-step planning and verification  
✔ Retries confirm self-correction behavior


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

---










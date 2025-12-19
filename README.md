# 🧠 Multi-Step Reasoning Agent with Self-Checking

---
Streamlit app link: https://multi-step-reasoning-agent-with-self-checking.streamlit.app/
---

A lightweight multi-step reasoning agent built using a **Planner → Executor → Verifier** architecture with automatic retries, logging, and evaluation.

The system produces:
- A clean, user-facing answer
- A machine-friendly JSON output
- Internal metadata (plan, checks, retries)
- Persistent logs (CSV / JSON) for evaluation

Designed for structured word problems such as arithmetic, time, and multi-step reasoning tasks.

---

## 🚀 Key Features

### 🧩 Multi-Phase Reasoning Pipeline

1. Planner  
   - Reads the question  
   - Produces a structured step-by-step plan  
   - Output is JSON-friendly and deterministic  

2. Executor  
   - Executes the plan exactly  
   - Performs calculations  
   - Returns intermediate_result and factual step records  
   - No chain-of-thought exposed  

3. Verifier  
   - Independently validates executor output  
   - Recomputes results  
   - Flags incorrect reasoning  
   - Triggers retries if needed  

4. Retry Controller  
   - Automatically retries up to a fixed limit  
   - Tracks retry count for evaluation  

---

## ✅ Expected JSON Output

Example response:
```
{
  "answer": 350,
  "status": "success",
  "reasoning_visible_to_user": "I solved this by planning, executing, and verifying the result.",
  "metadata": {
    "plan": {
      "steps": [
        "Calculate distance at 50 km/hr for 3 hours",
        "Calculate distance at 80 km/hr for 2 hours",
        "Sum both distances"
      ]
    },
    "checks": [
      {
        "check_name": "verification_passed",
        "passed": true,
        "details": ""
      }
    ],
    "retries": 0
  }
}
```
---

## 📁 Project Structure
```
MultiStep_Reasoning/
│
├── agent/
│   ├── graph.py              # LangGraph definition
│   ├── nodes.py              # Planner / Executor / Verifier nodes
│   └── graph_state.py        # State schema
│
├── prompts/
│   ├── planner_prompt.txt
│   ├── executor_prompt.txt
│   └── verifier_prompt.txt
│
├── solve.py                  # Core solve() API
├── app.py                    # Streamlit UI
│
├── tests/
│   ├── easy_tests.py
│   ├── tricky_tests.py
│
├── utils/
│   └── logger.py             # CSV / JSON logger
│
├── logs/
│   ├── run_logs.csv
│   
│
├── run_tests.py              # Test runner
└── print_summary.py          # Test analytics
```
---

## 🖥️ How to Run the Application

Start the Streamlit App:

```
streamlit run app.py
```
- Enter a question
- View final answer, explanation, retries, verifier checks, and raw JSON output

---

## 🧪 Evaluation & Test Suite

The project includes a custom test framework to evaluate reasoning quality and robustness.

### Test Categories

Easy Tests:
- Basic arithmetic
- Speed × time × distance
- Simple time differences

Tricky Tests:
- Multi-step reasoning
- Ambiguous phrasing
- Time boundary cases
- Edge conditions

---

## ▶️ How to Run Tests

Run all tests:

python run_tests.py

Run individually:

```
python -m tests.easy_tests  
python -m tests.tricky_tests  
```
---

## 🧪 What Each Test Logs

For every test case, the following are recorded:

- Question  
- Final JSON output  
- Whether the verifier passed  
- Number of retries performed  

---

## 📄 Logs Export

All runs (tests + app usage) are automatically logged to:

- logs/run_logs.csv  
 
---

## 🔍 What the Logs Help Evaluate

- Planner accuracy  
- Executor consistency  
- Verifier effectiveness  
- Retry behavior  

---

## 📊 Auto-Generated Test Summary

Category | Test Count | Verifier Pass Rate | Retries Observed  
Easy     | 5–10       | ~100%              | 0–1  
Tricky  | 3–5        | ~85–90%            | 1–2  

---

## 📈 Retry & Quality Metrics

Using print_summary.py, the system computes:
- Retry rate
- Average retries per question
- Planner / Executor quality indicators
- Failure patterns

---

## ⚠️ Rate-Limit Notes

- Running many tests consumes LLM tokens  
- For testing: use smaller models  
- For demo / production: use gpt-4o-mini  

---

## 🚧 Future Improvements

- Local math executor (no LLM for arithmetic)
- Caching planner outputs
- Parallel verifier strategies
- Streaming UI responses
- Confidence scoring

---

## ✅ Summary

- Clean architecture  
- Deterministic execution  
- Self-verification  
- Retry logic  
- Full evaluation framework  
- Production-ready logging  


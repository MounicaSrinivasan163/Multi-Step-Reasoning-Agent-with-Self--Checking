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
## 🧠 Prompt Design & Rationale

This project uses **role-specific prompts** for each agent stage (Planner, Executor, Verifier) to enforce separation of concerns and improve reasoning reliability.

---

### 🔹 Why the Prompts Were Designed This Way

#### **1. Planner Prompt**
**Goal:** Convert a natural language question into a deterministic, structured plan.

**Design choices:**
- Forces numbered, sequential steps
- Avoids computation or reasoning
- Produces JSON-friendly output

**Why this works:**
- Prevents early arithmetic mistakes
- Makes multi-step problems explicit
- Enables retries by re-planning instead of guessing

**Example responsibilities:**
- Identify inputs (numbers, units, times)
- Decide computation order
- Specify transformations (sum, difference, conversion)

---

#### **2. Executor Prompt**
**Goal:** Execute the plan *exactly as written* and produce a machine-checkable result.

**Design choices:**
- Strict JSON schema (intermediate_result + steps)
- One factual line per step
- No free-form explanation or verification

**Why this works:**
- Keeps execution deterministic
- Makes debugging and testing easy
- Allows verifier to independently recompute results

**Executor never:**
- Fixes planner mistakes
- Verifies correctness
- Adds assumptions silently

---

#### **3. Verifier Prompt**
**Goal:** Independently validate the executor’s result.

**Design choices:**
- Recomputes from scratch
- Outputs pass/fail + short summary
- No chain-of-thought exposure

**Why this works:**
- Catches arithmetic slips
- Detects plan/execution mismatch
- Enables controlled retries without infinite loops

---

### ⚠️ What Didn’t Work Well Initially

1. **Single-prompt reasoning**
   - Mixing planning, execution, and verification caused hallucinations
   - Difficult to debug or retry

2. **Free-form Executor output**
   - Inconsistent formats broke tests
   - Verifier could not reliably parse results

3. **Verbose chain-of-thought**
   - Caused token overuse
   - Reduced determinism
   - Violated safe-output constraints

4. **Implicit assumptions**
   - Ambiguous inputs (time ranges, units) caused silent errors
   - Fixed by forcing explicit assumptions into metadata

---

### 🚀 What I Would Improve With More Time

1. **Prompt caching**
   - Cache Planner outputs for repeated or similar questions
   - Reduce token usage and rate-limit issues

2. **Stronger Verifier heuristics**
   - Add multiple independent checks (units, bounds, sanity checks)
   - Score confidence instead of binary pass/fail

3. **Executor fallback logic**
   - Use pure Python for arithmetic-only plans
   - Call LLM only when interpretation is required

4. **Adaptive retry strategy**
   - Change prompts dynamically after repeated failures
   - Example: simplify plan or reduce step count

5. **Benchmark-driven prompt tuning**
   - Optimize prompts based on test pass rate
   - Track failure modes across easy vs tricky cases

---

### ✅ Outcome

This prompt design achieves:
- **High determinism**
- **Clear auditability**
- **Reliable self-correction**
- **Clean JSON outputs suitable for evaluation**

It balances LLM flexibility with strong structural constraints, making the system suitable for both **interactive use** and **automated testing**.

---
## ⚠️ Current Architecture Challenges & Future Improvements

### General Challenges in the Current Architecture

1. **LLM-based Arithmetic Is Non-Deterministic**  
   While LLMs are strong at reasoning and explanation, they are unreliable for precise mathematical computation, especially with fractions, rates, and sign-sensitive problems.

2. **Verifier Is Not Truly Independent**  
   The Verifier uses the same LLM paradigm as the Executor, which can cause it to repeat the same incorrect reasoning instead of catching errors.

3. **Lack of Formula Enforcement**  
   Mathematical domains (rates, mensuration, time–work) require strict formula application, which the current architecture does not enforce programmatically.

4. **Retries Don’t Guarantee Correction**  
   When the core reasoning pattern is flawed, retries may only restate the same mistake in different wording.

---

### Example: Pipes & Cisterns Failure

**Question:**  
Pipes A and B can fill a tank in 20 and 30 hours respectively, while Pipe C empties it in 60 hours.  
If all three are opened together, how long will it take to fill the tank?

**Correct Solution:**  
```
Correct Solution:

Net filling rate =
1/20 + 1/30 − 1/60

LCM = 60

= 3/60 + 2/60 − 1/60
= 4/60
= 1/15

So, time required = 15 hours
```

**Agent Output:**  
24 hours ❌

#### What Went Wrong
- The **Executor** incorrectly combined rate fractions
- The **Verifier** validated the same flawed reasoning
- No deterministic check existed to enforce correct rate arithmetic

This illustrates a core limitation:  
> LLMs can describe math convincingly while still producing incorrect results.

---

### How This Can Be Improved in the Future

1. **Hybrid Execution Layer**
   - Delegate all numeric computation to Python functions
   - Use the LLM only for planning and explanation

2. **Deterministic Verification**
   - Recompute results using formulas instead of natural language
   - Reject answers that don’t match computed values

3. **Domain-Aware Executors**
   - Special handlers for:
     - Pipes & Cisterns
     - Time & Work
     - Mensuration
     - Speed–Distance–Time

4. **Smarter Retry Strategy**
   - On failure, switch execution mode (LLM → deterministic)
   - Avoid repeating identical reasoning paths

---

### Key Takeaway

This architecture intentionally exposes LLM weaknesses rather than hiding them, making reasoning failures transparent and correctable.  
Future versions will combine LLM reasoning with deterministic computation for mathematical reliability.
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


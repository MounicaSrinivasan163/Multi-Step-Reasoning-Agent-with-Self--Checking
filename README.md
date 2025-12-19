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

## ⚠️ Current Limitations & Future Improvements

### What Didn’t Work Well Initially

1. **Single-Prompt Reasoning**
   - Combining planning, execution, and verification in one prompt led to hallucinations.
   - Failures were hard to debug, and retries often repeated the same mistake.

2. **Free-Form Executor Output**
   - Inconsistent response formats caused parsing and test failures.
   - The verifier could not reliably extract or validate results.

3. **Verbose Chain-of-Thought**
   - Increased token usage and reduced determinism.
   - Risked violating safe-output and evaluation constraints.

4. **Implicit Assumptions**
   - Ambiguous inputs (units, time ranges, directions) caused silent errors.
   - Partially mitigated by forcing explicit assumptions into structured metadata.

---

### What I Would Improve With More Time

1. **Prompt Caching**
   - Cache Planner outputs for repeated or similar questions.
   - Reduce token usage and rate-limit pressure.

2. **Stronger Verifier Heuristics**
   - Add multiple independent checks (units, bounds, sanity checks).
   - Move from binary pass/fail to confidence scoring.

3. **Executor Fallback Logic**
   - Use pure Python for arithmetic-only plans.
   - Invoke the LLM only when interpretation or decomposition is required.

4. **Adaptive Retry Strategy**
   - Dynamically modify prompts after repeated failures.
   - Example: simplify plans, reduce step count, or switch execution mode.

5. **Benchmark-Driven Prompt Tuning**
   - Continuously tune prompts based on test pass rates.
   - Track and analyze failure modes across easy vs. tricky cases.

---

### Current Architecture Challenges

1. **LLM-Based Arithmetic Is Non-Deterministic**  
   LLMs are strong at explanation but unreliable for precise computation, especially with fractions, rates, and sign-sensitive problems.

2. **Verifier Is Not Fully Independent**  
   Using the same LLM paradigm for execution and verification can replicate the same flawed reasoning instead of catching it.

3. **Lack of Formula Enforcement**  
   Mathematical domains (pipes & cisterns, time–work, mensuration) require strict formula application, which is not enforced programmatically.

4. **Retries Don’t Guarantee Correction**  
   When the underlying reasoning pattern is wrong, retries may only restate the same error.

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

**What Went Wrong**
- The Executor incorrectly combined rate fractions.
- The Verifier validated the same flawed reasoning.
- No deterministic, formula-based check enforced correct arithmetic.

This highlights a core limitation:
> LLMs can produce convincing explanations while still being numerically wrong.

---

### How This Will Be Improved

1. **Hybrid Execution Layer**
   - Delegate all numeric computation to deterministic Python functions.
   - Use the LLM only for planning and explanation.

2. **Deterministic Verification**
   - Recompute results using formulas, not natural language.
   - Reject outputs that don’t match computed values.

3. **Domain-Aware Executors**
   - Introduce specialized handlers for:
     - Pipes & Cisterns
     - Time & Work
     - Mensuration
     - Speed–Distance–Time

4. **Smarter Retry Strategy**
   - Switch execution modes on failure (LLM → deterministic).
   - Avoid repeating identical reasoning paths.

---

### Key Takeaway

This architecture deliberately **exposes LLM weaknesses instead of hiding them**, making reasoning failures transparent and auditable.  
Future iterations will combine LLM-based planning with deterministic computation and verification to achieve mathematical reliability while preserving interpretability.


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


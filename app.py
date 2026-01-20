import json
import streamlit as st
from utils.logger import log_run
from solve import solve

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Multi-Step Reasoning Agent",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Multi-Step Reasoning Agent")
st.caption("Planner → Executor → Verifier → Retry/checker  →  Final Answer")

# -----------------------------
# User Input
# -----------------------------
question = st.text_area(
    "Enter your question",
    placeholder="Example: If I travel at 60 km/hr for 2 hours, what distance do I cover?"
)

run = st.button("Run Agent 🚀")

# -----------------------------
# Run Agent
# -----------------------------
if run and question.strip():

    with st.spinner("Thinking..."):
        result = solve(question)
        log_run(result=result, question=question, source="app")

    # -----------------------------
    # Neat Answer Output
    # -----------------------------
    st.subheader("✅ Final Answer")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Answer:**")
        st.success(result.get("answer", "N/A"))

        st.markdown("**Status:**")
        st.info(result.get("status", "unknown"))

    with col2:
        st.markdown("**Explanation:**")
        st.write(result.get("reasoning_visible_to_user", ""))

    # -----------------------------
    # Metadata Summary
    # -----------------------------
    st.subheader("📊 Execution Summary")
    meta = result.get("metadata", {})

    st.write(f"**Retries:** {meta.get('retries', 0)}")

    checks = meta.get("checks", [])
    if checks:
        for check in checks:
            check_name = check.get("check_name", "unknown_check")
            passed = check.get("passed", False)
            status_text = "✅ Passed" if passed else "❌ Failed"
            details = check.get("details", "")
            st.write(f"- **{check_name}** → {status_text} | {details}")

    # -----------------------------
    # Raw JSON Output
    # -----------------------------
    st.subheader("🧾 Raw JSON Output")
    st.code(json.dumps(result, indent=2), language="json")

elif run:
    st.warning("Please enter a question.")


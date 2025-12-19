import csv
from collections import defaultdict

LOG_FILE = "logs/run_logs.csv"

def generate_summary():
    summary = defaultdict(int)
    retry_count = 0
    verifier_failures = 0

    with open(LOG_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        summary["total"] += 1

        if row["status"] == "success":
            summary["success"] += 1

        retries = int(row["retries"])
        retry_count += retries
        if retries > 0:
            summary["retried"] += 1

        if row["verifier_passed"] == "False":
            verifier_failures += 1

    summary["avg_retries"] = round(retry_count / max(summary["total"], 1), 2)
    summary["verifier_pass_rate"] = round(
        (summary["total"] - verifier_failures) / max(summary["total"], 1) * 100, 2
    )
    
    summary["planner_quality"] = round(
    (summary["success"] - summary.get("retried", 0)) / summary["success"] * 100, 2
     )

    summary["executor_quality"] = summary["verifier_pass_rate"]


    return summary

import csv
import os
from datetime import datetime

LOG_FILE = "logs/run_logs.csv"

HEADERS = [
    "timestamp",
    "source",
    "question",
    "answer",
    "status",
    "verifier_passed",
    "retries",
    "raw_json"
]


def log_run(result: dict, question: str, source: str = "app"):
    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.exists(LOG_FILE)

    verifier_passed = any(
        check.get("passed", False)
        for check in result.get("metadata", {}).get("checks", [])
    )

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "question": question,
            "answer": result.get("answer"),
            "status": result.get("status"),
            "verifier_passed": verifier_passed,
            "retries": result.get("metadata", {}).get("retries", 0),
            "raw_json": str(result)
        })

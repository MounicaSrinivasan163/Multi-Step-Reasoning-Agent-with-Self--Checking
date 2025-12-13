import json
import csv

json_file = "tests/test_logs.json"
csv_file = "tests/test_logs.csv"

with open(json_file, "r") as f:
    data = json.load(f)

with open(csv_file, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["question", "status", "answer", "verifier_passed", "retries"]
    )
    writer.writeheader()
    writer.writerows(data)

print("✅ Logs exported to CSV")

import json
from solve import solve

def test_tricky_questions():

    tricky_questions = [
        "I travel at 50 km/hr for 3 hours and then 80 km/hr for 2 hours. What is the total distance?",
        "A car travels for 2 hours at 60 km/hr, then slows down to half the speed for 1 hour. Total distance?",
        "A train departs at 9:30 AM and arrives at 1:15 PM. How long is the journey?",
        "If speed is 0 km/hr for 2 hours, what distance is covered?"
    ]

    logs = []

    for question in tricky_questions:
        result = solve(question)

        assert result["status"] in ["success", "failed"]

        verifier_passed = result["metadata"]["checks"][-1]["passed"]
        retries = result["metadata"]["retries"]

        logs.append({
            "question": question,
            "status": result["status"],
            "answer": result["answer"],
            "verifier_passed": verifier_passed,
            "retries": retries
        })

    with open("tests/test_logs_tricky.json", "w") as f:
        json.dump(logs, f, indent=2)

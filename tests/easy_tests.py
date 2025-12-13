import json
from solve import solve

def test_easy_questions():

    easy_questions = [
        "If I travel at 60 km/hr for 2 hours, what distance do I cover?",
        "A train moves at 40 km/hr for 3 hours. Find the distance.",
        "A car travels 50 km/hr for 4 hours. How far does it go?",
        "A person walks 5 km/hr for 6 hours. What distance is covered?",
        "How long will it take to travel 120 km at 60 km/hr?"
    ]

    logs = []

    for question in easy_questions:
        result = solve(question)

        # ✅ Assertions
        assert result["status"] == "success"
        assert "answer" in result
        assert "metadata" in result

        verifier_passed = result["metadata"]["checks"][-1]["passed"]
        retries = result["metadata"]["retries"]

        assert verifier_passed is True
        assert retries >= 0

        logs.append({
            "question": question,
            "status": result["status"],
            "answer": result["answer"],
            "verifier_passed": verifier_passed,
            "retries": retries
        })

    # Save logs
    with open("tests/test_logs.json", "w") as f:
        json.dump(logs, f, indent=2)

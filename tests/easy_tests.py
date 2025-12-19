from solve import solve
from utils.logger import log_run

QUESTIONS = [
        "If I travel at 60 km/hr for 2 hours, what distance do I cover?",
        "A train moves at 40 km/hr for 3 hours. Find the distance.",
    ]

for q in QUESTIONS:
    result = solve(q)

    # Assertion
    assert result["status"] == "success"

    # Log test run
    log_run(
        result=result,
        question=q,
        source="easy_test"
    )

    print("Testing Done for the question : ", q)

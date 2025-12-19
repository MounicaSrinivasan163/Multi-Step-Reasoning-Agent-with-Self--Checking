from solve import solve
from utils.logger import log_run

QUESTIONS = [
        "I travel at 50 km/hr for 3 hours and then 80 km/hr for 2 hours. What is the total distance?",
        "A car travels for 2 hours at 60 km/hr, then slows down to half the speed for 1 hour. Total distance?",
        
    ]

for q in QUESTIONS:
    result = solve(q)

    assert result["status"] == "success"

    log_run(
        result=result,
        question=q,
        source="tricky_test"
    )

    print("Testing Done for the question : ", q)

from solve import solve
import json

easy_questions = [
    "If I travel at 60 km/hr for 2 hours, what distance do I cover?",
    "A train moves at 40 km/hr for 3 hours. Find the distance.",
    "A car travels 50 km/hr for 4 hours. How far does it go?",
    "A person walks 5 km/hr for 6 hours. What distance is covered?",
    "A cyclist rides at 20 km/hr for 1.5 hours. What is the distance?",
    "How long will it take to travel 120 km at 60 km/hr?",
    "What is the speed if 150 km is covered in 3 hours?"
]

print("\n🧪 RUNNING EASY TESTS")
print("=" * 60)

for idx, question in enumerate(easy_questions, start=1):
    print(f"\nTest Case {idx}")
    print("-" * 40)
    print("Question:", question)

    result = solve(question)

    print("\nFinal JSON:")
    print(json.dumps(result, indent=2))

    checks = result.get("metadata", {}).get("checks", [])
    verifier_passed = checks[-1]["passed"] if checks else False
    retries = result.get("metadata", {}).get("retries", 0)

    print("\nVerifier Passed:", verifier_passed)
    print("Retries Occurred:", retries)
    print("=" * 60)

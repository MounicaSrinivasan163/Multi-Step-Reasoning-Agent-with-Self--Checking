from solve import solve
import json

tricky_questions = [
    # Multi-step
    "I travel at 50 km/hr for 3 hours and then 80 km/hr for 2 hours. What is the total distance?",

    # Ambiguous phrasing
    "A car travels for 2 hours at 60 km/hr, then slows down to half the speed for 1 hour. Total distance?",

    # Time boundary
    "A train departs at 9:30 AM and arrives at 1:15 PM. How long is the journey?",

    # Mixed units
    "A runner runs 500 meters every 2 minutes. How far does she run in 20 minutes?",

    # Edge case
    "If speed is 0 km/hr for 2 hours, what distance is covered?"
]

print("\n🧪 RUNNING TRICKY TESTS")
print("=" * 60)

for idx, question in enumerate(tricky_questions, start=1):
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

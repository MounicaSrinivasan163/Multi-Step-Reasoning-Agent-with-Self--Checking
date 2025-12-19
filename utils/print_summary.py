from utils.summary import generate_summary

summary = generate_summary()

print("\n📊 TEST SUMMARY")
print("-" * 40)
print(f"Total Tests        : {summary['total']}")
print(f"Successful         : {summary['success']}")
print(f"Retried Tests      : {summary.get('retried', 0)}")
print(f"Avg Retries        : {summary['avg_retries']}")
print(f"Verifier Pass Rate : {summary['verifier_pass_rate']}%")
print("-" * 40)

import subprocess
import sys

def run_test(module_name):
    print(f"\n🚀 Running {module_name}...\n")
    result = subprocess.run(
        [sys.executable, "-m", module_name],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("❌ Errors:\n", result.stderr)

if __name__ == "__main__":
    run_test("tests.easy_tests")
    run_test("tests.tricky_tests")

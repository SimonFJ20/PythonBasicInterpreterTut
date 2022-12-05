from glob import glob
from subprocess import run
from re import search
from sys import argv

def run_part_tests(flag: str, test_folder: str, exit_on_error=False, exit_on_fail=False):
    samples = list(sorted(filter(lambda s : test_folder in s, glob(f"tests/**/*.skl"))))
    expected = list(sorted(filter(lambda s : test_folder in s, glob(f"tests/**/*.expected"))))
    for i in range(len(samples)):
        print(f"Running '{samples[i]}' ", end="")
        result = run(["node", "skivelang.js", samples[i], flag], capture_output=True)
        if result.returncode != 0:
            print("FAIL")
            print("REASON: returncode != 0")
            print("ERROR:")
            print(result.stderr.decode("utf-8"))
            if exit_on_error: exit()
        else:
            with open(expected[i]) as f:
                expected_stdout = f.read()
            if expected_stdout != result.stdout.decode("utf-8"):
                print("FAIL", flush=True)
                print("REASON: expected_stdout != result.stdout")
                print("EXPECTED:")
                print(expected_stdout)
                print("GOT:")
                print(result.stdout.decode("utf-8"))
                if exit_on_fail: exit()
            else:
                print("OK", flush=True)

if __name__ == "__main__":
    exit_on_fail = "--exit-on-fail" in argv
    exit_on_error = "--exit-on-error" in argv
    run_part_tests("--test-tokenizer", "tokenizer", exit_on_error, exit_on_fail)
    run_part_tests("--test-parser", "parser", exit_on_error, exit_on_fail)
    run_part_tests("--test-transpiler", "transpiler", exit_on_error, exit_on_fail)


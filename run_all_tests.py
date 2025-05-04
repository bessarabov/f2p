#!/usr/bin/env python3

import os
import subprocess
import sys

TESTS_DIR = os.path.abspath(os.path.dirname(__file__)) + '/tests/'
F2P = os.path.abspath(os.path.join(TESTS_DIR, '..', 'f2p'))

def run_test(test_dir):
    full_path = os.path.join(TESTS_DIR, test_dir)

    with open(os.path.join(full_path, 'run.cmd')) as f:
        cmd = f.read().strip()

    cmd_parts = cmd.replace('../../f2p', F2P).split()

    result = subprocess.run(
        cmd_parts,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=full_path,
        text=True
    )

    actual_stdout = result.stdout.strip()
    actual_stderr = result.stderr.strip()

    stdout_path = os.path.join(full_path, 'expected_stdout')
    stderr_path = os.path.join(full_path, 'expected_stderr')

    ok = True

    if os.path.exists(stdout_path):
        with open(stdout_path) as f:
            expected_stdout = f.read().strip()
        if actual_stdout != expected_stdout:
            print(f"[FAIL] {test_dir} (stdout mismatch)")
            print(cmd)
            print("Expected stdout:")
            print(expected_stdout)
            print("Actual stdout:")
            print(actual_stdout)
            ok = False

    if os.path.exists(stderr_path):
        with open(stderr_path) as f:
            expected_stderr = f.read().strip()
        if actual_stderr != expected_stderr:
            print(f"[FAIL] {test_dir} (stderr mismatch)")
            print(cmd)
            print("Expected stderr:")
            print(expected_stderr)
            print("Actual stderr:")
            print(actual_stderr)
            ok = False
        if result.returncode == 0:
            print(f"[FAIL] {test_dir} (expected non-zero exit code)")
            ok = False

    if not os.path.exists(stdout_path) and not os.path.exists(stderr_path):
        print(f"[FAIL] {test_dir} (no expected output files)")
        ok = False

    if ok:
        print(f"[ OK ] {test_dir}")

    return ok

def main():
    test_dirs = [d for d in os.listdir(TESTS_DIR)
                 if os.path.isdir(os.path.join(TESTS_DIR, d))]

    failed = 0
    for td in sorted(test_dirs):
        if not run_test(td):
            failed += 1

    if failed:
        print(f"\n{failed} test(s) failed.")
        sys.exit(1)
    else:
        print("\nAll tests passed.")

if __name__ == '__main__':
    main()


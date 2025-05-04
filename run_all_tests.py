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
    expected_path = os.path.join(full_path, 'expected_stdout')

    if os.path.exists(expected_path):
        with open(expected_path) as f:
            expected_stdout = f.read().strip()
    else:
        expected_stdout = ''

    if actual_stdout != expected_stdout:
        print(f"[FAIL] {test_dir}")
        print(cmd)
        print("Expected:")
        print(expected_stdout)
        print("Actual:")
        print(actual_stdout)
        return False
    else:
        print(f"[ OK ] {test_dir}")
        return True

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

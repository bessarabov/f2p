#!/usr/bin/env python3

import os
import subprocess
import sys

TESTS_DIR = os.path.abspath(os.path.dirname(__file__)) + '/tests/'
F2P = os.path.abspath(os.path.join(TESTS_DIR, '..', 'f2p'))

def read_file_contents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

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

    actual_stdout = result.stdout
    actual_stderr = result.stderr

    file_expected_stdout = os.path.join(full_path, 'expected_stdout')
    file_expected_stderr = os.path.join(full_path, 'expected_stderr')
    expected_stdout = read_file_contents(file_expected_stdout)
    expected_stderr = read_file_contents(file_expected_stderr)

    ok = True

    if actual_stdout != expected_stdout:
        #write_file(file_expected_stdout, actual_stdout)
        print(f"[FAIL] {test_dir} (stdout mismatch)")
        print(cmd)
        print("Expected stdout:")
        print(expected_stdout)
        print("Actual stdout:")
        print(actual_stdout)
        ok = False

    if actual_stderr != expected_stderr:
        #write_file(file_expected_stderr, actual_stderr)
        print(f"[FAIL] {test_dir} (stderr mismatch)")
        print(cmd)
        print("Expected stderr:")
        print(expected_stderr)
        print("Actual stderr:")
        print(actual_stderr)
        ok = False

    if ok:
        print(f"[ OK ] {test_dir}")

    return ok

def main():
    test_dirs = [d for d in os.listdir(TESTS_DIR)
                 if os.path.isdir(os.path.join(TESTS_DIR, d))]

    succeeded = 0
    failed = 0
    for td in sorted(test_dirs):
        if run_test(td):
            succeeded += 1
        else:
            failed += 1

    if failed:
        print(f"\n{succeeded} test(s) succeeded.")
        print(f"{failed} test(s) failed.")
        sys.exit(1)
    else:
        print(f"\n{succeeded} test(s) succeeded.")
        print("All tests passed.")

if __name__ == '__main__':
    main()

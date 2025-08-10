#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import argparse
import shlex

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

def run_test(test_dir, verbose=False):
    full_path = os.path.join(TESTS_DIR, test_dir)
    cwd = os.path.join(TESTS_DIR, test_dir, 'dir')

    with open(os.path.join(full_path, 'run.cmd')) as f:
        cmd = f.read().strip()

    cmd_parts = shlex.split(cmd.replace('../../f2p', F2P))

    test_gitignore_file = os.path.join(full_path, 'gitignore')
    test_gitignore_in_cwd = os.path.join(TESTS_DIR, test_dir, 'dir', '.gitignore')
    if os.path.exists(test_gitignore_file):
        shutil.copy2(test_gitignore_file, test_gitignore_in_cwd)

    result = subprocess.run(
        cmd_parts,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
        text=True
    )

    if os.path.exists(test_gitignore_in_cwd):
        os.remove(test_gitignore_in_cwd)

    actual_stdout = result.stdout
    actual_stderr = result.stderr

    file_expected_stdout = os.path.join(full_path, 'expected_stdout')
    file_expected_stderr = os.path.join(full_path, 'expected_stderr')
    expected_stdout = read_file_contents(file_expected_stdout)
    expected_stderr = read_file_contents(file_expected_stderr)

    stdout_mismatch = actual_stdout != expected_stdout
    stderr_mismatch = actual_stderr != expected_stderr
    ok = not (stdout_mismatch or stderr_mismatch)

    if ok:
        print(f"[ OK ] {test_dir}")
        return True

    print(f"[FAIL] {test_dir}")
    if verbose:
        if stdout_mismatch:
            print("(stdout mismatch)")
            print("Command:")
            print(' '.join(cmd_parts))
            print("Expected stdout:")
            print(expected_stdout)
            print("Actual stdout:")
            print(actual_stdout)
        if stderr_mismatch:
            print("(stderr mismatch)")
            print("Command:")
            print(' '.join(cmd_parts))
            print("Expected stderr:")
            print(expected_stderr)
            print("Actual stderr:")
            print(actual_stderr)
    return False

def list_available_tests():
    return sorted(
        d for d in os.listdir(TESTS_DIR)
        if os.path.isdir(os.path.join(TESTS_DIR, d))
    )

def main():
    parser = argparse.ArgumentParser(description="Run f2p tests")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed diffs for failures')
    parser.add_argument('-t', '--test', metavar='TEST_DIR', default=None,
                        help='Run only the specified test directory under tests/')
    args = parser.parse_args()

    if args.test:
        candidate = os.path.join(TESTS_DIR, args.test)
        if not os.path.isdir(candidate):
            print(f"Error: test '{args.test}' not found under {TESTS_DIR}", file=sys.stderr)
            avail = list_available_tests()
            if avail:
                print("Available tests:", file=sys.stderr)
                for name in avail:
                    print(f"  - {name}", file=sys.stderr)
            else:
                print("No tests found.", file=sys.stderr)
            sys.exit(2)
        test_dirs = [args.test]
    else:
        test_dirs = list_available_tests()

    succeeded = 0
    failed = 0
    for td in test_dirs:
        if run_test(td, verbose=args.verbose):
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

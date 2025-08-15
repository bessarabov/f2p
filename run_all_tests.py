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

def run_test(test_dir, verbose=False, update=False):
    test_dir_full_path = os.path.join(TESTS_DIR, test_dir)
    original_dir_full_path = os.path.join(test_dir_full_path, 'dir')
    working_dir_full_path = os.path.join(test_dir_full_path, 'working_dir')

    shutil.copytree(original_dir_full_path, working_dir_full_path)

    with open(os.path.join(test_dir_full_path, 'run.cmd')) as f:
        cmd = f.read().strip()

    cmd_parts = shlex.split(cmd.replace('../../f2p', F2P))

    test_gitignore_file = os.path.join(test_dir_full_path, 'gitignore')
    test_gitignore_in_working_dir = os.path.join(working_dir_full_path, '.gitignore')
    if os.path.exists(test_gitignore_file):
        shutil.copy2(test_gitignore_file, test_gitignore_in_working_dir)

    try:
        result = subprocess.run(
            cmd_parts,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_dir_full_path,
            text=True
        )
    except Exception as e:
        # Could not execute command at all
        if os.path.exists(test_gitignore_in_working_dir):
            os.remove(test_gitignore_in_working_dir)
        if update:
            print(f"[FAIL] {test_dir} (update failed: {e})")
        else:
            print(f"[FAIL] {test_dir} (exec error: {e})")
        return False

    shutil.rmtree(working_dir_full_path)

    actual_stdout = result.stdout
    actual_stderr = result.stderr

    file_expected_stdout = os.path.join(test_dir_full_path, 'expected_stdout')
    file_expected_stderr = os.path.join(test_dir_full_path, 'expected_stderr')

    if update:
        # Overwrite expectations with current outputs
        write_file(file_expected_stdout, actual_stdout)
        write_file(file_expected_stderr, actual_stderr)
        print(f"[UPD ] {test_dir}")
        return True

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
    parser.add_argument('-u', '--update', action='store_true',
                        help='Overwrite expected_stdout and expected_stderr with actual outputs for the selected test(s) (“bless” mode).')
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
        if run_test(td, verbose=args.verbose, update=args.update):
            succeeded += 1
        else:
            failed += 1

    if failed:
        print(f"\n{succeeded} test(s) succeeded.")
        print(f"{failed} test(s) failed.")
        sys.exit(1)
    else:
        print(f"\n{succeeded} test(s) succeeded.")
        if args.update:
            print("All tests updated.")
        else:
            print("All tests passed.")

if __name__ == '__main__':
    main()


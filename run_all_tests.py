#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import argparse
import shlex

ROOT_DIR = os.path.abspath(os.path.dirname(__file__)) + '/'
TESTS_DIR = ROOT_DIR + 'tests/'

def read_file_contents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def safe_write_or_delete(file_path, content):
    """Write file only if content is non-empty; delete file if content is empty."""
    if content:
        write_file(file_path, content)
    else:
        if os.path.isfile(file_path):
            os.remove(file_path)

def run_test(test_dir, verbose=False, update=False):
    test_path = os.path.join(TESTS_DIR, test_dir)
    original_dir = os.path.join(test_path, 'dir')
    working_dir = os.path.join(test_path, 'working_dir')

    shutil.copytree(original_dir, working_dir)

    with open(os.path.join(test_path, 'run.cmd')) as f:
        cmd = ROOT_DIR + f.read().strip()

    cmd_parts = shlex.split(cmd)

    gitignore_src = os.path.join(test_path, 'gitignore')
    gitignore_dst = os.path.join(working_dir, '.gitignore')
    if os.path.exists(gitignore_src):
        shutil.copy2(gitignore_src, gitignore_dst)

    try:
        result = subprocess.run(
            cmd_parts,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_dir,
            text=True
        )
    except Exception as e:
        if os.path.exists(gitignore_dst):
            os.remove(gitignore_dst)
        print(f"[FAIL] {test_dir} (exec error: {e})")
        return False
    finally:
        shutil.rmtree(working_dir)

    actual_stdout = result.stdout
    actual_stderr = result.stderr
    exit_code = result.returncode

    expected_stdout_file = os.path.join(test_path, 'expected_stdout')
    expected_stderr_file = os.path.join(test_path, 'expected_stderr')
    expected_exit_file   = os.path.join(test_path, 'expected_exit_code')

    if update:
        # Only write stdout file if non-empty, else delete
        safe_write_or_delete(expected_stdout_file, actual_stdout)

        # Only write stderr file if non-empty, else delete
        safe_write_or_delete(expected_stderr_file, actual_stderr)

        # Handle exit code file
        if exit_code != 0:
            write_file(expected_exit_file, f"{exit_code}\n")
        else:
            if os.path.exists(expected_exit_file):
                os.remove(expected_exit_file)

        print(f"[UPD ] {test_dir}")
        return True

    expected_stdout = read_file_contents(expected_stdout_file)
    expected_stderr = read_file_contents(expected_stderr_file)

    # Determine expected exit code
    if os.path.exists(expected_exit_file):
        raw = read_file_contents(expected_exit_file).strip()
        try:
            expected_exit = int(raw) if raw else 0
        except ValueError:
            print(f"[FAIL] {test_dir} (invalid expected_exit_code: {raw!r})")
            return False
    else:
        expected_exit = 0

    stdout_mismatch = actual_stdout != expected_stdout
    stderr_mismatch = actual_stderr != expected_stderr
    exit_mismatch   = exit_code != expected_exit

    ok = not (stdout_mismatch or stderr_mismatch or exit_mismatch)

    if ok:
        print(f"[ OK ] {test_dir}")
        return True

    print(f"[FAIL] {test_dir}")
    if verbose:
        if stdout_mismatch:
            print("\n(stdout mismatch)")
            print("Expected stdout:")
            print(expected_stdout)
            print("Actual stdout:")
            print(actual_stdout)

        if stderr_mismatch:
            print("\n(stderr mismatch)")
            print("Expected stderr:")
            print(expected_stderr)
            print("Actual stderr:")
            print(actual_stderr)

        if exit_mismatch:
            print("\n(exit code mismatch)")
            print(f"Expected exit: {expected_exit}")
            print(f"Actual exit:   {exit_code}")

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
            print(f"Error: test '{args.test}' not found.", file=sys.stderr)
            for name in list_available_tests():
                print(f"  - {name}")
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

    print(f"\n{succeeded} test(s) succeeded.")
    print(f"{failed} test(s) failed." if failed else "All tests passed.")

    if failed:
        sys.exit(1)

if __name__ == '__main__':
    main()

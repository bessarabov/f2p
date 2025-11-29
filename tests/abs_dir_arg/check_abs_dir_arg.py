#!/usr/bin/env python3
import os
import subprocess
import sys
import textwrap

def main():
    # We are in tests/abs_dir_arg/working_dir
    cwd = os.getcwd()

    # Repo root: tests/abs_dir_arg/check_abs_dir_arg.py -> repo/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    f2p_path = os.path.join(repo_root, 'f2p')

    # Create example directory and file inside working_dir
    example_dir = os.path.join(cwd, 'example')
    os.makedirs(example_dir, exist_ok=True)
    file_path = os.path.join(example_dir, 'file.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("file content\n")

    abs_dir = os.path.abspath(example_dir)
    abs_file = os.path.abspath(file_path)

    proc = subprocess.run(
        [f2p_path, abs_dir, '--to=stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if proc.returncode != 0:
        print(f"Expected exit code 0, got {proc.returncode}", file=sys.stderr)
        print("stderr:", proc.stderr, file=sys.stderr)
        sys.exit(1)

    expected_stdout = textwrap.dedent(f"""\
        ## File `{abs_file}`

        file content

        """)
    if proc.stdout != expected_stdout:
        print("STDOUT mismatch", file=sys.stderr)
        print("Expected:", repr(expected_stdout), file=sys.stderr)
        print("Actual:  ", repr(proc.stdout), file=sys.stderr)
        sys.exit(1)

    expected_stderr = "1 file, 4 lines\n"
    if proc.stderr != expected_stderr:
        print("STDERR mismatch", file=sys.stderr)
        print("Expected:", repr(expected_stderr), file=sys.stderr)
        print("Actual:  ", repr(proc.stderr), file=sys.stderr)
        sys.exit(1)

    # Success: no output at all, exit 0
    sys.exit(0)

if __name__ == '__main__':
    main()


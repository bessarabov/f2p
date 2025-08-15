#!/usr/bin/env python3
import subprocess
import sys
import os
import re
import difflib

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
F2P = os.path.join(REPO_ROOT, 'f2p')
README = os.path.join(REPO_ROOT, 'README.md')

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_usage_block_from_readme(md_text):
    """
    Find the first fenced code block under the '## Usage' section and return
    its contents as a string. Then drop the first line if it looks like a shell
    invocation ('$ ./f2p --help' / '$ f2p --help' / variants with -h).
    """
    # Go to '## Usage' section
    m = re.search(r'(?mi)^\s*##\s+Usage\s*$', md_text)
    if not m:
        raise RuntimeError("Couldn't find '## Usage' header in README.md")
    start = m.end()

    # Find first fenced code block after it
    fence_open = re.search(r'(?m)^```', md_text[start:])
    if not fence_open:
        raise RuntimeError("Couldn't find code fence after '## Usage' in README.md")
    block_start = start + fence_open.end()
    fence_close = re.search(r'(?m)^```', md_text[block_start:])
    if not fence_close:
        raise RuntimeError("Unclosed code fence in README.md after '## Usage'")
    block_end = block_start + fence_close.start()

    block = md_text[block_start:block_end]

    # Normalize newlines
    block = block.replace('\r\n', '\n').replace('\r', '\n')

    lines = block.split('\n')

    # 1) Drop leading blank lines inside the code fence
    while lines and lines[0].strip() == '':
        lines.pop(0)

    # 2) Remove a leading shell command line like '$ ./f2p --help' or '$ f2p -h'
    if lines and re.match(r'^\s*\$\s*(\./)?f2p\s+--?h(elp)?\s*$', lines[0]):
        lines.pop(0)
        # and then drop a single empty line if it follows
        if lines and lines[0].strip() == '':
            lines.pop(0)

    return '\n'.join(lines).rstrip('\n')

def normalize_help(s: str) -> str:
    """
    Make small, version-proof normalizations so the comparison is robust across Python versions:
      - normalize EOLs
      - trim trailing spaces
      - map 'optional arguments:' vs 'options:' heading to a single form
    """
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = '\n'.join(line.rstrip() for line in s.split('\n'))

    # Argparse changed the header name in newer Python versions.
    s = re.sub(r'(?m)^\s*optional arguments:\s*$', 'options:', s)
    s = re.sub(r'(?m)^\s*options:\s*$', 'options:', s)

    return s.strip('\n')

def main():
    # Run real program help
    try:
        proc = subprocess.run([F2P, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    except FileNotFoundError:
        print(f"Could not execute {F2P}", file=sys.stderr)
        sys.exit(2)

    real_help = proc.stdout
    readme_text = read(README)
    readme_help_block = extract_usage_block_from_readme(readme_text)

    real_norm = normalize_help(real_help)
    readme_norm = normalize_help(readme_help_block)

    if real_norm == readme_norm:
        # Success: be quiet so expected_stdout/err can be empty
        sys.exit(0)

    # Show a clear unified diff on stderr and fail
    diff = difflib.unified_diff(
        readme_norm.splitlines(),
        real_norm.splitlines(),
        fromfile='README.md (expected)',
        tofile='f2p --help (actual)',
        lineterm=''
    )
    print("\n".join(diff), file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    main()


# f2p

## Installation

Simply copy the f2p file from this repository and make it executable.

## Usage

```
$ ./f2p --help
usage:

    f2p

or:

    f2p [-o FILE]

Output the contents of text files to STDOUT.

If run without arguments, it outputs all text files in
the current directory (recursively), excluding files under .git/

If run with -o FILE1 -o FILE2, it outputs only the specified files.

optional arguments:
  -h, --help  show this help message and exit
  -o FILE     Only output the specified file (can be used multiple times)
```

# f2p

## Installation

Simply copy the `f2p` file from this repository and make it executable.

## Usage

```
$ f2p --help
usage:

    f2p

or:

    f2p [FILE_OR_DIR ...]

Output the contents of UTF-8 text files.

If run without arguments, it recursively finds all UTF-8 text files in the
current directory (respecting .gitignore and excluding .git/).

When writing to a terminal, output goes to the clipboard by default (can be changed with --to).
When piped or redirected, output goes to stdout by default.

positional arguments:
  FILE_OR_DIR           Can be specified zero or more times. Files are output
                        as-is; directories are searched recursively for text
                        UTF-8 files, respecting .gitignore

optional arguments:
  -h, --help            show this help message and exit
  --to {clipboard,stdout}
                        Destination for output. When writing to a terminal,
                        the default is clipboard (pbcopy). When the output is
                        piped or redirected, the default is stdout.
```

# f2p

## Installation

Simply copy the f2p file from this repository and make it executable.

## Usage

```
$ ./f2p --help
usage:

    f2p

or:

    f2p [FILE_OR_DIR ...]

Output the contents of text files to STDOUT.

If run without arguments, it recursively finds and outputs
all text UTF-8 files in the current directory, respecting .gitignore
and excluding files under .git/

positional arguments:
  FILE_OR_DIR  Can be specified zero or more times. Files are output as-is;
               directories are searched recursively for text UTF-8 files,
               respecting .gitignore

optional arguments:
  -h, --help   show this help message and exit
```

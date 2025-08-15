# f2p

## Installation

Simply copy the f2p file from this repository and make it executable.

## Usage

```
$ ./f2p --help
usage:

    f2p

or:

    f2p [FILE ...]

Output the contents of text files to STDOUT.

If run without arguments, it outputs all text files in
the current directory (recursively), honoring .gitignore
(and always excluding files under .git/).

If run with one or more FILE arguments, it outputs only those files.

positional arguments:
  FILE        Only output the specified file(s)

optional arguments:
  -h, --help  show this help message and exit
```

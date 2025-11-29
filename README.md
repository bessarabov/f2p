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

Output the contents of text UTF-8 files, by default copy it to the clipboard.

If run without arguments, it recursively finds all text UTF-8 files in the
current directory, respecting .gitignore and excluding files under .git/, and
outputs them to the clipboard.

positional arguments:
  FILE_OR_DIR           Can be specified zero or more times. Files are output
                        as-is; directories are searched recursively for text
                        UTF-8 files, respecting .gitignore

optional arguments:
  -h, --help            show this help message and exit
  --to {clipboard,stdout}
                        Destination for output. Default is clipboard (macOS
                        pbcopy)
```

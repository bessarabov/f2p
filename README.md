# f2p

`f2p` is a small utility created to make working with LLMs easier.

It provides a simple way to copy the contents of multiple files into one large,
readable text block that can be pasted directly into an LLM prompt.

The most common way I use it on my MacBook is simply running the tool in a
project's root directory:

```
bessarabov@m3:~/git/f2p$ f2p
58 files, 986 lines
bessarabov@m3:~/git/f2p$
```

This command finds all UTF-8 text files in the current directory and copies
their combined contents to the macOS clipboard (via pbcopy). After running it,
my clipboard contains something like (but instead of ... it contains the actual
content):

```
## File `.github/workflows/test.yml`

...

## File `LICENSE`

...

## File `README.md`

...

## f2p

...

### ...
```

Then I can paste it directly into an LLM prompt.

Sometimes I specify exactly which files I want to send to the LLM, for example:

```
f2p path/to/file.txt path/to/other_file.txt
```

It also works with directories, or with a mix of directories and individual
files, for example:

```
f2p project_a/dir/ project_b/other_dir/ /Users/bessarabov/Desktop/file.tsv
```

The name comes from "files to prompt".

This tool is intended for manual use. It is not designed to be part of
automated scripts or pipelines.

I wrote this tool for myself. It does exactly what I want. Sometimes I realize
it should behave differently, and I just change it (well, technically the LLM
changes it for me).

The absence of versioning is intentional: I don't want to spend time
maintaining a changelog, and I don't want to depend on past versions. I'm
completely fine making backward-incompatible changes whenever I feel they are
necessary. If you start using this script, be aware that I may change it in
ways that make sense for me but break your workflow.

The script is open source under the MIT License. If you find it useful, the
best approach is probably to fork it and adapt it in whatever direction fits
your needs. I doubt I will accept pull requests. I might take something
obviously useful and harmless, but in general I'm not interested in changing
this script in ways I don’t personally need.

LLMs write code well enough (especially when reviewed and corrected), so if you
need a command-line tool for easily inserting file contents into prompts, you
can use this project as a starting point and then move it in whatever direction
you want with the help of your favourite LLM.

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

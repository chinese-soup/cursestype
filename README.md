# Cursestype

## About
* A bad [MonkeyType](https://monkeytype.com) (or any generic WPM typing tester app) clone using Python's built-in curses wrapper.
* Work in progress.

## Motivation
* Just for fun

# Requirements
* Python > 3.7

# Usage
So far it's just:
```bash
$ chmod +x cursestype.py
$ ./cursestype.py "The quick brown fox jumped over the lazy dog"
```

# TODO
* TODO: keep a dictionary of currently OK chars
* TODO: don't let user go back a word if he commits it (space) like MonkeyType doesn't
* TODO: if a user backspaces a green thing (a CORRECT char), make it gray again
* TODO: Multiline w.move()s
* TODO: newlines only as text wrapping 
* TODO: don't count newlines as a character
* TODO: Menu to change language file etc.
* TODO: Languages other than ANSI english
* TODO: Language files
* TODO: Command line parameters

Note: `curses` is not supported in Windows `cmd.exe`, use Windows Subsystem for Linux.

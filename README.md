# Cursestype

## About
* A bad [MonkeyType](https://monkeytype.com) (or any generic WPM typing tester app) clone build exclusively using Python's built-in `curses` wrapper.
* Work in progress.

## Motivation
* Just for fun
### Why curses
It's built-in and no external dependencies are required.

# Requirements
* Python > 3.7

# Usage
So far it's just:
```bash
$ chmod +x cursestype.py
$ ./cursestype.py "The quick brown fox jumped over the lazy dog"
```
Note: `curses` is not supported in Windows `cmd.exe`, use Windows Subsystem for Linux.


# TODO
- [ ] keep a dictionary of currently OK chars
- [ ] don't let user go back a word if he commits it (space) like MonkeyType doesn't
- [x] if a user backspaces a green thing (a CORRECT char), make it gray again
- [ ] Multiline w.move()s
- [ ] newlines only as text wrapping
- [ ] don't count newlines as a character
- [ ] Menu to change language file etc.
- [ ] Let user specify a text file to load to type OR just generate words from language files that user selects
- [ ] Languages other than ANSI english
- [ ] Language files
- [ ] Command line parameters
- [ ] timed gamemode (15s/30s/45s/60s)

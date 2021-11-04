# Cursestype

## About
* A bad [MonkeyType](https://monkeytype.com) (or any generic WPM typing tester app) clone build exclusively using Python's built-in `curses` wrapper.
* Work in progress.

## Motivation
* Just for fun & learning about ncurses
### Why curses
It's built-in and no external dependencies are required.

# Requirements
* Python > 3.7

# Usage
So far it's just:
## Start with custom text
```bash
$ chmod +x cursestype.py
$ ./cursestype.py "The quick brown fox jumped over the lazy dog"
```
## Start with default language:
```bash
$ chmod +x cursestype.py
./cursestype.py
```
Note: `curses` is not supported in Windows `cmd.exe`, use Windows Subsystem for Linux.

# Limitations
* Only supports Latin alphabet languages

# TODO
- [ ] keep a dictionary of currently OK chars
- [ ] don't let user go back a word if he commits it (space) like MonkeyType doesn't (Confidence mode?)
- [x] if a user backspaces a green thing (a CORRECT char), make it gray again
- [ ] Multiline w.move()s
- [ ] newlines only as text wrapping
- [ ] don't count newlines as a character
- [ ] Menu to change language file etc.
- [ ] Let user specify a text file to load to type OR just generate words from language files that user selects
- [x] Languages other than ANSI english
- [ ] Language files
- [ ] Command line parameters
- [ ] Timed gamemode (15s/30s/45s/60s)
- [ ] Record & replay the run (and save replays?)
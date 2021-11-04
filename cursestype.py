#!/usr/bin/env python3

""""
* TODO: - keep a dictionary of currently OK chars
* TODO: - don't let user go back a word if he commits it (space) like MonkeyType doesn't
* TODO: - if a user backspaces a green thing (a CORRECT char), make it gray again
* TODO: Multiline w.move()s
* TODO: newlines only as text wrapping
* TODO: don't count newlines as a character
* TODO: Menu to change language file etc.
* TODO: Languages other than ANSI english
* TODO: Language files
* TODO: Command line parameters
"""

import curses
import sys
import time
import logging

L = logging.getLogger()

if len(sys.argv) > 1:
    text_str = sys.argv[1]
else:
    text_str = "The quick brown fox jumps over the lazy dog"

text = list(text_str)
words = text_str.split(" ")
word_count = len(words)

def main():
    """
    The curses.wrapper function is an optional function that
    encapsulates a number of lower-level setup and teardown
    functions, and takes a single function to run when
    the initializations have taken place.
    """
    curses.wrapper(curses_main)

def error_exit(w, msg):
    w.addstr(f"{msg}\n")
    w.addstr("Press any key to quit...")
    w.refresh()
    w.getch()
    sys.exit(1)

def curses_main(w):
    """
    This function is called curses_main to emphasise that it is
    the logical if not actual main function, called by curses.wrapper.
    Its purpose is to call several other functions to demonstrate
    some of the functionality of curses.
    """

    w.addstr("CursesType v0.1")
    w.addstr("\n")

    if not curses.has_colors():
        error_exit(w, "Unfortunately your terminal does not support colors, cannot continue.")

    w.refresh()
    w.nodelay(1)

    # TODO: Accuracy
    index = 0
    time_taken = 0.0
    start_ts = 0.0
    mistakes = 0
    current_cursor_pos = (0, 0)

    timer_started = False # TODO: Start the timer only once

    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_CYAN, -1)

    w.addstr(text_str)

    # TODO: Multiline w.move()s
    # TODO: newlines only as text wrapping
    # TODO: don't count newlines as a character
    newlines = len(text_str.split("\n")) - 1
    y, x = w.getyx()

    w.move(y - newlines, 0)

    """
    curses.napms(100)
    curses.curs_set(True)
    """

    while True:
        if index == len(text):
            w.addstr(f"\n")
            w.addstr(f"Result:\n")
            w.addstr(f"Time: {time_taken}\n")
            wpm = (word_count / time_taken) * 60
            w.addstr(f"Words per minute: {wpm}\n")
            w.addstr(f"Incorrect characters: {mistakes}\n")
            w.refresh()
            time.sleep(3)
            break

        key = w.getch()
        now_time = time.time()
        time_taken = now_time - start_ts

        # We didn't get any key this "cycle"
        if key == -1:
            continue

        char_key = chr(key)

        if char_key == text[index]:
            # CORRECT!
            # TODO: - keep a dictionary of currently OK chars
            # TODO: - don't let user go back a word if he commits it (space) like MonkeyType doesn't
            # TODO: - if a user backspaces a green thing (a CORRECT char), make it gray again
            # TODO: Multiline w.move()s
            w.addstr(char_key, curses.color_pair(2))
            w.refresh()
            index += 1

            if timer_started == False:
                start_ts = time.time()
                time_taken = 0.0001
                timer_started = True

        elif key == curses.KEY_BACKSPACE or key == 127:
            # BACKSPACE
            y, x = w.getyx()
            w.move(y, x-1)
            index -= 1

        elif key == curses.KEY_ENTER or key == 10:
            pass

        else:
            # WRONG!
            w.addstr(text[index], curses.color_pair(1))
            w.refresh()
            index += 1
            mistakes += 1

        current_cursor_pos = w.getyx()
        w.move(0, 0)
        w.clrtoeol()
        w.addstr(f"Timer: {time_taken:.2f} | Current WPM: {(word_count / time_taken) * 60} | Mistakes: {mistakes}")

        w.move(current_cursor_pos[0], current_cursor_pos[1])

if __name__ == "__main__":
    main()
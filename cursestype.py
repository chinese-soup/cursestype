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
import curses.panel
import sys
import time
import logging
import importlib  # TODO: get rid of?
import random

L = logging.getLogger()

def generate_words(lang, number_of_words):
    lang_module = importlib.import_module(f"words.{lang}")
    wordlist = lang_module.get_list()
    words = []

    for i in range(0, number_of_words): #  TODO: Select number of words
        words.append(random.choice(wordlist))

    if words:
        return " ".join(words)

gamemode = "custom text" # TODO: Customizable
gamemode_additional = 15
language = "czech" # TODO: Customizable

if len(sys.argv) > 1:
    text_str = sys.argv[1]
else:
    text_str = generate_words(language, gamemode_additional)
    if text_str:
        gamemode = f"words ({gamemode_additional})"
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
    w.addstr("\n\n")

    if not curses.has_colors():
        error_exit(w, "Unfortunately your terminal does not support colors, cannot continue.")

    w.refresh()

    """win = curses.newwin(10, 10)
    win.border(65, 66, 67, 68,
               69, 70, 71, 72)
    win.box('4', '4')
    win.addstr("AHOJ")"""

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
    curses.init_pair(3, curses.COLOR_WHITE, -1)
    curses.init_pair(4, -1, -1)
    curses.init_pair(5, -1, curses.COLOR_BLUE)

    w.addstr(text_str, curses.color_pair(3))

    # TODO: Multiline w.move()s
    # TODO: newlines only as text wrapping
    # TODO: don't count newlines as a character
    newlines = len(text_str.split("\n")) - 1
    y, x = w.getyx()

    w.move(y - newlines, 0)
    w.keypad(1)

    """
    curses.napms(100)
    curses.curs_set(True)
    """

    while True:
        if index == len(text):
            w.addstr(f"\n\n")
            w.addstr(f"Result:\n", curses.A_STANDOUT|curses.A_BOLD)
            w.addstr(f"Time: {time_taken}\n")
            wpm = (word_count / time_taken) * 60
            w.addstr(f"Words per minute: {wpm}\n")
            w.addstr(f"Incorrect characters: {mistakes}\n")
            w.refresh()
            time.sleep(3)
            break

        try: # get_wch doesnt like w.nodelay(1), get_ch likes w.nodelay(1) and returns -1
            key = w.get_wch()
            # key = w.getch()
        except:
            continue

        now_time = time.time()
        time_taken = now_time - start_ts

        # We didn't get any key this "cycle" (this is for get_ch, get_wch is above)
        if key == -1:
             continue

        #char_key = chr(key)
        char_key = key

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

        elif key == curses.KEY_BACKSPACE or key == 127 or key == "^?" or ord(key) == 127:
            # BACKSPACE
            y, x = w.getyx()
            w.move(y, x-1)
            index -= 1
            w.addstr(text[index], curses.color_pair(4))  # TODO: make white again
            w.move(y, x - 1)

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
        w.addstr(f"Timer: {time_taken:.2f} | Current WPM: {(word_count / time_taken) * 60:.2f} | Mistakes: {mistakes}\n")
        w.addstr(f"Gamemode: {gamemode} | Language: {language}")

        w.move(current_cursor_pos[0], current_cursor_pos[1])

if __name__ == "__main__":
    main()
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

def generate_words_from_wordlist(lang, number_of_words):
    lang_module = importlib.import_module(f"words.{lang}")
    wordlist = lang_module.get_list()
    words = []

    for i in range(0, number_of_words): #  TODO: Select number of words
        words.append(random.choice(wordlist))

    if words:
        return words

gamemode = "custom text" # TODO: Customizable
gamemode_additional = 30
language = "english" # TODO: Customizable

#if len(sys.argv) > 1:
#    text_str = sys.argv[1]
#else:

# TODO: CMD line options
if len(sys.argv) > 1:
    language = sys.argv[1]

words_list = generate_words_from_wordlist(language, gamemode_additional)
if words_list:
    gamemode = f"words ({gamemode_additional})"
else:
    text_str = "The quick brown fox jumps over the lazy dog"

#text = list(text_str)
#words = text_str.split(" ")
word_count = len(words_list)

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

    #w.addstr("CursesType v0.1")
    w.addstr("\n\n\n\n\n\n")
    #w.clrtoeol()
    #w.clrtobot()

    if not curses.has_colors():
        error_exit(w, "Unfortunately your terminal does not support colors, cannot continue.")

    maxy, maxx = w.getmaxyx()

    #win = curses.newwin(5, 55)
    status_win = curses.newwin(5, maxx)

    w.refresh()
    w.nodelay(1)

    # TODO: Accuracy
    index = 0
    index_y = 0
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

    # w.addstr(text_str, curses.color_pair(3))

    # w.box()
    # TODO: Multiline w.move()s
    # TODO: newlines only as text wrapping
    # TODO: don't count newlines as a character
    """newlines = len(text_str.split("\n")) - 1
    y, x = w.getyx()

    w.move(y - newlines, 0)"""

    # TODO: Shitty wordwrap here, won't work if user changes terminal size
    line = []
    lines_dict = []
    length = 0

    for x, i in enumerate(words_list):
        line.append(i)
        length += len(i)
        #if length > maxx - len(i):
        if len(line) == 3:
            length = 0
            lines_dict.append(" ".join(line) + " ") # Add a space!
            line = []

    if len(lines_dict) > 1:
        lines_dict[ len(lines_dict)-1 ] = lines_dict[-1:][0][:-1] # HACK: Remove space at the end of last line

    text = lines_dict

    for line in lines_dict:
        w.addstr(f"{line}\n", curses.color_pair(3))

    y, x = w.getyx()
    w.move(y - len(lines_dict), 0)

    w.keypad(1)

    # Draw a dummy status box, because we didn't start the test yet
    status_win.move(1, 2)
    status_win.clrtoeol()
    status_win.addstr(f"Timer: {time_taken:.2f} | Current WPM: 0.00")
    # Second status line
    status_win.move(2, 2)
    status_win.clrtoeol()
    status_win.addstr(f"Mistakes: {mistakes} | Gamemode: {gamemode} | Language: {language}")

    status_win.box()  # Rebox because we cleared to EOL
    status_win.refresh()

    """+
    curses.curs_set(True)
    curses.napms(100)
    """
    while True:
        curses.napms(1) # nap only for 1 ms so cursor doesn't go all over the place

        # We are at the end
        if index == len(text[index_y]) and index_y == len(text) - 1:
            resultwin_border = curses.newwin(10, 50, current_cursor_pos[0]+2, 2)
            resultwin = resultwin_border.derwin(2, 2)

            resultwin.addstr(f"Result:\n\n", curses.A_STANDOUT|curses.A_BOLD)
            resultwin.addstr(f"Time: ", curses.A_BOLD)
            resultwin.addstr(f"{time_taken}\n")
            wpm = (word_count / time_taken) * 60
            resultwin.addstr(f"Words per minute: ", curses.A_BOLD)
            resultwin.addstr(f"{wpm}\n")
            resultwin.addstr(f"Incorrect characters: ", curses.A_BOLD)
            resultwin.addstr(f"{mistakes}\n")
            resultwin.addstr(f"\nPress any key to quit.")
            resultwin_border.box()
            resultwin_border.refresh()
            resultwin.refresh()
            w.refresh()
            w.nodelay(0)
            curses.napms(500)
            w.get_wch()
            break
        # We are at the end of the line
        elif index == len(text[index_y]):
            index_y += 1
            index = 0
            w.move(current_cursor_pos[0] + 1, 0)

        try: # get_wch doesnt like w.nodelay(1), get_ch likes w.nodelay(1) and returns -1
            key = w.get_wch()
            # key = w.getch()
        except:
            continue

        now_time = time.time()
        time_taken = now_time - start_ts

        # We didn't get any key this "cycle" (this is for get_ch, get_wch is above)
        # if key == -1:
        #    continue

        #char_key = chr(key)
        char_key = key
        is_string = False

        curses.curs_set(True)
        # Did we get a string from get_wide_char?
        if isinstance(key, str):
            is_string = True

        if char_key == text[index_y][index]:  # CORRECT, the letter user pressed was the next letter
            # TODO: - keep a dictionary of currently OK chars
            # TODO: Multiline w.move()s
            w.addstr(char_key, curses.color_pair(2))
            w.refresh()
            index += 1

            # Start timer if we were correct on first char
            if timer_started == False:
                start_ts = time.time()
                time_taken = 0.0001
                timer_started = True

        elif not is_string:
            if key == curses.KEY_RESIZE:
                pass  # TODO: status_window_update()
            elif key == 3:
                raise KeyboardInterrupt
            else:
                pass

        elif is_string:  # The key pressed is a string, but it isn't what user was supposed to type
            if ord(key) == 127:  # BACKSPACE
                if index == 0: # We are at the beginning, don't backspace
                    continue

                y, x = w.getyx()
                w.move(y, x-1)
                index -= 1
                w.addstr(text[index_y][index], curses.color_pair(4))  # TODO: make white again
                w.move(y, x - 1)

            else:  # WRONG!
                # Next character to be typed is a space, don't let user skip it by typing anything else than space
                # TODO: Monkeytype style?:
                # TODO: "first second" -> "first" -> "tttt" -> "firsttttt second" instead of cursor standing still
                if text[index_y][index] == " ":
                    pass

                # We good, next character is anything but space, so user entered wrong char
                else:
                    w.addstr(text[index_y][index], curses.color_pair(1))
                    w.refresh()

                    index += 1
                    mistakes += 1

                # Start timer if we made a mistake on first char
                if timer_started == False:
                    start_ts = time.time()
                    time_taken = 0.0001
                    timer_started = True

        else: # TODO: eh
            pass

        # Save current cursor position (after character has been typed)
        current_cursor_pos = w.getyx()

        # First status line
        # TODO: status_window_update()
        # TODO: Change status_win to two inlined windows like the result window is

        curses.curs_set(False)
        status_win.erase()
        status_win.move(1, 2)
        status_win.clrtoeol()
        status_win.addstr(f"Timer: {time_taken:.2f} | Current WPM: {((word_count / time_taken) * 60):.2f}")
        # Second status line
        status_win.move(2, 2)
        status_win.clrtoeol()
        status_win.addstr(
            f"Mistakes: {mistakes} | Gamemode: {gamemode} | Language: {language} | Index after: {index} | Current X: {current_cursor_pos[1]}\n Index after: {index_y}| Y: {current_cursor_pos[0]}")

        status_win.box()  # Rebox because we cleared to EOL
        status_win.refresh()

        w.move(current_cursor_pos[0], current_cursor_pos[1])


def status_window_update(status_win):
    pass
    # TODO: eh
    # First status line
    status_win.clear()
    status_win.move(1, 2)
    status_win.clrtoeol()
    status_win.addstr(f"Timer: {time_taken:.2f} | Current WPM: {((word_count / time_taken) * 60):.2f}")
    # Second status line
    status_win.move(2, 2)
    status_win.clrtoeol()
    status_win.addstr(
        f"Mistakes: {mistakes} | Gamemode: {gamemode} | Language: {language} | Index after: {index} | Current X: {current_cursor_pos[1]}")

    status_win.box()  # Rebox because we cleared to EOL
    status_win.refresh()


if __name__ == "__main__":
    main()
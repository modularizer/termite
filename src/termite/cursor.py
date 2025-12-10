from typing import Literal

DETECT_MODE = "detect"
CONSOLE_MODE = "console"
TERMINAL_MODE = "terminal"

def detect():
    try:
        import curses
        curses.setupterm()
        _sc = curses.tigetstr("sc")  # save cursor
        _rc = curses.tigetstr("rc")  # restore cursor
        SAVE_CURSOR_DETECTED = _sc.decode() if _sc else ""
        RESTORE_CURSOR_DETECTED = _rc.decode() if _rc else ""
        return SAVE_CURSOR_DETECTED, RESTORE_CURSOR_DETECTED
    except:
        return "", ""

# SAVE_CURSOR_DETECTED, RESTORE_CURSOR_DETECTED = "", ""
SAVE_CURSOR_DETECTED, RESTORE_CURSOR_DETECTED = detect()


CARRIAGE_RETURN = "\r"
CLEAR_REST_OF_LINE = f"\033[K"
CLEAR_LINE = f"{CARRIAGE_RETURN}{CLEAR_REST_OF_LINE}"
ERASE_LINE="\033[2K"


settings = {
    "cursor_mode": DETECT_MODE
}

def set_cursor_mode(s: Literal["terminal", "console", "detect"]):
    settings["cursor_mode"] = s

SAVE_CURSOR_TERMINAL = "\0337"    # or "\033[s"
RESTORE_CURSOR_TERMINAL = "\0338" # or "\033[u"
SAVE_CURSOR_CONSOLE = "\033[s"
RESTORE_CURSOR_CONSOLE = "\033[u"


def save():
    c = settings["cursor_mode"]
    return SAVE_CURSOR_DETECTED if c == DETECT_MODE else SAVE_CURSOR_TERMINAL if c == TERMINAL_MODE else SAVE_CURSOR_CONSOLE


def restore():
    c = settings["cursor_mode"]
    return RESTORE_CURSOR_DETECTED if c == DETECT_MODE else  RESTORE_CURSOR_TERMINAL if c == TERMINAL_MODE else RESTORE_CURSOR_CONSOLE

def left(n=1):
    return f"\033[{n}D"

def right(n=1):
    return f"\033[{n}C"

def up(n=1):
    return f"\033[{n}A"

def down(n=1):
    return f"\033[{n}B"

def col(n=0):
    if n == 0:
        return "\r"
    return f"\033[{n+1}G"

def pos(row, col):
    return f"\033[{row+1};{col+1}H"

def row(n):
    return f"\033[{n+1}d"


def clear_line():
    return CLEAR_LINE


def erase_line():
    return ERASE_LINE


def backspace():
    return "\033[1D \033[1D"


def replace(ch=" "):
    return ch + left()


def write_ahead(text: str):
    return save() + text + restore()


#
# cursor_actions = [
#     "POS", "LEFT", "RIGHT", "UP", "DOWN", "ROW", "COL",
#     "SAVE", "RESTORE", "WRITE_AHEAD", "CLEAR_LINE", ""
# ]

funcs = {
    "WRITEAHEAD": write_ahead,
    "REPLACE": replace,
    "BACKSPACE": backspace,
    "ERASE": erase_line,
    "ERASELINE": erase_line,
    "CLEAR": clear_line,
    "LEFT": left,
    "RIGHT": right,
    "UP": up,
    "DOWN": down,
    "ROW": row,
    "COL": col,
    "POS": pos,
    "WA": write_ahead,
    "SAVE": save,
    "RESTORE": restore
}



_consts = {
    "LEFT": left(),
    "RIGHT": right(),
    "UP": up(),
    "DOWN": down(),
    "CLEAR": CLEAR_LINE,
    "ERASE": ERASE_LINE,
    "CLEAR_LINE": CLEAR_LINE,
    "ERASE_LINE": ERASE_LINE,
    "CLEAR_REST": CLEAR_REST_OF_LINE,
    "CLEAR_REST_OF_LINE": CLEAR_REST_OF_LINE,
    "SAVE": save(),
    "RESTORE": restore()
}

class CursorConsts:
    def __getitem__(self, item):
        k = item.upper().replace("_", "")
        return _consts[k]

    def __getattr__(self, item):
        return self[item]

    def __contains__(self, item):
        return item.upper().replace("_", "") in _consts

consts = CursorConsts()

class Cursor:
    consts = consts

    def __getitem__(self, item):
        k = item.upper().replace("_", "")
        return funcs[k]

    def __getattr__(self, item):
        return self[item]

    def __contains__(self, item):
        return item.upper().replace("_", "") in funcs

cursor = Cursor()

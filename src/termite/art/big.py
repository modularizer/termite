
alphabet = """
▗▞▚▖ █▀▜▖ ▟▛▀▚ █▀▜▖ █▀▀▀ █▀▀▀ ▟▛▀▚ █  █ ▝▜▛▘   █  █ ▜▛ █    █  █ █  █ ▗▛▜▖ █▀▜▖ ▗▛▜▖ █▀▜▖ ▟▀▀▚ ▀▜▛▀ █  █ ▙  ▟ █  █ ▜▖▗▛ ▜▖▗▛ ▀▀▜█
▟▂▂▙ █▀▜▖ █    █  █ █▀▀  █▀▀  █ ▗▄ █▀▀█  ▐▌    █  █▜▌  █    █▚▞█ █▚ █ █  █ █▄▟▘ █  █ █▄▟▘ ▝▜▙▖  ▐▌  █  █ █  █ ▌▗▖▐  ██   ██  ▗▄▛▘
█  █ █▄▟▘ ▜▙▄▞ █▄▟▘ █▄▄▄ █    ▜▙▄▞ █  █ ▗▟▙▖▝▙▄▛  █ ▝▙ █▄▄▄ █  █ █ ▚█ ▝▙▟▘ █    ▝▙▟▙ █ ▝▙ ▚▄▄▛  ▐▌  ▜▇▇▛ ▝▙▟▘ ▜▘▝▛ ▟▘▝▙  ▐▌  █▙▄▄
"""
special = """
▗▛▜▖  ▐▌            ▗▖        ▗▖    ▗▄  ▟▄▙  ▐▌  ▜▖      ▗▛ ▜▖   ▗▛   ▐▛▘ ▝▜▌  ▗▛▜▖ ▗▐▗   ▘ ▗▛  ▞▚ ▗▛▛▖  ▌     ▌▌   ▚         
 ▗▟▘  ▐▌                  ▄▄       ▐▗▚▌ ▐ ▌  ▐▌   ▜▙    ▟▛   █   █    ▐▌   ▐▌   ▜▙   ▝     ▟▛       ▜▙                        ▟▙   
 ▗▖   ▗▖  ▗▖   ▟▘   ▝▘        ▟▘    ▝▀▀ ▜▀▛  ▐▌    ▝▙  ▟▘   ▟▘   ▝▙   ▐▙▖ ▗▟▌  ▝▙▟▙       ▟▘ ▗     ▝▟▟                  ▂▂▂▂  ▜▛
"""

lines = alphabet.splitlines()[1:]

BIG_LETTERS = []
for i in range(26):
    letter = "\n".join([x[5*i:5*i+4] for x in lines])
    BIG_LETTERS.append(letter)
    # print(letter)

slines = special.splitlines()[1:]
BIG_CHARS = []
for i in range(26):
    letter = "\n".join([x[5*i:5*i+4] for x in slines])
    BIG_CHARS.append(letter)
    # print(letter)


BIG_A, BIG_B, BIG_C, BIG_D, BIG_E, BIG_F, BIG_G, BIG_H, BIG_I, BIG_J, BIG_K, BIG_L, BIG_M, BIG_N, BIG_O, BIG_P, BIG_Q, BIG_R, BIG_S, BIG_T, BIG_U, BIG_V, BIG_W, BIG_X, BIG_Y, BIG_Z = BIG_LETTERS

BIG_QUESTION, BIG_EXCLAMATION, BIG_PERIOD, BIG_COMMA, BIG_COLON, BIG_DASH, BIG_SEMICOLON, BIG_AT, BIG_HASH, BIG_PIPE, BIG_FORWARD_SLASH, BIG_BACK_SLASH, BIG_CLOSE_PARENTH, BIG_OPEN_PARENTH, BIG_OPEN_BRACKET, BIG_CLOSE_BRACKET, BIG_AMP, BIG_AST, BIG_PCT, BIG_CARAT, BIG_DOLLAR, BIG_SINGLE_QUOTE, BIG_QUOTE, BIG_TICK, BIG_UNDERSCORE, BIG_PLUS  = BIG_CHARS

BIG_MAP = {
    "?": BIG_QUESTION,
    "!": BIG_EXCLAMATION,
    ".": BIG_PERIOD,
    ",": BIG_COMMA,
    "-": BIG_DASH,
    ";": BIG_SEMICOLON,
    "@": BIG_AT,
    "#": BIG_HASH,
    "|": BIG_PIPE,
    "/": BIG_FORWARD_SLASH,
    "\\": BIG_BACK_SLASH,
    "(": BIG_OPEN_PARENTH,
    ")": BIG_CLOSE_PARENTH,
    "[": BIG_OPEN_BRACKET,
    "]": BIG_CLOSE_BRACKET,
    "&": BIG_AMP,
    "*": BIG_AST,
    "%": BIG_PCT,
    "^": BIG_CARAT,
    "$": BIG_DOLLAR,
    "'": BIG_SINGLE_QUOTE,
    '"': BIG_QUOTE,
    "`": BIG_TICK,
    "_": BIG_UNDERSCORE,
    "+": BIG_PLUS,

    "A": BIG_A,
    "B": BIG_B,
    "C": BIG_C,
    "D": BIG_D,
    "E": BIG_E,
    "F": BIG_F,
    "G": BIG_G,
    "H": BIG_H,
    "I": BIG_I,
    "J": BIG_J,
    "K": BIG_K,
    "L": BIG_L,
    "M": BIG_M,
    "N": BIG_N,
    "O": BIG_O,
    "P": BIG_P,
    "Q": BIG_Q,
    "R": BIG_R,
    "S": BIG_S,
    "T": BIG_T,
    "U": BIG_U,
    "V": BIG_V,
    "W": BIG_W,
    "X": BIG_X,
    "Y": BIG_Y,
    "Z": BIG_Z,
}



def big_text(s: str):
    lines = s.splitlines()
    out = ""
    for line in lines:
        if not line:
            out += "\n"
            continue

        rows = ["", "", ""]
        for ch in line:
            up = ch.upper()

            if up in BIG_MAP:
                big = BIG_MAP[up].splitlines()
            elif ch == " ":
                big = ["    ", "    ", "    "]  # width of one char
            else:
                big = ["    ", "    ", "    "]  # unknown char

            for i in range(3):
                rows[i] += big[i] + " "

        out += "\n".join(rows) + "\n"

    return out.rstrip("\n")



def bigprint(s: str):
    print(big_text(s))

big = big_text

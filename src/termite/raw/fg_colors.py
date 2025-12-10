
RESET = "\033[0m"


# === Standard Foreground Colors ===
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
LIGHT_GRAY  = "\033[37m"
LIGHT_GREY  = "\033[37m"
BRIGHT_BLACK   = "\033[90m"
GRAY   = "\033[90m"
GREY  = "\033[90m"
BRIGHT_RED     = "\033[91m"
BRIGHT_GREEN   = "\033[92m"
BRIGHT_YELLOW  = "\033[93m"
BRIGHT_BLUE    = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN    = "\033[96m"
BRIGHT_WHITE   = "\033[97m"


FG_RGB_HEADER = "\033[38;2;"
def FG_RGB(r: int, g: int, b: int):
    return f"{FG_RGB_HEADER}{r};{g};{b}m"


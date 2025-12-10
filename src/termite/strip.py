import re
from typing import List

# Match any CSI sequence: ESC [ params cmd
CSI_RE = re.compile(r"\x1b\[([0-9;]*)([A-Za-z])")

# SGR parameter sets
FG_CODES = {
    30, 31, 32, 33, 34, 35, 36, 37, 39,
    90, 91, 92, 93, 94, 95, 96, 97,
}
BG_CODES = {
    40, 41, 42, 43, 44, 45, 46, 47, 49,
    100, 101, 102, 103, 104, 105, 106, 107,
}
STYLE_CODES = {
    1, 2, 3, 4, 5, 7, 8, 9,
    21, 22, 23, 24, 25, 27, 28, 29,
    51, 52, 53, 54, 55,
}
# Extended color SGR introducers: 38 (fg), 48 (bg), 58 (underline color)
EXT_COLOR_CODES = {38, 48, 58}

# CSI commands that move the cursor (we'll remove these when requested)
CURSOR_CMDS = {
    "A",  # CUU - cursor up
    "B",  # CUD - cursor down
    "C",  # CUF - cursor forward (right)
    "D",  # CUB - cursor backward (left)
    "E",  # CNL - cursor next line
    "F",  # CPL - cursor previous line
    "G",  # CHA - cursor horizontal absolute
    "H",  # CUP - cursor position
    "f",  # HVP - horizontal & vertical position (alias)
    "S",  # SU - scroll up
    "T",  # SD - scroll down
}


def _parse_sgr_params(params_str: str) -> List[int]:
    if params_str == "" or params_str is None:
        return [0]
    return [int(p) if p else 0 for p in params_str.split(";")]


def _filter_sgr_params(
        params: List[int],
        remove_fg_colors: bool,
        remove_bg_colors: bool,
        remove_styles: bool,
        remove_reset: bool,
) -> List[int]:
    """
    Filter SGR param list according to flags.
    Handles basic colors, styles, and extended colors (38/48/58).
    """
    kept: List[int] = []
    i = 0
    n = len(params)

    while i < n:
        p = params[i]

        # Reset
        if p == 0:
            if not remove_reset:
                kept.append(p)
            i += 1
            continue

        # Styles (bold, underline, etc.)
        if p in STYLE_CODES:
            if not remove_styles:
                kept.append(p)
            i += 1
            continue

        # Simple foreground
        if p in FG_CODES:
            if not remove_fg_colors:
                kept.append(p)
            i += 1
            continue

        # Simple background
        if p in BG_CODES:
            if not remove_bg_colors:
                kept.append(p)
            i += 1
            continue

        # Extended color (38/48/58)
        if p in EXT_COLOR_CODES:
            # figure out sequence length: 38;5;n or 38;2;r;g;b
            mode = params[i + 1] if i + 1 < n else None
            if mode == 5:
                seq_len = 3  # p, 5, n
            elif mode == 2:
                seq_len = 5  # p, 2, r, g, b
            else:
                # malformed / unknown; just treat as single param
                seq_len = 1

            # decide whether to remove this whole extended-color sequence
            if p == 38:  # fg
                remove_this = remove_fg_colors
            elif p == 48:  # bg
                remove_this = remove_bg_colors
            else:  # 58: underline color; treat as a "style color"
                remove_this = remove_styles

            if not remove_this:
                kept.extend(params[i : i + seq_len])

            i += seq_len
            continue

        # Unknown param -> keep
        kept.append(p)
        i += 1

    return kept


def strip_text(
        s: str,
        remove_fg_colors: bool = True,   # remove foreground colors, including rgb
        remove_bg_colors: bool = True,   # remove background colors, including rgb
        remove_styles: bool = True,      # remove styles like bold, italic, etc
        remove_cursor_actions: bool = True,  # remove CSI cursor movement sequences
        remove_reset: bool | None = None,
) -> str:
    """
    Strip / filter ANSI CSI sequences in `s` according to flags.
    - Only touches CSI sequences (ESC [ ... cmd).
    - SGR ('m') codes are filtered by color/style flags.
    - Cursor movement CSI commands are removed when remove_cursor_actions=True.
    - Other CSI commands (e.g. clear screen 'J', 'K') are left untouched.
    """
    # print(f"stripping: {s!r}")
    if remove_reset is None:
        # default: reset is removed iff we're removing all three categories
        remove_reset = remove_fg_colors and remove_bg_colors and remove_styles

    def repl(m: re.Match) -> str:
        params_str, cmd = m.groups()

        # SGR: ESC [ ... m
        if cmd == "m":
            params = _parse_sgr_params(params_str)
            filtered = _filter_sgr_params(
                params,
                remove_fg_colors=remove_fg_colors,
                remove_bg_colors=remove_bg_colors,
                remove_styles=remove_styles,
                remove_reset=remove_reset,
            )
            if not filtered:
                return ""  # drop entire SGR
            return "\x1b[" + ";".join(str(p) for p in filtered) + "m"

        # Other CSI commands (e.g. J/K clear) -> keep as-is
        return m.group(0)

    r =CSI_RE.sub(repl, s)
    
    if remove_cursor_actions:
        r = _sim_text(r)
    # print(f"returning: {r!r}")
    return r





def _parse_csi_nums(params_str: str) -> list[int]:
    if not params_str:
        return [1]
    parts = params_str.split(";")
    nums = []
    for p in parts:
        if p == "":
            nums.append(0)
        else:
            try:
                nums.append(int(p))
            except ValueError:
                nums.append(0)
    if not nums:
        nums = [1]
    return nums


def _sim_text(s: str) -> str:
    """
    Simulate a tiny terminal on text `s`:

    - First strips colors/styles (SGR) but keeps cursor movement and clears.
    - Handles:
        ESC[nD  (left)
        ESC[nC  (right)
        ESC[nG  (goto column)
        ESC[nH / ESC[n;mf  (row/column) -> we only use column
        ESC[E/F  (next/prev line) -> we start new lines
    - Overwrites characters when the cursor moves back and prints more.
    - Newlines in the input start a new simulated line.
    - Vertical cursor moves (A/B/S/T) are ignored for now (no 2D buffer).
    """
    

    lines: list[str] = []
    buf: list[str] = []
    cursor = 0

    i = 0
    n = len(s)

    while i < n:
        ch = s[i]

        # newline -> commit line, reset buffer/cursor
        if ch == "\n":
            lines.append("".join(buf))
            buf = []
            cursor = 0
            i += 1
            continue

        # Try to parse CSI
        if ch == "\x1b" and i + 1 < n and s[i + 1] == "[":
            m = CSI_RE.match(s, i)
            if not m:
                # malformed, just skip ESC
                i += 1
                continue

            params_str, cmd = m.groups()
            i = m.end()

            if cmd not in CURSOR_CMDS:
                # non-cursor CSI (e.g. J/K clears) -> ignore for layout
                continue

            nums = _parse_csi_nums(params_str)

            if cmd == "D":  # left
                count = nums[0] or 1
                cursor = max(0, cursor - count)

            elif cmd == "C":  # right
                count = nums[0] or 1
                cursor = max(0, cursor + count)

            elif cmd in ("G",):  # goto column
                col = nums[0] or 1
                cursor = max(0, col - 1)

            elif cmd in ("H", "f"):  # row/column; we only care about column
                # ESC[row;colH  (1-based); default row/col = 1
                col = nums[1] if len(nums) >= 2 else nums[0]
                if col < 1:
                    col = 1
                cursor = col - 1
                # we ignore row here (no 2D buffer)

            elif cmd in ("E", "F"):  # next/prev line
                # Commit current line and start a new one
                lines.append("".join(buf))
                buf = []
                cursor = 0

            # A, B, S, T (vertical moves/scroll) we just ignore in this 1D model

            continue

        # Printable char -> write/overwrite at cursor
        if ch >= " " and ch != "\x7f":
            if cursor >= len(buf):
                # pad with spaces if cursor jumped ahead
                buf.extend(" " for _ in range(cursor - len(buf)))
                buf.append(ch)
            else:
                buf[cursor] = ch
            cursor += 1

        i += 1

    # Flush last line
    if buf or not lines:
        lines.append("".join(buf))

    s = "\n".join(lines).rstrip("\n")
    return s


def stripped_length(s, **kw):
    return len(strip_text(s, **kw))


if __name__ == "__main__":
    # from termite import cprint
    # s = cprint("text", completion="answer", print=None)
    # s2 = strip_text(s)
    print("abcdefg\x1b[3DXY")
    print(strip_text("abcdefg\x1b[3DXY"))
    # -> "abcdXYg"  (7 chars, overwrite in the middle)
    
    print("hello\x1b[2D!!")
    print(strip_text("hello\x1b[2D!!"))
    # -> "hel!!"
    
    print("one line\nsecond\x1b[3DXXX")
    print(strip_text("one line\nsecond\x1b[3DXXX"))
# -> "one line\nseXXXd"
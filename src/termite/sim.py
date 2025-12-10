import re
from dataclasses import dataclass

CSI_RE = re.compile(r"\x1b\[([0-9;]*)([A-Za-z])")

CURSOR_CMDS = {
    "A",  # up      (ignored in 1D)
    "B",  # down    (ignored)
    "C",  # right
    "D",  # left
    "E",  # next line
    "F",  # prev line
    "G",  # goto column
    "H",  # row/column
    "f",  # row/column
    "S",  # scroll up   (ignored)
    "T",  # scroll down (ignored)
}


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

RESET = "\x1b[0m"



class Cell:
    def __init__(self, ch: str, sgr: str = ""):
        self.ch = ch
        self.sgr = sgr
        self.raw = ch
        self.styled = sgr + ch + RESET

    def __str__(self):
        return self.styled

    def __repr__(self):
        return self.ch

def encode_cells(cell_lines: list[list[Cell]] | list[Cell] | Cell) -> str:
    """
    Turn Cell structure back into ANSI text with minimal SGR sequences.
    """
    if not cell_lines:
        return ""
    if not isinstance(cell_lines, list):
        cell_lines = [cell_lines]
    if not isinstance(cell_lines[0], list):
        cell_lines = [cell_lines]
    out_lines: list[str] = []
    prev_sgr = ""  # styling active at last printed char

    for line in cell_lines:
        parts: list[str] = []

        for cell in line:
            # style change?
            if cell.sgr != prev_sgr:
                # need a reset?
                if cell.sgr == "":
                    parts.append(RESET)
                else:
                    parts.append(cell.sgr)

                prev_sgr = cell.sgr

            parts.append(cell.ch)

        # end-of-line cleanup
        if prev_sgr:
            # reset at line boundary so next line starts cleanly
            parts.append(RESET)
            prev_sgr = ""

        out_lines.append("".join(parts))

    return "\n".join(out_lines)

def merge_unstyled_cells(cell_lines: list[list[Cell]] | list[Cell] | Cell) -> str:
    if not cell_lines:
        return ""
    if not isinstance(cell_lines, list):
        cell_lines = [cell_lines]
    if not isinstance(cell_lines[0], list):
        cell_lines = [cell_lines]
    return "\n".join("".join(ch.ch for ch in line) for line in cell_lines)


class CellLines(list):
    @property
    def styled(self):
        return encode_cells(self)

    @property
    def raw(self):
        return merge_unstyled_cells(self)

    @property
    def size(self):
        r = self.raw
        lines = r.splitlines()
        rows = len(lines)
        cols = max([len(x) for x in lines])
        return rows, cols

    @property
    def width(self):
        return self.size[1]

    @property
    def height(self):
        return self.size[0]

    @property
    def cols(self):
        return self.width

    @property
    def rows(self):
        return self.height

    def __getitem__(self, item):
        x = super().__getitem__(item)
        return CellLines(x) if isinstance(x, list) else ""

    def __str__(self):
        return self.styled


def sim(s: str) -> CellLines:
    """
    Simulate a 1D terminal with:
      - SGR ('m') tracked as current style
      - cursor movement CSI handled (left/right/column/next/prev line)
      - printable chars overwrite at cursor
    Returns: list of lines, each a list[Cell].
    """
    lines: list[list[Cell]] = [[]]
    cursor = 0
    current_sgr = ""  # raw SGR string (e.g. "\x1b[31m")

    i = 0
    n = len(s)

    while i < n:
        ch = s[i]

        # Newline: commit line, start next
        if ch == "\n":
            lines.append([])
            cursor = 0
            i += 1
            continue

        # CSI sequence?
        if ch == "\x1b" and i + 1 < n and s[i + 1] == "[":
            m = CSI_RE.match(s, i)
            if not m:
                i += 1
                continue

            params_str, cmd = m.groups()
            i = m.end()

            # SGR (style/color)
            if cmd == "m":
                # normalize back to a single SGR sequence string
                if params_str == "":
                    current_sgr = "\x1b[0m"
                else:
                    current_sgr = f"\x1b[{params_str}m"
                continue

            # Cursor movement
            if cmd in CURSOR_CMDS:
                nums = _parse_csi_nums(params_str)

                if cmd == "D":  # left
                    count = nums[0] or 1
                    cursor = max(0, cursor - count)

                elif cmd == "C":  # right
                    count = nums[0] or 1
                    cursor = max(0, cursor + count)

                elif cmd == "G":  # goto column (1-based)
                    col = nums[0] or 1
                    cursor = max(0, col - 1)

                elif cmd in ("H", "f"):  # row/col; we only care about col
                    col = nums[1] if len(nums) >= 2 else nums[0]
                    if col < 1:
                        col = 1
                    cursor = col - 1

                elif cmd in ("E", "F"):
                    # next/prev line: start a new logical line
                    lines.append([])
                    cursor = 0

                # A/B/S/T (vertical/scroll) ignored in this 1D model
                continue

            # Other CSI (J, K, etc.) ignored for layout
            continue

        # Printable char: write/overwrite at cursor
        if ch >= " " and ch != "\x7f":
            line = lines[-1]
            if cursor >= len(line):
                # pad with unstyled spaces if we jumped ahead
                while len(line) < cursor:
                    line.append(Cell(" ", sgr=""))
                line.append(Cell(ch, sgr=current_sgr))
            else:
                line[cursor] = Cell(ch, current_sgr)
            cursor += 1

        i += 1

    # Ensure at least one line
    if not lines:
        lines = CellLines([[]])

    return CellLines(lines)


if __name__ == "__main__":
    s = sim("this is a text")
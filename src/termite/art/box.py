from termite.colors import get_color
from termite.raw import RESET
from termite.sim import sim, CellLines


def box(text: str, bg: str ="", border: str = "", text_color="black") -> str:
    lines = sim(text)
    width = lines.width
    bg = get_color("", bg) if bg else ""
    bc = get_color(border) if border else ""
    tc = get_color(text_color)
    top    = bg + bc +  "┌" + "─" * (width + 2) + "┐" + RESET + "\n"

    s = top
    for line in lines:
        c = CellLines(line)
        s += ( bg + bc + "│ " + RESET + bg + tc + c.styled.replace(RESET, RESET+bg+tc) + (width - len(c.raw)) * " " + RESET + bg + bc + " │" + RESET + "\n")
    bottom =  bg + bc + "└" + "─" * (width + 2) + "┘" + RESET
    s += bottom
    return s

def space_box(text: str, bg: str ="", padding: int = 0) -> str:
    lines = sim(text)
    width = lines.width
    bg = get_color("", bg) if bg else ""

    s = ""
    for line in lines:
        c = CellLines(line)
        s += ( bg + " " * padding + c.styled.replace(RESET, RESET+bg) + (width - len(c.raw)) * " "  + " " * padding + RESET + bg  + RESET + "\n")
    return s


def get_spaced_underline(text: str, ch = "─", padding: int = 0) -> str:
    lines = sim(text)
    width = lines.width + 2*padding
    return ch * width

def spaced_underline(text: str, indent=" ", ch = "─") -> str:
    lines = sim(text)
    width = lines.width + 2 * len(indent) + 1
    return indent_text(lines.styled, indent, indent + " ") + "\n" + ch * width

def indent_text(text, indent="  ", end_indent=""):
    return f"\n".join(f"{indent}{k}{end_indent}" for k in text.splitlines())

if __name__ == "__main__":
    from termite.sub import sub
    s = sim("This is a test")
    print(box(sub("GREEN[This is a test]"), border="RED", bg="GRAY"))
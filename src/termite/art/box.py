from termite.colors import get_color
from termite.raw import RESET
from termite.sim import sim, CellLines


def box(text: str) -> str:
    lines = sim(text)
    width = lines.width
    top    = "┌" + "─" * (width + 2) + "┐" + "\n"

    s = top
    for line in lines:
        c = CellLines(line)
        s += ( "│ " + c.styled + (width - len(c.raw)) * " " + " │" +  "\n")
    bottom = "└" + "─" * (width + 2) + "┘" + RESET
    s += bottom
    return s


if __name__ == "__main__":
    from termite.sub import sub
    s = sim("This is a test")
    print(box(sub("GREEN[This is a test]"), border="RED"))
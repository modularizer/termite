from termite.colors import FGColors, BGColors, get_color, FGRGBTerminalCode, BGRGBTerminalCode, settings, demo_color, register_terminal_color
from termite.tc import TerminalCode, BaseColor
from termite.raw import RESET
from termite.cases import cases
from termite.cursor import cursor
from termite.emojis import emojis
from termite.unicode import unicode
from termite.styles import styles, get_style


fg = FGColors()
bg = BGColors()

class FancyText:
    fg = fg
    bg = bg
    styles = styles
    cases = cases
    cursor = cursor
    emojis = emojis
    unicode = unicode
    reset = RESET
    RESET = RESET
    rst = RESET
    RST = RESET

    demo_color=staticmethod(demo_color)
    register_terminal_color = staticmethod(register_terminal_color)
    get_color = staticmethod(get_color)


    def __getattr__(self, item):
        return self.get_item(item)


    def __getitem__(self, item):
        return self.get_item(item)

    @property
    def terminal_color(self):
        return settings["tc"]

    @terminal_color.setter
    def terminal_color(self, value):
        settings["tc"] = value

    def get_item(self, item):
        if isinstance(item, TerminalCode):
            return item
        if item in self.cases:
            return self.cases[item]
        if item in self.cursor:
            return self.cursor[item]
        if item in self.emojis:
            return self.emojis[item]
        if item in self.unicode:
            return self.unicode[item]
        s = get_style(item)
        if s:
            return s
        name = TerminalCode.normname(item)
        if name.startswith("bg"):
            return TerminalCode.retrieve(name[2:], "bg") or BGRGBTerminalCode(name[2:])
        return TerminalCode.retrieve(item, "fg") or FGRGBTerminalCode(item)

    def __contains__(self, item):
        try:
            if item in self.cases or item in self.cursor or item in self.emojis or item in self.unicode:
                return True
            return self[item] is not None
        except:
            return False

    def __iter__(self):
        return iter({"styles": styles, "fg": fg, "bg": bg, "unicode": self.unicode, "emojis": self.emojis, "cases": self.cases, "cursor": self.cursor})

    def __call__(self,
                 foreground: BaseColor | TerminalCode | None = None,
                 background: BaseColor | TerminalCode | None = None,
                 style: list[str] | str = "",
                 terminal_color: str | None = None
                 ):
        return get_color(foreground=foreground, background=background, style=style, terminal_color=terminal_color)

    def full_demo(self):
        for k in self.fg:
            self.demo_color(k)
        for k in self.bg:
            self.demo_color(background=k)
        for k in self.styles:
            self.demo_color(style=k)

t = FancyText()
text = t


if __name__ == "__main__":
    t.full_demo()

    others = [
        "#343",
        "#797",
        "#249823",
        "#249823AA"
    ]
    for k in others:
        t.demo_color(k)

    t.demo_color("lime", "maroon")
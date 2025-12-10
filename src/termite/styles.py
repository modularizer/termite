# === Text Attributes ===
from termite.tc import TC, TerminalCode
import termite.raw as r

BOLD       = TC(r.BOLD      , "bold", "styles")
DIM        = TC(r.DIM       , "dim", "styles")
ITALIC     = TC(r.ITALIC    , "italic", "styles")
UNDERLINE  = TC(r.UNDERLINE , "underline", "styles")
BLINK      = TC(r.BLINK     , "blink", "styles")     # rarely supported, and often disabled
REVERSE    = TC(r.REVERSE   , "reverse", "styles")     # swap fg/bg
HIDDEN     = TC(r.HIDDEN    , "hidden", "styles")     # used for passwords
PASSWORD     = TC(r.HIDDEN    , "password", "styles")     # used for passwords
STRIKETHROUGH = TC(r.STRIKETHROUGH, "strikethrough", "styles")

class Styles:
    def __getattr__(self, item):
        return get_style(item)

    def __getitem__(self, item):
        return get_style(item)

    def __iter__(self):
        return iter(TerminalCode.registry.get("styles", {}))

    def __dir__(self):
        return list(TerminalCode.registry.get("styles", {}))

    def __contains__(self, item):
        return item.lower() in TerminalCode.registry.get("styles", {})


styles = Styles()


def get_style(style: list[str] | str | None = None):
    if isinstance(style, TerminalCode):
        return style
    if not style:
        return TerminalCode("", "empty", "styles")
    known_styles = TerminalCode.registry.get("styles", "")
    style = TerminalCode.normname(style) if isinstance(style, str) else [c if isinstance(c, TerminalCode) else TerminalCode.normname(c)  for c in style]
    if isinstance(style, str) and not all(c in known_styles for c in style):
        style = [style]
    s = TerminalCode.retrieve(style[0], "styles")
    if s is None:
        return TerminalCode("", "empty", "styles")
    for c in style[1:]:
        x = TerminalCode.retrieve(c, "styles")
        if x is None:
            x = TerminalCode("", "empty", "styles")
        s += x
    return s
import termite.raw as r
from termite.cases import cases
from termite.styles import get_style
from termite.tc import TerminalCode, TC, to_rgba, BaseColor

RESET = TC(r.RESET, "reset", "fg", "bg", "styles")



# === Standard Foreground Colors ===
b=0
blu = 238
v=205
w=229
f=255
h =127
t = 92
BLACK = TC(r.BLACK, "black", "fg", rgb=(b,b,b))
RED   = TC(r.RED  , "red", "fg", rgb=(v, b, b))
GREEN = TC(r.GREEN, "green", "fg", rgb=(b, v, b))
YELLOW  = TC(r.YELLOW, "yellow", "fg", rgb=(v, v, b))
BLUE  = TC(r.BLUE , "blue", "fg", rgb=(b, b, blu))
MAGENTA = TC(r.MAGENTA, "magenta", "fg", rgb=(v, b, v))
CYAN  = TC(r.CYAN , "cyan", "fg", rgb=(b, v, v))
WHITE = TC(r.WHITE, "white", "fg", rgb=(w,w,w))
LIGHT_GRAY  = TC(r.LIGHT_GRAY, "lightgray", "fg", rgb=(w,w,w))
LIGHT_GREY  = TC(r.LIGHT_GREY, "lightgrey", "fg", rgb=(w,w,w))
BRIGHT_BLACK = TC(r.BRIGHT_BLACK, "brightblack", "fg", rgb=(h, h, h))
GRAY = TC(r.GRAY, "gray", "fg", rgb=(h, h, h))
GREY  = TC(r.GREY, "grey", "fg", rgb=(h, h, h))
BRIGHT_RED   = TC(r.BRIGHT_RED  , "brightred", "fg", rgb = (f, b, b))
BRIGHT_GREEN = TC(r.BRIGHT_GREEN, "brightgreen", "fg", rgb = (b, f, b))
BRIGHT_YELLOW  = TC(r.BRIGHT_YELLOW, "brightyellow", "fg", rgb = (f, f, b))
BRIGHT_BLUE  = TC(r.BRIGHT_BLUE , "brightblue", "fg", rgb=(t, t, f))
BRIGHT_MAGENTA = TC(r.BRIGHT_MAGENTA, "brightmagenta", "fg", rgb=(f, b, f))
BRIGHT_CYAN  = TC(r.BRIGHT_CYAN , "brightcyan", "fg", rgb=(b, f, f))
BRIGHT_WHITE = TC(r.BRIGHT_WHITE, "brightwhite", "fg", rgb=(f,f, f))


class FGRGBTerminalCode(TerminalCode):
    def __new__(cls, rgb: BaseColor, name: str = "unknown", *groups: str):
        rgb: BaseColor = to_rgba(rgb)[:3]
        c = r.FG_RGB(*rgb)
        # print("foreground", rgb, name, repr(c)[1:-1])
        groups = groups or ("unknown",)
        groups = [cls.normname(n) for n in groups]
        for g in ("rgb", "fg"):
            if g not in groups:
                groups.append(g)
        return super().__new__(cls,
                               c,
                               name,
                               *groups,
                               rgb=rgb)


DARKRED = FGRGBTerminalCode(r.DARKRED_HEX, "darkred")
DARKGREEN = FGRGBTerminalCode(r.DARKGREEN_HEX, "darkgreen")
DARKBLUE = FGRGBTerminalCode(r.DARKBLUE_HEX, "darkblue")
DARKCYAN = FGRGBTerminalCode(r.DARKCYAN_HEX, "darkcyan")
DARKMAGENTA = FGRGBTerminalCode(r.DARKMAGENTA_HEX, "darkmagenta")
DARKYELLOW = FGRGBTerminalCode(r.DARKYELLOW_HEX, "darkyellow")
LIGHTRED = FGRGBTerminalCode(r.LIGHTRED_HEX, "lightred")
LIGHTGREEN = FGRGBTerminalCode(r.LIGHTGREEN_HEX, "lightgreen")
LIGHTBLUE = FGRGBTerminalCode(r.LIGHTBLUE_HEX, "lightblue")
LIGHTCYAN = FGRGBTerminalCode(r.LIGHTCYAN_HEX, "lightcyan")
LIGHTMAGENTA = FGRGBTerminalCode(r.LIGHTMAGENTA_HEX, "lightmagenta")
LIGHTYELLOW = FGRGBTerminalCode(r.LIGHTYELLOW_HEX, "lightyellow")
ORANGE = FGRGBTerminalCode(r.ORANGE_HEX, "orange")
PINK = FGRGBTerminalCode(r.PINK_HEX, "pink")
PURPLE = FGRGBTerminalCode(r.PURPLE_HEX, "purple")
BROWN = FGRGBTerminalCode(r.BROWN_HEX, "brown")
GOLD = FGRGBTerminalCode(r.GOLD_HEX, "gold")
LIME = FGRGBTerminalCode(r.LIME_HEX, "lime")
TEAL = FGRGBTerminalCode(r.TEAL_HEX, "teal")
NAVY = FGRGBTerminalCode(r.NAVY_HEX, "navy")
OLIVE = FGRGBTerminalCode(r.OLIVE_HEX, "olive")
MAROON = FGRGBTerminalCode(r.MAROON_HEX, "maroon")



# === Standard Background Colors ===
BG_BLACK = TC(r.BG_BLACK, "black", "bg", rgb=(b,b,b))
BG_RED   = TC(r.BG_RED  , "red", "bg", rgb=(v, b, b))
BG_GREEN = TC(r.BG_GREEN, "green", "bg", rgb=(b, v, b))
BG_YELLOW  = TC(r.BG_YELLOW, "yellow", "bg", rgb=(v, v, b))
BG_BLUE  = TC(r.BG_BLUE , "blue", "bg", rgb=(b, b, blu))
BG_MAGENTA = TC(r.BG_MAGENTA, "magenta", "bg", rgb=(v, b, v))
BG_CYAN  = TC(r.BG_CYAN , "cyan", "bg", rgb=(b, v, v))
BG_WHITE = TC(r.BG_WHITE, "white", "bg", rgb=(w,w,w))
BG_BRIGHT_BLACK = TC(r.BG_BRIGHT_BLACK, "brightblack", "bg", rgb=(h, h, h))
BG_BRIGHT_RED   = TC(r.BG_BRIGHT_RED  , "brightred", "bg", rgb=(f, b, b))
BG_BRIGHT_GREEN = TC(r.BG_BRIGHT_GREEN, "brightgreen", "bg", rgb=(b, f, b))
BG_BRIGHT_YELLOW  = TC(r.BG_BRIGHT_YELLOW, "brightyellow", "bg", rgb=(f, f, b))
BG_BRIGHT_BLUE  = TC(r.BG_BRIGHT_BLUE , "brightblue", "bg", rgb=(t, t, f))
BG_BRIGHT_MAGENTA = TC(r.BG_BRIGHT_MAGENTA, "brightmagenta", "bg", rgb=(f, b, f))
BG_BRIGHT_CYAN  = TC(r.BG_BRIGHT_CYAN , "brightcyan", "bg", rgb=(b, f, f))
BG_BRIGHT_WHITE = TC(r.BG_BRIGHT_WHITE, "brightwhite", "bg", rgb=(f, f, f))


class BGRGBTerminalCode(TerminalCode):
    def __new__(cls, rgb: BaseColor, name: str = "unknown", *groups: str):
        rgb: BaseColor = to_rgba(rgb)[:3]
        c = r.BG_RGB(*rgb)
        groups = groups or ("unknown",)
        groups = [cls.normname(n) for n in groups]
        for g in ("rgb", "bg"):
            if g not in groups:
                groups.append(g)
        return super().__new__(cls,
                               c,
                               name,
                               *groups,
                               rgb=rgb)
BG_DARKRED = BGRGBTerminalCode(r.DARKRED_HEX, "darkred")
BG_DARKGREEN = BGRGBTerminalCode(r.DARKGREEN_HEX, "darkgreen")
BG_DARKBLUE = BGRGBTerminalCode(r.DARKBLUE_HEX, "darkblue")
BG_DARKCYAN = BGRGBTerminalCode(r.DARKCYAN_HEX, "darkcyan")
BG_DARKMAGENTA = BGRGBTerminalCode(r.DARKMAGENTA_HEX, "darkmagenta")
BG_DARKYELLOW = BGRGBTerminalCode(r.DARKYELLOW_HEX, "darkyellow")
BG_LIGHTRED = BGRGBTerminalCode(r.LIGHTRED_HEX, "lightred")
BG_LIGHTGREEN = BGRGBTerminalCode(r.LIGHTGREEN_HEX, "lightgreen")
BG_LIGHTBLUE = BGRGBTerminalCode(r.LIGHTBLUE_HEX, "lightblue")
BG_LIGHTCYAN = BGRGBTerminalCode(r.LIGHTCYAN_HEX, "lightcyan")
BG_LIGHTMAGENTA = BGRGBTerminalCode(r.LIGHTMAGENTA_HEX, "lightmagenta")
BG_LIGHTYELLOW = BGRGBTerminalCode(r.LIGHTYELLOW_HEX, "lightyellow")
BG_ORANGE = BGRGBTerminalCode(r.ORANGE_HEX, "orange")
BG_PINK = BGRGBTerminalCode(r.PINK_HEX, "pink")
BG_PURPLE = BGRGBTerminalCode(r.PURPLE_HEX, "purple")
BG_BROWN = BGRGBTerminalCode(r.BROWN_HEX, "brown")
BG_GOLD = BGRGBTerminalCode(r.GOLD_HEX, "gold")
BG_LIME = BGRGBTerminalCode(r.LIME_HEX, "lime")
BG_TEAL = BGRGBTerminalCode(r.TEAL_HEX, "teal")
BG_NAVY = BGRGBTerminalCode(r.NAVY_HEX, "navy")
BG_OLIVE = BGRGBTerminalCode(r.OLIVE_HEX, "olive")
BG_MAROON = BGRGBTerminalCode(r.MAROON_HEX, "maroon")




# _____________________________________________________________________________________________________________________
INITIAL_DEFAULT_TERMINAL_COLOR = "#fff"
settings = {

}

def to_rgb(color, background=None) -> tuple[int, int, int]:
    """
    fg, bg: (r,g,b) or hex
    alpha: 0.0–1.0 (fg opacity over bg)
    """
    fr, fg, fb, fa = to_rgba(color)
    if fa == 1:
        return fr, fg, fb
    if background is None:
        background = settings.get("tc", None)
    br, bg, bb, ba = to_rgba(background)
    a = max(0.0, min(1.0, float(fa)))

    r = round((1 - a) * br + a * fr)
    g = round((1 - a) * bg + a * fg)
    b = round((1 - a) * bb + a * fb)
    return r, g, b

settings["tc"] = to_rgb(INITIAL_DEFAULT_TERMINAL_COLOR, "#fff")

def register_terminal_color(color: str, background_of_background=INITIAL_DEFAULT_TERMINAL_COLOR):
    settings["tc"] = to_rgb(color, background_of_background)



def merge_colors(color1: str | TerminalCode, color2: str | TerminalCode, group: str = "fg") -> TerminalCode:
    """
    Merge two colors by averaging their RGB values.
    
    Args:
        color1: First color (name or TerminalCode)
        color2: Second color (name or TerminalCode)
        group: Color group ("fg" or "bg")
    
    Returns:
        TerminalCode with merged RGB values, or None if colors can't be merged
    """
    # Retrieve TerminalCode instances
    tc1 = color1 if isinstance(color1, TerminalCode) else TerminalCode.retrieve(color1, group)
    tc2 = color2 if isinstance(color2, TerminalCode) else TerminalCode.retrieve(color2, group)

    # Both must be valid colors with RGB values
    if not tc1 or not tc2:
        raise Exception(f"Invalid colors: {tc1!r}, {tc2!r}")

    if not tc1.rgb or not tc2.rgb:
        raise Exception(f"Invalid rgbs: {tc1.rgb}, {tc2.rgb}")

    # Average the RGB values
    r1, g1, b1 = tc1.rgb
    r2, g2, b2 = tc2.rgb
    merged_rgb = ((r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2)
    
    # Create merged TerminalCode
    if group == "fg":
        return FGRGBTerminalCode(merged_rgb, f"{tc1.name}{tc2.name}", "fg", "merged")
    else:
        return BGRGBTerminalCode(merged_rgb, f"{tc1.name}{tc2.name}", "bg", "merged")


def get_color(
        foreground: BaseColor | TerminalCode | None = None,
        background: BaseColor | TerminalCode | None = None,
        style: list[str] | str = "",
        terminal_color: str | None = None
    ):
    s = get_style(style)
    if terminal_color is None:
        terminal_color = settings["tc"]

    tc = TerminalCode.retrieve(terminal_color, "bg") or to_rgb(terminal_color)
    bgtc = "" if background is None else (TerminalCode.retrieve(background, "bg") or BGRGBTerminalCode(to_rgb(background, tc)))
    fgtc = "" if foreground is None else (TerminalCode.retrieve(foreground, "fg") or FGRGBTerminalCode(to_rgb(foreground, background)))
    opts = [x for x in (s, bgtc, fgtc) if x]
    if len(opts) == 0:
        return TerminalCode("", "empty", "text")
    if len(opts) == 1:
        return opts[0]
    return TerminalCode("".join(opts), f"bg={background},fg={foreground},s={style}", "text")


def demo_color(
        foreground: BaseColor | TerminalCode | None = None,
        background: BaseColor | TerminalCode | None = None,
        style: list[str] | str = "",
        terminal_color: str | None = None,
        **kw
):
    if terminal_color is None:
        terminal_color = settings["tc"]
    c = get_color(foreground=foreground, background=background, style=style, terminal_color=terminal_color)
    s = f"{foreground=}, {background=}, {terminal_color=}, {style=}, {c=}"
    print(c + s + RESET, **kw)


class FGColors:
    def __getattr__(self, item):
        return get_color(item)

    def __getitem__(self, item):
        return get_color(item)

    def __dir__(self):
        return list(TerminalCode.registry.get("fg", {}))

    def __iter__(self):
        return iter(TerminalCode.registry.get("fg", {}))



class BGColors:
    def __getattr__(self, item):
        return get_color(background=item)

    def __getitem__(self, item):
        return get_color(background=item)

    def __iter__(self):
        return iter(TerminalCode.registry.get("bg", {}))

    def __dir__(self):
        return list(TerminalCode.registry.get("bg", {}))



fg = FGColors()
bg = BGColors()




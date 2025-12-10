import termite.raw as r
from termite.cases import cases
raw_colors = r

BaseColor = int | str | tuple[int, int, int] | tuple[int, int, int, float] | tuple[int, int, int, int]

def to_rgba(color: BaseColor) -> tuple[int, int, int, float] | None:
    """
    Accepts:
      - some common colors from known_colors
      - (r, g, b) tuple with values 0–255
      - (r, g, b, a) tuple with values 0–255
      - '#RRGGBB' or 'RRGGBB'
      - '#RGB' or 'RGB' shorthand
    Returns:
      (r, g, b, a) tuple
    """

    if color is None:
        return None
    if color == "":
        return (255, 255, 255, 1)
    if isinstance(color, int):
        color = hex(color)
    if hasattr(color, "rgba"):
        return color.rgba
    if hasattr(color, "rgb"):
        return *color.rgb, 1
    if isinstance(color, str):
        color = TerminalCode.normname(color)
        r = repr(color)
        if r.startswith("'\\"):
            if r.startswith(raw_colors.FG_RGB_HEADER) or r.startswith(raw_colors.BG_RGB_HEADER):
                rs, gs, bs = r[:-1].split(",")[2:]
                return int(rs), int(gs), int(bs)
            tc = TerminalCode.retrieve(color)
            if tc and tc.rgb:
                return *tc.rgb, 1
            raise Exception("invalid string")
    if not color:
        return (255, 255, 255, 1)
    if isinstance(color, str):
        color = color.lower()

    if isinstance(color, tuple) and len(color) == 3:
        r, g, b = color
        return int(r), int(g), int(b), 1.0

    if isinstance(color, tuple) and len(color) == 4:
        r, g, b, a = color
        if a > 1:
            a = a/255
        return int(r), int(g), int(b), float(a)

    if not isinstance(color, str):
        raise TypeError(f"color must be an (r,g,b) or (r,g,b,a) tuple or a hex string, not {color}")

    s = color.strip().lower()
    if s.startswith("#"):
        s = s[1:]
    if s.startswith("0x"):
        s = s[2:]

    if len(s) == 3:
        # #RGB → #RRGGBBAA
        s = "".join(ch * 2 for ch in s) + "FF"
    if len(s) == 4:
        # #RGBA → #RRGGBBAA
        s = "".join(ch * 2 for ch in s)

    if len(s) == 6:
        s += "FF"
    if len(s) != 8:
        raise ValueError(f"Invalid hex color: {color!r}")

    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    a = int(s[6: 8], 16) / 255
    return r, g, b, a



class TerminalCode(str):
    registry = {

    }
    reverse_registry: dict[str, list["TerminalCode"]] = {

    }

    @staticmethod
    def normname(s: str):
        return s.lower().replace(" ","").replace("-","").replace("_","") if isinstance(s, str) else s

    @classmethod
    def retrieve(cls, name: str, group: str | None = None):
        if name is None:
            return None
        if not isinstance(name, str):
            return None
        if isinstance(name, TerminalCode):
            return name
        if (repr(name).startswith("'\\")):
            rr = cls.reverse_registry.get(name)
            if rr:
                return rr[0]
            return cls(name)
        name = cls.normname(name)
        if group is not None:
            group = cls.normname(group)
            return cls.registry.get(group, {}).get(name)

        if name in cls.registry.get("unknown", {}):
            return cls.registry["unknown"][name]
        for g in cls.registry:
            if name in cls.registry[g]:
                return cls.registry[g][name]

    def __new__(cls, code: str, name: str = "unknown", *groups: str, rgb: BaseColor | None = None):
        obj = super().__new__(cls, code)  # create the string instance
        rgb = to_rgba(rgb)[:3] if rgb is not None else None
        name = cls.normname(name)
        obj.name = name                     # attach custom attribute
        if name not in cls.reverse_registry:
            cls.reverse_registry[name] = []
        cls.reverse_registry[name].append(obj)
        groups = groups or ("unknown",)
        groups = [cls.normname(n) for n in groups]
        obj.groups = groups
        obj.rgb = rgb
        for group in groups:
            if group not in cls.registry:
                cls.registry[group] = {}
            cls.registry[group][name] = obj
        return obj

    @property
    def aliases(self):
        return [x.name for x in self.reverse_registry[str(self)] if x.name != self.name]

    def __call__(self, text: str = ""):
        return self + text + r.RESET

    def __add__(self, other):
        o = str(other)
        oname = getattr(other, "name", o)
        return TerminalCode(str(self) + o, name=f"{self.name}+{oname}")

    def __getitem__(self, item):
        return self + item

    def __getattr__(self, item):
        return self + item

    def print(self, m="", print=print, **kw):
        print(self(m), **kw)


TC = TerminalCode
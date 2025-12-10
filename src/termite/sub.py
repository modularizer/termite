from collections.abc import Callable

import termite.raw.bg_colors as R_bg
import termite.raw.fg_colors as R_fg
import termite.raw.styles as R_s
import termite.raw.hex_colors as R_h
import termite.cursor as cursor
from termite.art import box
from termite.art.big import big_text
from termite.fancy import t
from termite.cases import case_names, cases
from termite.colors import to_rgb, TerminalCode, merge_colors
from termite.emojis import emoji_names, emojis, dashed_emoji_names
from termite.unicode import unicode_names, unicode, dashed_unicode_names
from termite.raw import FG_RGB, BG_RGB

OPENER="["
CLOSER="]"
PREFIX=""
SUFFIX=""
JOINER="+"
ESC="%"
ESC_END=""


Rk = dir(R_fg) + dir(R_bg) + dir(R_s)

color_keys = [x for x in Rk if x.upper() == x and not x.startswith('_') and not x.endswith("HEX") and not x.endswith("RGB") and not x.endswith("HEADER")]
color_values = {k.replace("_", ""): getattr(t, k)  for k in color_keys}
color_keys = list(color_values)
hex_colors = [x for x in dir(R_h) if x.endswith("HEX")]
for k in hex_colors:
    color_keys.append(k)
    hex_val = getattr(R_h, k)
    color_values[k] = FG_RGB(*to_rgb(hex_val))
    color_values["BG_" + k] = BG_RGB(*to_rgb(hex_val))


for k in list(color_keys):
    kr = k.replace("_", "")
    if kr != k:
        color_keys.append(k)
        color_values[kr] = color_values[k]
color_keys = list(sorted(color_keys, key=len, reverse=True))




cursor_actions = {
    "LEFT": cursor.left(),
    "RIGHT": cursor.right(),
    "UP": cursor.up(),
    "DOWN": cursor.down(),
    "SAVE": cursor.save(),
    "RESTORE": cursor.restore()
}
cursor_keys = list(sorted(list(cursor_actions.keys()), key=len, reverse=True))

cursor_functions = {
    "LEFT": cursor.left,
    "RIGHT": cursor.right,
    "UP": cursor.up,
    "DOWN": cursor.down,
    "WRITEAHEAD": cursor.write_ahead,
    "WA": cursor.write_ahead,
    "COMPLETION": lambda x: cursor.write_ahead(t.GRAY(x)),
    "BIG": big_text,
    "BOX": box,
    **{k: cases[k] for k in case_names}
}
cursor_function_keys = list(sorted(list(cursor_functions.keys()), key=len, reverse=True))

all_keys = list(sorted(list(color_keys + cursor_keys + cursor_function_keys), key=len, reverse=True))

class Node:
    def __init__(self, prefix="", full_text = "", root = None):
        self.children = {}
        self.prefix = prefix
        self.full_text = full_text
        self.root = root if root is not None else self

    def clone(self, **kw):
        node = type(self)(self.prefix)
        node.__dict__ = {**dict(self.__dict__), **kw}
        return node

    def get(self, word: str):
        node = self
        ft = self.full_text + word
        for ch in word:
            node = node.children.get(ch)
            if node is None:
                node = self.root.clone(full_text=self.full_text)

        return node.clone(full_text=ft)

    def set(self, word):
        node = self
        for ch in word:
            if ch in node.children:
                node = node.children[ch]
            else:
                nn = type(self)(node.prefix + ch, root=self.root)
                node.children[ch] = nn
                node = nn
        return node

    def __getattr__(self, item):
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

class Token(Node):
    def __init__(self, prefix="", full_text = "", root = None):
        super().__init__(prefix=prefix, full_text=full_text, root=root)
        self.value = None
        self.func = None
        self.called = None
        self.end_token = None
        self.opened = None
        self.content = ""
        self.end = None


    def open(self, end=R_fg.RESET, opener=OPENER):
        node = self.set(opener)
        node.opened = True
        node.called = True
        node.value = self.value
        node.end = end if isinstance(end, str) else None
        node.func = end if not isinstance(end, str) else None
        return node


    def close(self, end_token):
        self.opened = False
        self.end_token = end_token
        return self

    def __repr__(self):
        return f"Token<{self.prefix}(>" if self.func is not None else f"Token<{self.value!r}>" if self.value is not None else f"Token<{self.full_text}>"



class EndToken:
    def __init__(self, token):
        self.token = token.close(self)
        self.opened = False
        self.prefix = ")"
        self.value = token.end

    def __repr__(self):
        return f"EndToken<{self.value!r}>" if self.value is not None else f"EndToken<)>"

def sub(*text: str, color_prefix=PREFIX, color_suffix=SUFFIX, opener=OPENER, closer=CLOSER, joiner=JOINER, esc=ESC, esc_end=ESC_END, raw=False):
    text = "".join(text)
    root = Token()
    for k in color_keys:
        node = root.set(color_prefix + k + color_suffix)
        node.value = color_values[k]
        node.open(opener=opener)

    for k in cursor_actions:
        node = root.set(color_prefix + k + color_suffix)
        node.value = cursor_actions[k]

    for k in cursor_function_keys:
        node = root.set(color_prefix + k + color_suffix)
        node.open(cursor_functions[k])

    for k in emoji_names:
        root.set(":" + k + ":").value = emojis[k]
    for k in dashed_emoji_names:
        root.set(":" + k + ":").value = emojis[k]
    for k in unicode_names:
        root.set(":" + k + ":").value = unicode[k]
    for k in dashed_unicode_names:
        root.set(":" + k + ":").value = unicode[k]
    root.set(color_prefix + "rgb" + color_suffix).open(opener=opener).value = "rgb" + opener
    root.set(color_prefix + "bgrgb" + color_suffix).open(opener=opener).value = "bgrgb" + opener
    root.set(color_prefix + "rgba" + color_suffix).open(opener=opener).value = "rgba" + opener
    root.set(color_prefix + "bgrgba" + color_suffix).open(opener=opener).value = "bgrgba" + opener

    tokens = [root.clone()] # list of Token or str
    escaped = False
    for ch in (text + "x"):
        last_node = tokens[-1]
        if ch == esc_end and escaped:
            escaped = False
            continue
        elif ch == esc and not escaped:
            escaped = True
            continue
        elif not escaped and ch == joiner and last_node.value:
            continue
        elif not escaped and ch == closer:
            if len(last_node.full_text) > len(last_node.prefix):
                pre_prefix = last_node.full_text[:-len(last_node.prefix)] if len(last_node.full_text) > len(last_node.prefix) else ""
                tokens = tokens[:-1] + ([root.clone()[pre_prefix] ] if pre_prefix else []) + [last_node]
            for tk in reversed(tokens):
                if tk.opened:
                    px = tk.value
                    if px in ["rgba" + opener, "rgb" + opener, "bgrgb" + opener, "bgrgba" + opener]:
                        s = tokens[-1].full_text
                        n = s.count(",")
                        T = BG_RGB if px.startswith("bg") else FG_RGB
                        if n == 0: # rgba(#hex)
                            tk.value = T(*to_rgb(s))
                        elif n == 1: # rgba(#hex, #bg)
                            a, b = s.split(",")
                            tk.value  = T(*to_rgb(a, b))
                        elif n == 2: # rgba(r,g,b)
                            r,g,b = s.split(",")
                            tk.value  = T(int(r), int(g), int(b))
                        elif n == 3: # rgba(r,g,b,a)
                            r,g,b, a = s.split(",")
                            tk.value  = T(int(r), int(g), int(b), float(a) if float(a) <= 1 else float(a)/255)
                        elif n == 4: # rgba(r,g,b,a, #bg)
                            r,g,b, a, bg = s.split(",")
                            tk.value  = T(*to_rgb((int(r), int(g), int(b), float(a) if float(a) <= 1 else float(a)/255), bg))
                        elif n == 6: # rgba(r,g,b,a, bgr, bgg, bgb)
                            r,g,b, a, br, bb, bb = s.split(",")
                            tk.value  = T(*to_rgb((int(r), int(g), int(b), float(a) if float(a) <= 1 else float(a)/255), (int(br), int(bg), int(bb))))
                        elif n == 7: # rgba(r,g,b,a, bgr, bgg, bgb, bga)
                            r,g,b, a, br, bb, bb, ba = s.split(",")
                            tk.value  = T(*to_rgb((int(r), int(g), int(b), float(a) if float(a) <= 1 else float(a)/255), (int(br), int(bg), int(bb), float(ba) if float(ba) <= 1 else float(ba)/255)))
                        else:
                            raise ValueError("invalid value")
                        tk.prefix = ""
                        tk.full_text = ""
                        tk.open()
                        tokens.pop()
                    else:
                        tokens.append(EndToken(tk))
                        tokens.append(root.clone())
                    break
            else:
                tokens[-1] = last_node[closer]

        else:
            opening = ch == opener and last_node.children.get(opener) and not escaped
            node = last_node[ch]
            if not node.prefix and (last_node.value or last_node.func):
                pre_prefix = last_node.full_text[:-len(last_node.prefix)] if len(last_node.full_text) > len(last_node.prefix) else ""
                tokens = tokens[:-1] + ([root.clone()[pre_prefix] ] if pre_prefix else []) + [last_node, root.clone()[ch if not opening else ""]]
                continue
            # pre_prefix = last_node.full_text[:-len(last_node.prefix)] if len(last_node.full_text) > len(last_node.prefix) else ""
            # tokens = tokens[:-1] + ([root.clone()[pre_prefix] ] if pre_prefix else []) + [node]
            tokens[-1] = node
            if not opening:
                node.opened = False
            else:
                pre_prefix = last_node.full_text[:-len(last_node.prefix)] if len(last_node.full_text) > len(last_node.prefix) else ""
                tokens = tokens[:-1] + ([root.clone()[pre_prefix] ] if pre_prefix else []) + [node]
                node.full_text = ""
                node.prefix = ""

        if escaped and not esc_end:
            escaped = False

    content: list[str | TerminalCode | tuple[list, Callable]] = []
    all_levels = [content]
    current_list = content
    for t in tokens:
        if isinstance(t, EndToken):
            if t.value is not None:
                current_list.append(t.value)
            else:
                all_levels.pop()
                current_list = all_levels[-1]
        elif t.value and t.func is None:
            current_list.append(t.value)
        elif t.func:
            x = []
            current_list.append((x, t.func))
            t.content = x
            current_list = x
            all_levels.append(x)
        else:
            current_list.append(t.full_text)

    def resolve(content, func=None):
        s = ""
        colors = []
        bg_colors = []
        for c in [*content, ""]:
            if isinstance(c, tuple):
                cc, cf = c
                if colors:
                    if len(colors) > 1:
                        co = merge_colors(colors[0], colors[1], "fg")
                        for nc in colors[2:]:
                            co = merge_colors(co, nc, "fg")
                        s += co
                    else:
                        s += colors[0]
                    colors = []
                if bg_colors:
                    if len(bg_colors) > 1:
                        co = merge_colors(bg_colors[0], bg_colors[1], "bg")
                        for nc in colors[2:]:
                            co = merge_colors(co, nc, "bg")
                        s += co
                    else:
                        s += bg_colors[0]
                    bg_colors = []
                s += resolve(cc, cf)
            elif isinstance(c, TerminalCode) and c != R_fg.RESET:
                if "fg" in c.groups:
                    colors.append(c)
                elif "bg" in c.groups:
                    bg_colors.append(c)
                else:
                    s += c
            elif isinstance(c, str):
                if colors:
                    if len(colors) > 1:
                        co = merge_colors(colors[0], colors[1], "fg")
                        for nc in colors[2:]:
                            co = merge_colors(co, nc, "fg")
                        s += co
                    else:
                        s += colors[0]
                    colors = []
                if bg_colors:
                    if len(bg_colors) > 1:
                        co = merge_colors(bg_colors[0], bg_colors[1], "bg")
                        for nc in colors[2:]:
                            co = merge_colors(co, nc, "bg")
                        s += co
                    else:
                        s += bg_colors[0]
                    bg_colors = []
                s += c
            else:
                raise Exception(f"{c}, {type(c)}")
        s = func(s) if func is not None else s
        before = ""
        while before != s:
            before = s
            s = s.replace(R_fg.RESET + R_fg.RESET, R_fg.RESET)
        return s

    items = all_levels[0]
    s = resolve(items, lambda s:s)[:-1]
    if raw:
        return repr(s)
    return s



def demo(text: str, color_prefix=PREFIX, color_suffix=SUFFIX, opener=OPENER, closer=CLOSER, joiner=JOINER, esc=ESC, esc_end=ESC_END):
    r = sub(text, color_prefix=color_prefix, color_suffix=color_suffix, opener=opener, closer=closer, joiner=joiner, esc=esc, esc_end=esc_end)
    print(f"Input:  {text!r}")
    print(f"Output: {r!r}")
    print(r)
    print()

def _resolve_file(file):
    """Resolve special file values to actual file objects."""
    import sys
    if file == "stderr":
        return sys.stderr
    elif file == "stdout":
        return sys.stdout
    elif file == "/dev/tty":
        return open("/dev/tty", "w")
    elif isinstance(file, str):
        # Regular file path
        return open(file, "w")
    # Already a file object
    return file

def subprint(*text: str, color_prefix=PREFIX, color_suffix=SUFFIX, opener=OPENER, closer=CLOSER, joiner=JOINER, esc=ESC, esc_end=ESC_END, raw=False, print=print, **kwargs):
    s = sub(*text, color_prefix=color_prefix, color_suffix=color_suffix, opener=opener, closer=closer, joiner=joiner, esc=esc, esc_end=esc_end, raw=raw)
    # Handle special file values
    if "file" in kwargs:
        kwargs["file"] = _resolve_file(kwargs["file"])

    print(s, **kwargs)



def full_demo():
    demo("Hello TMGREENworldTMRESET!", color_prefix="TM")
    demo("GREEN[hello world]", color_prefix="")
    demo("BOLDGREEN[bold green text]", color_prefix="")
    demo("REDBOLD[red and bold] BLUEITALIC[blue and italic]", color_prefix="")
    demo("BOLDGREEN[REDBOLD[nested merged]]", color_prefix="")
    demo("RED[BOLD[UNDERLINE[triple nested]]]")
    demo("GREEN[ok]abcITALIC[taco]REDfiretruckRESET")
    demo("rgb[#FF5733][custom orange color]")
    demo("rgb[#258][shorthand hex]")
    demo("rgb[255,100,50][RGB tuple color]")
    demo("bgrgb[#0000FF][blue background]")
    demo("GREEN[BOLD[rgb[#FF0000][red text inside]]]")
    demo("RED[red] GREEN[green] BLUE[blue]")
    demo("bgrgb[#00FF00][background green]")
    demo("BLUE+RED[merged blue and red]")
    demo("GREEN+YELLOW[green+yellow] RED+BLUE[red+blue]")
    demo("BOLD+ITALIC+RED+BLUE[bold italic merged red+blue]")
    demo("BOLD+UNDERLINE+GREEN+YELLOW[bold underline green+yellow]")
    demo("BOLD[bold] ITALIC[italic] UNDERLINE[underline] STRIKETHROUGH[strikethrough]")
    demo("[BOLD]<bold> [ITALIC]<italic> [UNDERLINE]<underline> [STRIKETHROUGH]<strikethrough>",
         color_prefix="[", color_suffix="]", opener="<", closer=">")
    demo("BOLD<bold> ITALIC<italic> UNDERLINE<underline> STRIKETHROUGH<strikethrough>",
         opener="<", closer=">")
    demo("CAMELCASE[sample of camel case] TITLECASE[titles are cool]")
    demo("BOLD[CAMELCASE[sample of camel case]] TITLECASE[titles are cool]")
    demo("BOLD[art] abc GREEN[titles are cool]")
    demo("emojis are cool :fire")
    demo("unicode is cool :arrow-double-down")
    demo("BOX[BIG[hello, world]")

if __name__ == "__main__":
    full_demo()


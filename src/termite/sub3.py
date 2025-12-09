"""
Clean, simple implementation of the sub function following 7 clear steps.
"""
import re

import termite.raw as R
import termite.cursor as cursor
from termite.colors import to_rgb
from termite.raw import FG_RGB, BG_RGB



color_keys = [x for x in dir(R) if x.upper() == x and not x.startswith('_') and not x.endswith("HEX") and not x.endswith("RGB")]
color_values = {k: getattr(R, k) for k in color_keys}
hex_colors = [x for x in dir(R) if x.endswith("HEX")]
for k in hex_colors:
    color_keys.append(k)
    hex_val = getattr(R, k)
    color_values[k] = FG_RGB(*to_rgb(hex_colors))
    color_values["BG_" + k] = BG_RGB(*to_rgb(hex_colors))


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
    "SAVE": cursor.save,
    "RESTORE": cursor.restore,
    "WRITEAHEAD": cursor.write_ahead,
    "WA": cursor.write_ahead
}
cursor_function_keys = list(sorted(list(cursor_functions.keys()), key=len, reverse=True))

all_keys = list(sorted(list(color_keys + cursor_keys + cursor_function_keys), key=len, reverse=True))

def find_escape(text: str, opts):
    i = 0
    while True:
        i += 1
        for o in opts:
            if o*i not in text:
                return "|" + o*i + "|"

def sub(text: str, name="", esc="%", esc2=None):
    """
    Clean, simple substitution following 7 clear steps.
    """
    e2 = find_escape(text, "-")
    esc_pattern = re.compile(f"{re.escape(esc)}(.*?){re.escape(esc2 or esc)}")



    # Step 1: find an escape pattern not found in the current string
    e = find_escape(text, "$%!#^@*")


    # step 2, from logest to shortest, replace KEY with {e}KEY{e}
    for k in all_keys:
        text = text.replace(k, f"{e}{k}{e}")

    text = re.sub(esc_pattern, lambda g: g.replace(e, ""), text)


    # step 3: merge adjacent
    p = find_escape(text, "+")
    text = text.replace(e + e, p)

    # step 4, identify parts
    parts = text.split(e + e)
    x = []
    open_parts = []
    for i, part in enumerate(parts):
        items = part.split(p)
        if all(k in all_keys for k in items):
            x.append({"type": "special", "called": False, "open": False, "items": items, "i": len(x), "parents": [xpart["i"] for xpart in open_parts], "children": []})
        else:
            s = part
            if part.startswith("("):
                if i > 0:
                    open_parts.append(x[-1])
                    s = s[1:]
            s2 = ""
            for i, ch in enumerate(s):
                if ch == ")":
                    if open_parts:
                        x.append({"type": "content", "value": s2, "parents": [xpart["i"] for xpart in open_parts], "children": []})
                        o = open_parts.pop()
                        o["open"] = False
                        x.append({"type": "close", "i": o["i"], "parents": [xpart["i"] for xpart in open_parts], "children": []})
                        s2 = ""
                    else:
                        s2 += ch
                else:
                    s2 += ch
            if s2:
                x.append({"type": "content", "value": s2, "parents": [xpart["i"] for xpart in open_parts], "children": []})
    for i, part in x:
        for j in x["parents"]:
            x[j]["children"].append(i)

    # resolve uncalled
    for part in x:
        if part["type"] == "special" and not part["called"]:
            part["type"] = "content"
            part["value"] = "".join(color_values.get(k, cursor_actions.get(k, "")) for k in part["items"])

    parts = x

    def merge_consecutive_content():
        # TODO
        pass

    def resolve_calls_without_children():
        # TODO
        pass

    # TODO: continue merging and resolving until only a single part, of content








def demo(text: str, name=""):
    r = sub(text, name=name)
    print(f"Input:  {text!r}")
    print(f"Output: {r!r}")
    print(f"Result: {r}")
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

def subprint(*text: str, name="", raw=False, print=print, **kwargs):
    parts = [sub(t, name=name) for t in text]
    # Handle special file values
    if "file" in kwargs:
        kwargs["file"] = _resolve_file(kwargs["file"])

    if raw:
        # Print raw escape codes (repr format)
        raw_parts = [repr(part) for part in parts]
        print(*raw_parts, **kwargs)
    else:
        print(*parts, **kwargs)

if __name__ == "__main__":
    print("=== Sample 1: Simple substitution (no parentheses) ===")
    demo("Hello TMGREENworldTMRESET!", name="TM")


    print("=== Sample 2: Function call with parentheses ===")
    demo("GREEN(hello world)", name="")

    print("=== Sample 3: Merged keys (BOLDGREEN) ===")
    demo("BOLDGREEN(bold green text)", name="")

    print("=== Sample 3b: More merged keys ===")
    demo("REDBOLD(red and bold) BLUEITALIC(blue and italic)", name="")

    print("=== Sample 3c: Nested merged keys ===")
    demo("BOLDGREEN(REDBOLD(nested merged))", name="")

    print("=== Sample 4: Multiple nested levels ===")
    demo("TMRED(TMBOLD(TMUNDERLINE(triple nested)))")

    print("=== Sample 5: Mixed simple and function calls ===")
    demo("TMGREEN(ok)abcTMITALIC(taco)TMREDfiretruckTMRESET")

    print("=== Sample 6: RGB with hex color ===")
    demo("TMFGRGB(#FF5733)(custom orange color)")

    print("=== Sample 7: RGB with shorthand hex ===")
    demo("TMFGRGB(#258)(shorthand hex)")

    print("=== Sample 8: RGB with tuple ===")
    demo("TMFGRGB(255,100,50)(RGB tuple color)")

    print("=== Sample 9: Background RGB ===")
    demo("TMBGRGB(#0000FF)(blue background)")

    print("=== Sample 10: Complex nested with RGB ===")
    demo("TMGREEN(TMBOLD(TMFGRGB(#FF0000)(red text inside)))")

    print("=== Sample 11: Multiple colors in sequence ===")
    demo("TMRED(red) TMGREEN(green) TMBLUE(blue)")

    print("=== Sample 12: Keys without underscores ===")
    demo("TMBGRGB(#00FF00)(background green)")

    print("=== Sample 13: Merged colors (BLUERED) ===")
    demo("BLUERED(merged blue and red)", name="")

    print("=== Sample 14: More color merges ===")
    demo("GREENYELLOW(green+yellow) REDBLUE(red+blue)", name="")

    print("=== Sample 15: Stacked keys (BOLDITALICREDBLUE) ===")
    demo("BOLDITALICREDBLUE(bold italic merged red+blue)", name="")

    print("=== Sample 16: Multiple stacked styles and colors ===")
    demo("BOLDUNDERLINEGREENYELLOW(bold underline green+yellow)", name="")

    print("=== Sample 17: Shortened aliases (B, I, U) ===")
    demo("BOLD(bold) ITALIC(italic) UNDERLINE(underline) STRIKETHROUGH(strikethrough)", name="")


import sys

from termite.chars import BACKSPACE
import termite.cursor  as cursor
from termite.sub import sub as substitute
from termite.fancy import t

complete = lambda x: t.write_ahead(t.GRAY(x))


global_state = {}
def cprint(*pre: str,
          completion: str="",
          overwrite: bool = True,
          overwrite_line_count: int | None = None,
          file=sys.stdout,
           end="", # kwargs to pass to print
          print=print, # by default, use the print builtin, but allow overriding
          state: dict | None = global_state, # this is INTENTIONALLY mutable
          sub: bool = False,
           **kw,
          ):
    print = print or (lambda *a, **kw: None)
    post = completion
    post = post or ""
    pre = "".join(pre)
    state = state if state is not None else {}
    # first, clear the old content if we are overwriting
    if overwrite and (overwrite_line_count is None or overwrite_line_count > 0):
        # if overwrite_line_count is specified we will clear that many lines
        if overwrite_line_count is None:
            # if not specified, we will detect based on cached content
            overwrite_line_count = state.get("old", "").count("\n") + 1

        # now, clear the old rows
        for _ in range(overwrite_line_count - 1):
            print(cursor.clear_line() + cursor.up(), end="", flush=True, file=file)
        print(cursor.clear_line(), end="", flush=True, file=file)


    # Check if completion starts with backspaces (full replacement)
    backspace_count = 0
    if post.startswith(BACKSPACE):
        # Count leading backspaces
        while backspace_count < len(post) and post[backspace_count] == BACKSPACE:
            backspace_count += 1
    post = post[backspace_count:]
    backspace_count = min(len(pre), backspace_count)
    prefix_stays = pre[:-backspace_count] if backspace_count > 0 else pre
    prefix_replaced = pre[-backspace_count:] if backspace_count > 0 else ""
    replaced_highlight = t.bg.white(prefix_replaced) if prefix_replaced else ""
    completion = complete(post) if post else ""

    before_cursor = f"{prefix_stays}{replaced_highlight}"
    if before_cursor:
        if sub:
            before_cursor = substitute(before_cursor, **kw)
        print(before_cursor, end="", flush=True, file=file)
    if completion:
        if sub:
            completion = substitute(completion, **kw)
        print(completion, end="", flush=True, file=file)
    txt = before_cursor + completion
    state["old"] = txt
    return txt

if __name__ == "__main__":
    import time
    d = lambda: time.sleep(1)
    p = lambda x: print(x, end="", flush=True)

    # p("abc")
    # d()
    # p("\r")
    # d()
    # p(CLEAR_REST_OF_LINE)
    # d()
    # p("def")
    # d()
    # p("ghi")
    # d()
    # cprint("abc")
    # d()
    # cprint("abcd", "efg")
    # d()
    # cprint("abcdefg")
    # d()
    cprint("a\nb\nc\nd")
    d()
    cprint("e")
    d()
    cprint("f\n")
    d()
    cprint("test", completion="compl")
    d()
    cprint("testcompl", completion="etion")
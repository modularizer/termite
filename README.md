# Termite: Terminal Utilities

Terminal manipulation utilities for Python: colors, styles, emojis, cursor-control and string-based formatting.


## Features
* text-colors
  * basic named colors
  * arbitrary hex, rgb, or rgba(which gets blended back to rgb)
  * sum to merge colors, e.g. BLUE + RED
* highlight-colors
    * basic named colors
    * arbitrary hex, rgb, or rgba(which gets blended back to rgb)
    * sum to merge colors, e.g. BLUE + RED
* styles
  * **bold**
  * _italic_
  * underline
  * strikethrough
* cursor actions
  * write_ahead/save/restore
  * clear/erase
  * up/down/left/right
  * pos/row/col
* emojis
  * `:fire` => 🔥
* special fonts and ASCII art
    * Big Text
    * Boxed Text

## How to use
1. in Python
2. in the command-line

## Install
```bash
pip install modularizer-termite
```

## Quick Start

```python
from termite import subprint, full_demo

subprint("GREEN[BOX[BIG[hello, world]]]\nBGYELLOW[Termite can do a lot :fire:]")
full_demo()
```

## Tools

- `from termite import t`: access pretty much any const or builder
  - `print(t.GRAY + "some text" + t.RST)` or `print(t.GRAY("some text")`)
- `from termite import sub`: do string substitutions to get the fancy string
- `from termite import subprint`: do string substitutions then print the fancy string
- `from termite import cprint`: each statement overwrites the last, print with black text and gray completions, built for an autocomplete solution
- `termite.raw`: JUST the strings, none of our fancy classes or getters
- `termite.chars.CTRL`: object which gets the key equivalents of Ctrl combos, e.g. `CTRL + 'c'`, `CTRL["c"]`, `CTRL.C`


## String Substitution with `sub()`

The `sub()` function provides a declarative string-based API for terminal formatting.

### Basic Usage

```python
from termite import sub, subprint

a = sub("RED[text] GREEN[text] BLUE[text]")
b = sub("BOLD[bold] ITALIC[italic] UNDERLINE[underline]")
subprint("BOLDRED[Error message]")
```

### Stacked Keys

Stack multiple keys together. Keys are matched longest-first (e.g., `RED` before `R`):

```python
from termite import sub, subprint

x = sub("BOLDITALICREDBLU[bold italic merged red+blue]")
subprint("BOLDUNDERLINEGREENYELLOW[bold underline green+yellow]")
```

### Merged Colors

Multiple colors are automatically merged by averaging RGB values:

```python
from termite import subprint

subprint("BLUERED[merged blue+red]")
subprint("GREENYELLOW[green+yellow]")
subprint("REDBLUEGREEN[three colors merged]")
```

### Short Aliases

- `B` = BOLD, `I` = ITALIC, `U` = UNDERLINE, `D` = DIM, `S` = STRIKETHROUGH, `R` = REVERSE, `H` = HIDDEN

```python
from termite import subprint

subprint("B(bold) I(italic) U(underline)")
subprint("BOLD+ITALIC+UNDERLINE[bold italic underline]")
```

### Cursor Control

```python
from termite import subprint

subprint("LEFT RIGHT UP DOWN")              # Default: 1
subprint("LEFT[3] RIGHT[5] UP[2] DOWN[4]")  # With args
subprint("POS[10,20] ROW[5] COL[10]")       # Positioning
subprint("CLEAR ERASE BACK")                # Line control
subprint("WA[GRAY[completion]]")            # Write ahead
```

### RGB Colors

```python
from termite import subprint

subprint("rgb[#FF5733][custom orange]")
subprint("rgb[#258][shorthand]")
subprint("rgb[255,100,50][RGB tuple]")
subprint("bgrgb[#0000FF][background]")
```

### Nested Patterns

```python
from termite import subprint

subprint("GREEN[BOLD[bold green]]")
subprint("RED[BOLD[UNDERLINE[nested]]]")
subprint("GREEN[BOLD[FGRGB[#FF0000][red inside]]]")
```

### Examples

```python
from termite import subprint

# Status messages
subprint("GREEN[✓ Success] RED[✗ Error]")

# Progress
for i in range(10):
    subprint(f"BOLD[Progress: ]GREEN[{i+1}/10]", end="")
    subprint("CLEAR")

# Interactive completion
pre="prefix"
completion="test"
subprint(f"{pre}WA[GRAY[{completion}]]")
```

## Colors API

```python
from termite import colors

# Foreground colors
colors.red("text")
colors.green("text")
colors.bright_red("text")

# Background colors
colors.bg.blue("text")

# Styles
colors.bold("text")
colors.italic("text")

# RGB colors
colors("#FF5733")("text")
colors((255, 87, 51))("text")

# Combining
colors.bold + colors.red("text")
colors(foreground="red", background="blue", style="bold")
```

## Cursor Control

```python
from termite import cursor

cursor.up(n=1)        # Move up n lines
cursor.down(n=1)      # Move down n lines
cursor.left(n=1)     # Move left n chars
cursor.right(n=1)     # Move right n chars
cursor.pos(row, col)  # Move to position
cursor.col(n=0)       # Move to column
cursor.row(n)         # Move to row
cursor.clear_line()   # Clear to end of line
cursor.erase_line()   # Erase entire line
cursor.write_ahead(text)  # Write without moving cursor
cursor.backspace()    # Backspace
```

## Print with Suggestions

```python
import time
from termite import cprint

cprint("User typed: ", completion="completion")
time.sleep(1)
cprint("User typed: abc", completion="def")  # Updates previous
```

## Module Structure

- `colors.py` - Color and styling API
- `cursor.py` - Cursor movement and positioning
- `sub.py` - String substitution for formatting
- `terminal.py` - High-level printing utilities
- `raw` - Low-level ANSI codes
- `chars.py` - Control character mappings
- `clie.py` - Command Line Interface which calls sub


# Termite: Terminal Utilities

Terminal manipulation utilities for Python: ANSI colors, cursor control, text styling, and string-based formatting.

## Instal
```bash
pip install modularizer-termite
```

## Quick Start

```python
from termite import colors, cursor, sub, subprint

# Colors API
print(colors.red("Error"))
print(colors.bg.blue("Background"))

# Cursor control
print(cursor.up(3))
print(cursor.clear_line())

# String substitution (recommended)
subprint("RED(Error) GREEN(Success) BOLD(Important)")
```

## String Substitution with `sub()`

The `sub()` function provides a declarative string-based API for terminal formatting.

### Basic Usage

```python
from termite import sub, subprint

sub("RED(text) GREEN(text) BLUE(text)")
sub("BOLD(bold) ITALIC(italic) UNDERLINE(underline)")
subprint("BOLDRED(Error message)")
```

### Stacked Keys

Stack multiple keys together. Keys are matched longest-first (e.g., `RED` before `R`):

```python
sub("BOLDITALICREDBLUE(bold italic merged red+blue)")
sub("BOLDUNDERLINEGREENYELLOW(bold underline green+yellow)")
```

### Merged Colors

Multiple colors are automatically merged by averaging RGB values:

```python
sub("BLUERED(merged blue+red)")
sub("GREENYELLOW(green+yellow)")
sub("REDBLUEGREEN(three colors merged)")
```

### Short Aliases

- `B` = BOLD, `I` = ITALIC, `U` = UNDERLINE, `D` = DIM, `S` = STRIKETHROUGH, `R` = REVERSE, `H` = HIDDEN

```python
sub("B(bold) I(italic) U(underline)")
sub("BIU(bold italic underline)")
sub("BRED(bold red)")
```

### Cursor Control

```python
sub("LEFT RIGHT UP DOWN")              # Default: 1
sub("LEFT(3) RIGHT(5) UP(2) DOWN(4)")  # With args
sub("POS(10,20) ROW(5) COL(10)")       # Positioning
sub("CLEAR ERASE BACK")                # Line control
sub("WA(GRAY(completion))")            # Write ahead
```

### RGB Colors

```python
sub("FGRGB(#FF5733)(custom orange)")
sub("FGRGB(#258)(shorthand)")
sub("FGRGB(255,100,50)(RGB tuple)")
sub("BGRGB(#0000FF)(background)")
```

### Nested Patterns

```python
sub("GREEN(BOLD(bold green))")
sub("RED(BOLD(UNDERLINE(nested)))")
sub("GREEN(BOLD(FGRGB(#FF0000)(red inside)))")
```

### Examples

```python
# Status messages
subprint("GREEN(✓ Success) RED(✗ Error)")

# Progress
for i in range(10):
    subprint(f"BOLD(Progress: )GREEN({i+1}/10)", end="")
    sub("CLEAR")

# Interactive completion
subprint(f"{input}WA(GRAY({completion}))")
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
from termite import print_with_suggestion

print_with_suggestion("User typed: ", "completion")
print_with_suggestion("User typed: abc", "def")  # Updates previous
```

## Module Structure

- `colors.py` - Color and styling API
- `cursor.py` - Cursor movement and positioning
- `sub.py` - String substitution for formatting
- `terminal.py` - High-level printing utilities
- `raw.py` - Low-level ANSI codes
- `chars.py` - Control character mappings

## Notes

- All color codes auto-reset with the high-level API
- Uses ANSI escape codes (works on most modern terminals)
- RGB colors require 24-bit color (truecolor) support
- Keys in `sub()` are matched longest-first for correct parsing

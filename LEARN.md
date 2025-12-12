# Learning ANSI Escape Codes

This document explains how ANSI escape codes work at a fundamental level. These are the low-level control sequences that terminals use for colors, cursor movement, and text formatting.

## What Are ANSI Escape Codes?

ANSI escape codes (also called ANSI escape sequences) are special character sequences that control terminal behavior. They were standardized by the American National Standards Institute (ANSI) and are supported by most modern terminals.

These codes are **in-band signaling** - they're embedded directly in the text stream, which means they're invisible when printed but cause the terminal to perform actions like changing colors or moving the cursor.

## Basic Structure

ANSI escape codes typically start with:
- `\033[` (octal)
- `\x1b[` (hexadecimal)
- `\e[` (some languages support this shorthand)

This is called the **CSI** (Control Sequence Introducer). Everything after the `[` is the actual command.

## Color Codes

### Standard Colors (3-bit/8 colors)

**Foreground colors:**
- `30` = Black
- `31` = Red
- `32` = Green
- `33` = Yellow
- `34` = Blue
- `35` = Magenta
- `36` = Cyan
- `37` = White

**Background colors:**
- `40` = Black
- `41` = Red
- `42` = Green
- `43` = Yellow
- `44` = Blue
- `45` = Magenta
- `46` = Cyan
- `47` = White

**Example:**
```bash
echo -e "\033[31mRed text\033[0m"
```

### Bright Colors (4-bit/16 colors)

Add `60` to foreground codes or `10` to background codes:
- `90-97` = Bright foreground colors
- `100-107` = Bright background colors

**Example:**
```bash
echo -e "\033[91mBright red\033[0m"
```

### 256-Color Mode

Use `38;5;n` for foreground or `48;5;n` for background, where `n` is 0-255:
- `0-15` = Standard colors
- `16-231` = 6×6×6 color cube
- `232-255` = Grayscale

**Example:**
```bash
echo -e "\033[38;5;196m256-color red\033[0m"
```

### True Color (24-bit RGB)

Use `38;2;r;g;b` for foreground or `48;2;r;g;b` for background:
- `r`, `g`, `b` are RGB values (0-255)

**Example:**
```bash
echo -e "\033[38;2;255;100;50mCustom orange\033[0m"
```

## Text Styles

- `0` = Reset all
- `1` = Bold/Bright
- `2` = Dim/Faint
- `3` = Italic
- `4` = Underline
- `5` = Slow blink
- `6` = Rapid blink
- `7` = Reverse/Invert
- `8` = Hidden/Conceal
- `9` = Strikethrough

**Example:**
```bash
echo -e "\033[1;4mBold and underlined\033[0m"
```

Multiple codes can be combined with semicolons: `\033[1;31;44m` = bold red text on blue background.

## Cursor Control

### Movement

- `A` = Move cursor up N lines (default: 1)
- `B` = Move cursor down N lines (default: 1)
- `C` = Move cursor right N columns (default: 1)
- `D` = Move cursor left N columns (default: 1)
- `E` = Move cursor to beginning of line N lines down
- `F` = Move cursor to beginning of line N lines up

**Example:**
```bash
echo -e "Line 1\033[2A\033[5CMoved up 2 lines, right 5 columns"
```

### Positioning

- `H` or `f` = Move cursor to row, column (default: 1,1)
  - Format: `\033[row;colH` or `\033[row;colf`

**Example:**
```bash
echo -e "\033[10;20HText at row 10, column 20"
```

### Line Control

- `K` = Erase in line
  - `0` = Erase from cursor to end of line
  - `1` = Erase from cursor to beginning of line
  - `2` = Erase entire line
- `J` = Erase in display
  - `0` = Erase from cursor to end of screen
  - `1` = Erase from cursor to beginning of screen
  - `2` = Erase entire screen
  - `3` = Erase entire screen and scrollback buffer

**Example:**
```bash
echo -e "Some text\033[2K"  # Erase the line
```

### Cursor Visibility

- `?25h` = Show cursor
- `?25l` = Hide cursor

**Example:**
```bash
echo -e "\033[?25l"  # Hide cursor
# ... do something ...
echo -e "\033[?25h"  # Show cursor
```

### Save/Restore Cursor Position

- `s` = Save cursor position
- `u` = Restore cursor position

**Example:**
```bash
echo -e "\033[s"  # Save position
echo "Text"
echo -e "\033[u"  # Restore to saved position
```

## Special Sequences

### Device Control

- `6n` = Query cursor position (Device Status Report)
  - Terminal responds with `\033[row;colR`

### Alternative Screen Buffer

- `?1049h` = Switch to alternate screen buffer
- `?1049l` = Switch back to normal screen buffer

Useful for full-screen applications that want to restore the terminal state when exiting.

## Reset Code

Always end color/style sequences with `\033[0m` (or `\033[m`) to reset all attributes. This prevents "color bleeding" where subsequent text inherits the formatting.

## Testing in Your Terminal

You can test these codes directly:

```bash
# Colors
echo -e "\033[31mRed\033[32mGreen\033[34mBlue\033[0m"

# Cursor movement
echo -e "Start\033[5C\033[1AEnd"

# Combined
echo -e "\033[1;31;44mBold red on blue\033[0m"
```

## Terminal Compatibility

Not all terminals support all features:
- **Basic colors (3-bit)**: Supported everywhere
- **Bright colors (4-bit)**: Most terminals
- **256 colors**: Most modern terminals
- **True color (24-bit)**: Most modern terminals (check with `$TERM`)
- **Italic**: Not all terminals
- **Strikethrough**: Limited support

Check your terminal's capabilities:
```bash
echo $TERM
```

## Resources

### Official Standards
- **ECMA-48**: The official standard for ANSI escape codes
  - [ECMA-48 PDF](https://www.ecma-international.org/publications-and-standards/standards/ecma-48/)
- **ISO/IEC 6429**: International standard (supersedes ANSI X3.64)
  - [ISO/IEC 6429](https://www.iso.org/standard/12782.html)

### Documentation & Guides
- **ANSI Escape Codes (Wikipedia)**: Comprehensive overview
  - [Wikipedia: ANSI Escape Code](https://en.wikipedia.org/wiki/ANSI_escape_code)
- **Bash Prompt HOWTO**: Practical guide with examples
  - [Bash Prompt HOWTO](http://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/)
- **Terminal Colors (Arch Wiki)**: Terminal color configuration
  - [Arch Wiki: Color output in console](https://wiki.archlinux.org/title/Color_output_in_console)

### Interactive Tools
- **ANSI Escape Sequences Viewer**: Visual reference
  - [ANSI Escape Sequences](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)
- **Terminal Color Test Scripts**: Test your terminal's color support
  - [256colors.pl](https://github.com/eikenb/terminal-colors)
  - [colortest](https://github.com/pablopunk/colortest)

### Technical References
- **XTerm Control Sequences**: Comprehensive reference for xterm-compatible terminals
  - [XTerm Control Sequences](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)
- **Console Codes (Linux)**: Linux kernel console codes
  - [Linux Console Codes](https://www.kernel.org/doc/html/latest/admin-guide/console.html)

### Terminal Emulator Documentation
- **iTerm2**: [iTerm2 Documentation](https://iterm2.com/documentation.html)
- **Windows Terminal**: [Windows Terminal Documentation](https://docs.microsoft.com/en-us/windows/terminal/)
- **Alacritty**: [Alacritty Documentation](https://github.com/alacritty/alacritty/blob/master/docs/escape_support.md)

## Common Patterns

### Progress Indicators
```bash
# Spinner
for i in {1..10}; do
  echo -ne "\r\033[KProcessing... $i/10"
  sleep 0.5
done
```

### Colored Output
```bash
# Success/Error messages
echo -e "\033[32m✓ Success\033[0m"
echo -e "\033[31m✗ Error\033[0m"
```

### Status Lines
```bash
# Update status without newline
echo -ne "\033[2K\r\033[32mStatus: OK\033[0m"
```

## Best Practices

1. **Always reset**: End sequences with `\033[0m` to prevent color bleeding
2. **Check terminal support**: Not all terminals support all features
3. **Use sparingly**: Too many escape codes can make output hard to read
4. **Test in multiple terminals**: Ensure compatibility across different terminals
5. **Consider accessibility**: Some users may have color vision deficiencies

## Further Reading

- Study the source code of terminal applications like `htop`, `vim`, or `tmux` to see real-world usage
- Experiment with `tput` command (part of `ncurses`) for portable terminal control
- Explore terminal multiplexers like `tmux` and `screen` for advanced terminal features





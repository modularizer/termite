"""Bash/shell syntax highlighter."""

import re


def highlight_bash(lines: list[str]) -> list[str]:
    """Bash/shell syntax highlighting."""
    styled_lines = []
    
    # Keywords
    keywords = r'\b(if|then|else|elif|fi|for|while|do|done|case|esac|function|select|until)\b'
    # Commands
    commands = r'^\s*(\w+)(?=\s|$)'
    # Variables
    variables = r'\$\{?\w+\}?'
    # Strings
    strings = r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
    # Comments
    comments = r'(#.*$)'
    # Operators
    operators = r'(&&|\|\||[=!<>]+|[-+*/%])'
    # Shebang
    shebang = r'^(#!.*$)'
    
    for line in lines:
        if not line.strip():
            styled_lines.append('')
            continue
        
        escaped = line.replace('[', '%[').replace(']', '%]')
        styled = escaped
        
        # Shebang
        styled = re.sub(shebang, lambda m: f'GRAY[{m.group(0)}]', styled)
        # Comments
        styled = re.sub(comments, lambda m: f'GRAY[{m.group(0)}]', styled)
        # Strings
        styled = re.sub(strings, lambda m: f'GREEN[{m.group(0)}]', styled)
        # Variables
        styled = re.sub(variables, lambda m: f'CYAN[{m.group(0)}]', styled)
        # Commands (at start of line)
        styled = re.sub(commands, lambda m: f'BOLDBLUE[{m.group(0)}]', styled)
        # Keywords
        styled = re.sub(keywords, lambda m: f'BOLDMAGENTA[{m.group(0)}]', styled)
        # Operators
        styled = re.sub(operators, lambda m: f'BOLDRED[{m.group(0)}]', styled)
        
        styled_lines.append(styled)
    
    return styled_lines




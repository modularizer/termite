"""Python syntax highlighter."""

import re


def highlight_generic(lines: list[str]) -> list[str]:
    """Python syntax highlighting."""
    styled_lines = []

    # Keywords
    keywords = r'\b(async|await|function|object|def|class|if|elif|else|for|while|try|except|finally|with|import|from|as|return|yield|pass|break|continue|lambda|and|or|not|in|of|is|None|True|False|true|false|null|undefined)\b'
    # Types and built-ins
    types = r'\b(int|str|float|bool|list|dict|tuple|set|frozenset|bytes|bytearray|object|type|NoneType|number|string|Array|Record)\b'
    self = r'\b(self)\b'
    # String literals
    strings = r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
    # Numbers
    numbers = r'\b\d+\.?\d*\b'
    # Operators
    operators = r'(==|!=|<=|>=|<<|>>|\*\*|//|[-+*/%=<>!&|^~])'
    # Comments
    comments = r'(#.*$)'
    # Function/class names (after def/class)
    func_names = r'\b(def|class|function)\s+(\w+)'

    for line in lines:
        if not line.strip():
            styled_lines.append('')
            continue

        # Escape brackets first
        escaped = line.replace('[', '%[').replace(']', '%]')

        # First, extract comments and replace with placeholders
        # This prevents styling content inside comments
        comment_placeholders = []
        comment_counter = 0

        def replace_comment(match):
            nonlocal comment_counter
            comment_text = match.group(0)
            placeholder = f'__COMMENT_PLACEHOLDER_{comment_counter}__'
            comment_placeholders.append((placeholder, comment_text))
            comment_counter += 1
            return placeholder

        # Replace comments with placeholders
        code_part = re.sub(comments, replace_comment, escaped)

        # Now style only the code part (comments are protected)
        styled = code_part

        # Strings
        styled = re.sub(strings, lambda m: f'GREEN[{m.group(0)}]', styled)

        # Function/class definitions
        styled = re.sub(func_names, lambda m: f'BOLDBLUE[{m.group(1)}] BOLDYELLOW[{m.group(2)}]', styled)

        # Types
        styled = re.sub(types, lambda m: f'CYAN[{m.group(0)}]', styled)
        styled = re.sub(self, lambda m: f'CYANMAGENTA[{m.group(0)}]', styled)

        # Keywords
        styled = re.sub(keywords, lambda m: f'BOLDMAGENTA[{m.group(0)}]', styled)

        # Numbers
        styled = re.sub(numbers, lambda m: f'YELLOW[{m.group(0)}]', styled)

        # Operators
        styled = re.sub(operators, lambda m: f'BOLDRED[{m.group(0)}]', styled)

        # Now restore comments with their styling (GRAY only, no other styling)
        for placeholder, comment_text in comment_placeholders:
            styled = styled.replace(placeholder, f'GRAY[{comment_text}]')

        styled_lines.append(styled)

    return styled_lines




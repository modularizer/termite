import termite.raw as R
from termite.colors import TerminalCode, merge_colors
import termite.cursor as cursor
import re

keys = [x for x in dir(R) if x.upper() == x and not x.startswith('_')]
keys += [k.replace("_","") for k in keys if k.replace("_","") != k]
rx = "|".join(keys)

def _hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        # Shorthand like #258 -> #225588
        r = int(hex_str[0], 16) * 17
        g = int(hex_str[1], 16) * 17
        b = int(hex_str[2], 16) * 17
    elif len(hex_str) == 6:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
    else:
        raise ValueError(f"Invalid hex color: {hex_str}")
    return (r, g, b)

def _parse_rgb_params(params: str) -> tuple[int, int, int]:
    """Parse RGB parameters from string like '#258' or '255,100,50'."""
    params = params.strip()
    if params.startswith('#'):
        return _hex_to_rgb(params)
    elif ',' in params:
        parts = [int(x.strip()) for x in params.split(',')]
        if len(parts) == 3:
            return tuple(parts)
        else:
            raise ValueError(f"Invalid RGB tuple: {params}")
    else:
        raise ValueError(f"Invalid RGB format: {params}")

def _get_single_code(key: str) -> str:
    """Get ANSI code for a single key, handling underscores and case."""
    # Try exact match first
    if hasattr(R, key):
        code = getattr(R, key)
        if isinstance(code, str):
            return code
        # If it's a function, we can't use it directly here
        return ""
    
    # Try adding underscores in common positions (e.g., BGRGB -> BG_RGB, FGRGB -> FG_RGB)
    # Pattern: if key is all uppercase and has pattern like XXYYY, try XX_YYY
    if key.isupper() and len(key) > 3:
        # Try inserting underscore before last 3+ uppercase letters
        match = re.match(r'^([A-Z]{2,3})([A-Z]{3,})$', key)
        if match:
            variant = f"{match.group(1)}_{match.group(2)}"
            if hasattr(R, variant):
                code = getattr(R, variant)
                if isinstance(code, str):
                    return code
    
    # Try all uppercase/lowercase variants
    for variant in [key.upper(), key.lower()]:
        if hasattr(R, variant):
            code = getattr(R, variant)
            if isinstance(code, str):
                return code
    
    return ""

def _is_color_key(key: str, group: str = "fg") -> bool:
    """Check if a key is a color (in fg or bg group)."""
    tc = TerminalCode.retrieve(key, group)
    return tc is not None and tc.rgb is not None

def _is_style_key(key: str) -> bool:
    """Check if a key is a style (in styles group)."""
    tc = TerminalCode.retrieve(key, "styles")
    return tc is not None

def _is_valid_key(key: str) -> bool:
    """Check if a key is valid (either in raw module or TerminalCode registry)."""
    # Check raw module first
    if _get_single_code(key):
        return True
    # Check TerminalCode registry for styles, fg, bg
    if TerminalCode.retrieve(key, "styles"):
        return True
    if TerminalCode.retrieve(key, "fg"):
        return True
    if TerminalCode.retrieve(key, "bg"):
        return True
    return False

def _parse_stacked_keys(key: str) -> list[tuple[str, str]] | None:
    """
    Parse a stacked key like BOLDITALICREDBLUE into a list of (key, type) tuples.
    Returns None if parsing fails.
    Types: 'fg', 'bg', 'style'
    
    IMPORTANT: Always tries longest keys first to avoid matching shorter keys
    when longer valid keys exist (e.g., "RED" before "R", "BOLD" before "B").
    """
    if not key or not key.isupper():
        return None
    
    result = []
    i = 0
    
    while i < len(key):
        # Try to find the longest valid key starting at position i
        found = False
        # Try from longest to shortest (up to 15 chars for long color names, down to 1 for single chars)
        max_length = min(15, len(key) - i)
        for length in range(max_length, 0, -1):  # Start from longest, go down to 1
            candidate = key[i:i+length]
            
            # Check if it's a valid key (check all sources)
            if _is_valid_key(candidate):
                # Determine type - check in order: fg, bg, styles
                key_type = None
                if _is_color_key(candidate, "fg"):
                    key_type = "fg"
                elif _is_color_key(candidate, "bg"):
                    key_type = "bg"
                elif _is_style_key(candidate):
                    key_type = "style"
                else:
                    # Has a code but not in expected groups, treat as style
                    key_type = "style"
                
                result.append((candidate, key_type))
                i += length
                found = True
                break  # Always use the longest match found
        
        if not found:
            # Can't parse further
            return None
    
    return result if result else None

def _get_code(key: str) -> str:
    """Get ANSI code for a key, handling stacked keys like BOLDITALICREDBLUE."""
    # Try exact match first
    code = _get_single_code(key)
    if code:
        return code
    
    # Try to parse as stacked keys
    if len(key) > 4 and key.isupper():
        parsed = _parse_stacked_keys(key)
        if parsed and len(parsed) > 0:
            # Separate by type
            styles = []
            fg_colors = []
            bg_colors = []
            
            for k, ktype in parsed:
                if ktype == "style":
                    styles.append(k)
                elif ktype == "fg":
                    fg_colors.append(k)
                elif ktype == "bg":
                    bg_colors.append(k)
            
            result_codes = []
            
            # Add style codes
            for style_key in styles:
                style_code = _get_single_code(style_key)
                if style_code:
                    result_codes.append(style_code)
            
            # Merge foreground colors if any
            if len(fg_colors) > 0:
                # Get all color TerminalCodes
                fg_tcs = []
                for fg_color in fg_colors:
                    tc = TerminalCode.retrieve(fg_color, "fg")
                    if tc and tc.rgb:
                        fg_tcs.append(tc)
                    else:
                        # If any color is invalid, fallback to individual codes
                        for fg in fg_colors:
                            fg_code = _get_single_code(fg)
                            if fg_code:
                                result_codes.append(fg_code)
                        fg_tcs = []
                        break
                
                if fg_tcs:
                    # Merge all colors together
                    if len(fg_tcs) == 1:
                        result_codes.append(str(fg_tcs[0]))
                    else:
                        # Start with first color
                        merged = fg_tcs[0]
                        for fg_tc in fg_tcs[1:]:
                            merged_result = merge_colors(merged, fg_tc, "fg")
                            if merged_result:
                                merged = merged_result
                            else:
                                # Can't merge, add individually
                                result_codes.append(str(merged))
                                for remaining in fg_tcs[fg_tcs.index(fg_tc):]:
                                    result_codes.append(str(remaining))
                                merged = None
                                break
                        
                        if merged:
                            result_codes.append(str(merged))
            
            # Merge background colors if any
            if len(bg_colors) > 0:
                # Get all color TerminalCodes
                bg_tcs = []
                for bg_color in bg_colors:
                    tc = TerminalCode.retrieve(bg_color, "bg")
                    if tc and tc.rgb:
                        bg_tcs.append(tc)
                    else:
                        # If any color is invalid, fallback to individual codes
                        for bg in bg_colors:
                            bg_code = _get_single_code(bg)
                            if bg_code:
                                result_codes.append(bg_code)
                        bg_tcs = []
                        break
                
                if bg_tcs:
                    # Merge all colors together
                    if len(bg_tcs) == 1:
                        result_codes.append(str(bg_tcs[0]))
                    else:
                        # Start with first color
                        merged = bg_tcs[0]
                        for bg_tc in bg_tcs[1:]:
                            merged_result = merge_colors(merged, bg_tc, "bg")
                            if merged_result:
                                merged = merged_result
                            else:
                                # Can't merge, add individually
                                result_codes.append(str(merged))
                                for remaining in bg_tcs[bg_tcs.index(bg_tc):]:
                                    result_codes.append(str(remaining))
                                merged = None
                                break
                        
                        if merged:
                            result_codes.append(str(merged))
            
            if result_codes:
                return "".join(result_codes)
    
    return ""

def _has_nested_const(text: str, prefix: str) -> bool:
    """Check if text contains any valid KEY patterns (KEY(...) or KEY...RESET)."""
    i = 0
    while i < len(text):
        # Handle empty prefix specially - only match if current char is uppercase
        if prefix == "":
            if not text[i].isupper():
                i += 1
                continue
            key_start = i
        elif text[i:i+len(prefix)] == prefix:
            key_start = i + len(prefix)
        else:
            i += 1
            continue
        
        key_end = key_start
        # Extract the key
        while key_end < len(text) and (text[key_end].isupper() or text[key_end] == '_'):
            key_end += 1
        
        if key_end > key_start:
            key = text[key_start:key_end]
            # Check if it's a valid key (not just any uppercase sequence)
            if _is_valid_key(key):
                # Check if it's actually being used as a pattern:
                # 1. Followed by '(' (function call)
                # 2. Or followed by non-uppercase and then RESET (simple substitution)
                if key_end < len(text):
                    if text[key_end] == '(':
                        # Function call pattern
                        return True
                    else:
                        # Check for simple substitution pattern: KEY...RESET
                        if prefix == "":
                            reset_pattern = "RESET"
                        else:
                            reset_pattern = prefix + "RESET"
                        if reset_pattern in text[key_end:]:
                            return True
        i += 1
    return False

def sub(text: str, name="", esc="%", esc2=None):
    """
    Substitute KEY patterns with ANSI codes.
    
    Step 1: Escape all groups of {esc}.*?{esc2} to protect them from substitution
    Step 2: Replace constants NOT followed by parentheses (e.g., GREENtextRESET)
    Step 3: Replace constants with parentheses that have NO nested constants inside
            (e.g., GREEN(ok) but NOT RED(BOLD(x))), repeat until none left.
    Step 4: Restore escaped content back
    
    Supports:
    - GREEN(...) - function call with parentheses
    - GREENtextRESET - simple substitution until RESET
    - FGRGB(#258)(text) - RGB with hex color
    - FGRGB(255,100,50)(text) - RGB with tuple
    
    Args:
        text: Text to process
        name: Prefix for keys (default: "")
        esc: Escape start delimiter (default: "%")
        esc2: Escape end delimiter (default: same as esc)
    """
    if not text:
        return text
    
    esc2 = esc2 if esc2 is not None else esc
    
    # Step 1: Escape all groups of {esc}.*?{esc2}
    escaped_parts = []
    escaped_text = text
    placeholder_prefix = "\x00ESCAPED_"
    placeholder_counter = 0
    
    if esc and esc2:
        import re
        # Find all escape sequences (non-greedy match)
        pattern = re.escape(esc) + r'(.*?)' + re.escape(esc2)
        matches = list(re.finditer(pattern, escaped_text))
        
        # Replace from end to start to preserve indices
        for match in reversed(matches):
            placeholder = f"{placeholder_prefix}{placeholder_counter}\x00"
            escaped_parts.append((placeholder, match.group(1)))  # Store (placeholder, original_content)
            escaped_text = escaped_text[:match.start()] + placeholder + escaped_text[match.end():]
            placeholder_counter += 1
    
    # Reverse the list so we restore in the correct order
    escaped_parts.reverse()
    
    # Step 2 & 3: Run the substitution on the escaped text
    result = _sub(escaped_text, name=name)
    
    # Step 4: Restore escaped content back
    for placeholder, original_content in escaped_parts:
        result = result.replace(placeholder, original_content)
    
    return result


def _sub(text: str, name=""):
    """
    Substitute KEY patterns with ANSI codes.

    Step 1: Replace constants NOT followed by parentheses (e.g., GREENtextRESET)
    Step 2: Replace constants with parentheses that have NO nested constants inside
            (e.g., GREEN(ok) but NOT RED(BOLD(x))), repeat until none left.

    Supports:
    - GREEN(...) - function call with parentheses
    - GREENtextRESET - simple substitution until RESET
    - FGRGB(#258)(text) - RGB with hex color
    - FGRGB(255,100,50)(text) - RGB with tuple
    - GREEN - standalone key returns its code
    """
    if not text:
        return text
    
    prefix = name
    
    # Special case: if the entire text is just a valid key (with optional prefix), return its code
    if prefix == "":
        if text.isupper() and _is_valid_key(text):
            code = _get_code(text)
            if code:
                return code
    elif text == prefix or (text.startswith(prefix) and text[len(prefix):].isupper()):
        key = text[len(prefix):] if text.startswith(prefix) else text
        if key and _is_valid_key(key):
            code = _get_code(key)
            if code:
                return code
    
    # Step 1: Replace constants NOT followed by parentheses
    result = []
    i = 0
    
    while i < len(text):
        # Handle empty prefix specially - only match if current char is uppercase
        if prefix == "":
            if not text[i].isupper():
                result.append(text[i])
                i += 1
                continue
            key_start = i
        elif text[i:i+len(prefix)] == prefix:
            key_start = i + len(prefix)
        else:
            result.append(text[i])
            i += 1
            continue
        
        key_end = key_start
        
        # Extract the key
        while key_end < len(text) and (text[key_end].isupper() or text[key_end] == '_'):
            key_end += 1
        
        if key_end > key_start:
            key = text[key_start:key_end]
            
            # Check if followed by parentheses
            if key_end < len(text) and text[key_end] == '(':
                # Has parentheses, skip for now (will handle in step 2)
                result.append(text[i:key_end])
                i = key_end
            else:
                # No parentheses - check for cursor functions first
                cursor_result = None
                if key == "LEFT":
                    cursor_result = cursor.left()
                elif key == "RIGHT":
                    cursor_result = cursor.right()
                elif key == "UP":
                    cursor_result = cursor.up()
                elif key == "DOWN":
                    cursor_result = cursor.down()
                elif key == "CLEAR":
                    cursor_result = cursor.clear_line()
                elif key == "ERASE":
                    cursor_result = cursor.erase_line()
                elif key == "BACK":
                    cursor_result = cursor.backspace()
                elif key == "ROW":
                    cursor_result = cursor.row()
                elif key == "COL":
                    cursor_result = cursor.col()
                
                if cursor_result:
                    result.append(cursor_result)
                    i = key_end
                else:
                    # No parentheses - handle simple substitution: KEY...RESET
                    if prefix == "":
                        reset_pattern = "RESET"
                    else:
                        reset_pattern = prefix + "RESET"
                    reset_pos = text.find(reset_pattern, key_end)
                    
                    if reset_pos != -1:
                        content = text[key_end:reset_pos]
                        code = _get_code(key)
                        if code:
                            result.append(code)
                            result.append(content)
                            result.append(R.RESET)
                            i = reset_pos + len(reset_pattern)
                        else:
                            result.append(text[i:reset_pos + len(reset_pattern)])
                            i = reset_pos + len(reset_pattern)
                    else:
                        result.append(text[i:key_end])
                        i = key_end
        else:
            result.append(text[i])
            i += 1
    
    text = "".join(result)
    
    # Step 2: Replace constants with parentheses that have NO nested constants inside
    # Repeat until no more replacements can be made
    changed = True
    while changed:
        changed = False
        result = []
        i = 0
        
        while i < len(text):
            # Handle empty prefix specially - only match if current char is uppercase
            if prefix == "":
                if not text[i].isupper():
                    result.append(text[i])
                    i += 1
                    continue
                key_start = i
            elif text[i:i+len(prefix)] == prefix:
                key_start = i + len(prefix)
            else:
                result.append(text[i])
                i += 1
                continue
            
            key_end = key_start
            
            # Extract the key
            while key_end < len(text) and (text[key_end].isupper() or text[key_end] == '_'):
                key_end += 1
            
            if key_end > key_start:
                key = text[key_start:key_end]
                
                # Check if followed by parentheses
                if key_end < len(text) and text[key_end] == '(':
                    # Find matching closing paren
                    paren_count = 0
                    content_start = key_end + 1
                    content_end = content_start
                    
                    while content_end < len(text):
                        if text[content_end] == '(':
                            paren_count += 1
                        elif text[content_end] == ')':
                            if paren_count == 0:
                                break
                            paren_count -= 1
                        content_end += 1
                    
                    if content_end < len(text):
                        inner_content = text[content_start:content_end]
                        
                        # Special handling for WRITEAHEAD/WA - always process, even with nested constants
                        if key == "WRITEAHEAD" or key == "WA":
                            # Recursively process inner content to handle nested codes
                            processed_content = _sub(inner_content, name=prefix)
                            cursor_result = cursor.write_ahead(processed_content)
                            result.append(cursor_result)
                            i = content_end + 1
                            changed = True
                            continue
                        
                        # Check if inner content has nested constants
                        if not _has_nested_const(inner_content, prefix):
                            # No nested constants - can replace
                            
                            # Special handling for RGB functions
                            if key == "FGRGB" or key == "BGRGB":
                                # Check if this looks like RGB params (has # or comma)
                                comma_or_hash = inner_content.find(',') != -1 or inner_content.startswith('#')
                                
                                if comma_or_hash or (inner_content and inner_content[0].isdigit()):
                                    # This might be RGB params, check for second paren group
                                    next_paren = content_end + 1
                                    if next_paren < len(text) and text[next_paren] == '(':
                                        # Find matching closing paren for text
                                        text_start = next_paren + 1
                                        text_end = text_start
                                        paren_count = 0
                                        while text_end < len(text):
                                            if text[text_end] == '(':
                                                paren_count += 1
                                            elif text[text_end] == ')':
                                                if paren_count == 0:
                                                    break
                                                paren_count -= 1
                                            text_end += 1
                                        
                                        if text_end < len(text):
                                            rgb_text = text[text_start:text_end]
                                            # Check if rgb_text has nested constants
                                            if not _has_nested_const(rgb_text, prefix):
                                                try:
                                                    r, g, b = _parse_rgb_params(inner_content)
                                                    if key == "FGRGB":
                                                        code = R.FG_RGB(r, g, b)
                                                    else:
                                                        code = R.BG_RGB(r, g, b)
                                                    result.append(code)
                                                    result.append(rgb_text)
                                                    result.append(R.RESET)
                                                    i = text_end + 1
                                                    changed = True
                                                    continue
                                                except (ValueError, AttributeError):
                                                    pass
                            
                            # Special handling for cursor control functions
                            cursor_result = None
                            if key == "LEFT":
                                try:
                                    n = int(inner_content.strip()) if inner_content.strip() else 1
                                    cursor_result = cursor.left(n)
                                except (ValueError, AttributeError):
                                    pass
                            elif key == "RIGHT":
                                try:
                                    n = int(inner_content.strip()) if inner_content.strip() else 1
                                    cursor_result = cursor.right(n)
                                except (ValueError, AttributeError):
                                    pass
                            elif key == "UP":
                                try:
                                    n = int(inner_content.strip()) if inner_content.strip() else 1
                                    cursor_result = cursor.up(n)
                                except (ValueError, AttributeError):
                                    pass
                            elif key == "DOWN":
                                try:
                                    n = int(inner_content.strip()) if inner_content.strip() else 1
                                    cursor_result = cursor.down(n)
                                except (ValueError, AttributeError):
                                    pass
                            elif key == "POS":
                                # POS(r,c) - two comma-separated arguments
                                try:
                                    parts = [p.strip() for p in inner_content.split(',')]
                                    if len(parts) == 2:
                                        r = int(parts[0])
                                        c = int(parts[1])
                                        cursor_result = cursor.pos(r, c)
                                except (ValueError, AttributeError):
                                    pass
                            elif key == "ROW":
                                try:
                                    n = int(inner_content.strip()) if inner_content.strip() else 0
                                    cursor_result = cursor.row(n)
                                except (ValueError, AttributeError):
                                    pass
                            elif key == "COL":
                                try:
                                    n = int(inner_content.strip()) if inner_content.strip() else 0
                                    cursor_result = cursor.col(n)
                                except (ValueError, AttributeError):
                                    pass
                            elif key == "CLEAR":
                                # CLEAR() - no arguments needed
                                cursor_result = cursor.clear_line()
                            elif key == "ERASE":
                                # ERASE() - no arguments needed
                                cursor_result = cursor.erase_line()
                            elif key == "BACK":
                                # BACK() - no arguments needed
                                cursor_result = cursor.backspace()
                            # WRITEAHEAD/WA is handled earlier, before nested constants check
                            
                            if cursor_result:
                                result.append(cursor_result)
                                i = content_end + 1
                                changed = True
                                continue
                            
                            # Regular function call - no nested constants
                            code = _get_code(key)
                            if code:
                                result.append(code)
                                result.append(inner_content)
                                result.append(R.RESET)
                                i = content_end + 1
                                changed = True
                                continue
                        
                        # Has nested constants or couldn't replace, keep as-is
                        result.append(text[i:content_end+1])
                        i = content_end + 1
                    else:
                        result.append(text[i:key_end])
                        i = key_end
                else:
                    result.append(text[i:key_end])
                    i = key_end
            else:
                result.append(text[i])
                i += 1
        
        text = "".join(result)
    
    return text


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
    demo("B(bold) I(italic) U(underline)", name="")
    
    print("=== Sample 18: Combined shortened aliases ===")
    demo("BIU(bold italic underline)", name="")
    
    print("=== Sample 19: Short aliases with colors ===")
    demo("BRED(bold red) IBLUE(italic blue) UGREEN(underline green)", name="")
    
    print("=== Sample 20: Stacked short aliases and colors ===")
    demo("BIRED(bold italic red)", name="")
    
    print("=== Sample 21: More short alias combinations ===")
    demo("BUREDBLUE(bold underline merged red+blue)", name="")
    
    print("=== Sample 22: All short style aliases ===")
    demo("B(bold) D(dim) I(italic) U(underline) S(strikethrough) R(reverse)", name="")
    
    print("=== Sample 23: Cursor control functions ===")
    demo("LEFT RIGHT UP DOWN", name="")
    
    print("=== Sample 24: Cursor functions with arguments ===")
    demo("LEFT(3) RIGHT(5) UP(2) DOWN(4)", name="")
    
    print("=== Sample 25: Cursor position and line control ===")
    demo("POS(10,20) ROW(5) COL(10) CLEAR ERASE BACK", name="")
    
    print("=== Sample 26: Write ahead cursor function ===")
    demo("WRITEAHEAD(suggestion text)", name="")
    
    print("=== Sample 26b: Write ahead alias (WA) ===")
    demo("WA(short alias)", name="")
    
    print("=== Sample 27: Combined cursor and colors ===")
    demo("RED(Hello)LEFT(5)GREEN(World)", name="")
    
    print("=== Sample 28: Escape mechanism ===")
    demo("%RED(text)%", name="")  # Escaped - should not be processed
    demo("RED(%text%)", name="")  # Partially escaped
    demo("RED(normal) %GREEN(escaped)% RED(back)", name="")


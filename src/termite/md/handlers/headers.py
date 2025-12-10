"""Header handlers for markdown rendering."""

from typing import Dict

# Lazy imports to avoid circular dependencies
def _get_big_text():
    from termite.art.big import big_text
    return big_text

def _get_termite_colors():
    from termite.fancy import t
    return t


def register_header_handlers(renderer):
    """Register header handlers (# ## ### etc.)."""
    
    def header_handler(text: str, groups: Dict) -> str:
        level = len(groups.get('level', '#'))
        content = groups.get('text', '').strip()
        # Get terminal width from renderer
        terminal_width = getattr(renderer, 'terminal_width', 80)
        
        if level == 1:
            # h1: Use BIG text followed by dashes
            # Call big_text directly to avoid sub() duplication issues
            big_text = _get_big_text()
            big_output = big_text(content)
            # Use terminal width for dash line
            width = terminal_width
            # Escape the BIG output to prevent sub() from processing it
            escaped_big = big_output.replace('[', '%[').replace(']', '%]')
            return f"\n{escaped_big}\nGRAY[{'─' * width}]\n"
        else:
            # For h2-h6, apply styling directly to avoid sub() duplication issues
            # We'll return a special marker that the renderer will handle
            # Use terminal width for h2 and h3, content width for others
            if level in (2, 3):
                width = terminal_width
            else:
                width = max(len(content), 70)
            dash_line = '─' * width
            
            # Use a special format that won't be processed by sub()
            # The renderer will handle these specially
            # Use a unique marker for dashes that won't conflict
            if level == 2:
                # Return raw content with a marker - renderer will style it
                return f"\n__HEADER_H2__{content}__END__\n__UNDERLINE__{dash_line}__END__\n"
            elif level == 3:
                return f"\n__HEADER_H3__{content}__END__\n__UNDERLINE__{dash_line}__END__\n"
            elif level == 4:
                return f"\n__HEADER_H4__{content}__END__\n__UNDERLINE__{dash_line}__END__\n"
            elif level == 5:
                return f"\n__HEADER_H5__{content}__END__\n__UNDERLINE__{dash_line}__END__\n"
            else:
                return f"\n__HEADER_H6__{content}__END__\n__UNDERLINE__{dash_line}__END__\n"
    
    renderer.register_handler(r'^(?P<level>#{1,6})\s+(?P<text>.*)$', header_handler)


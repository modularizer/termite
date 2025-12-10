"""Block-level handlers (blockquotes, horizontal rules)."""

from typing import Dict


def register_block_handlers(renderer):
    """Register block-level handlers."""
    
    # Horizontal rule (--- or ***)
    def hr_handler(text: str, groups: Dict) -> str:
        # Get terminal width from renderer
        terminal_width = getattr(renderer, 'terminal_width', 80)
        return '\n' + "GRAY[" + "─" * terminal_width + "]" + '\n'
    
    renderer.register_handler(r'^[\-\*]{3,}$', hr_handler)
    
    # Blockquotes (> text)
    def blockquote_handler(text: str, groups: Dict) -> str:
        content = groups.get('text', '').strip()
        lines = content.split('\n')
        return '\n'.join(f"  GRAY[│] GRAY[{line}]" for line in lines if line) + '\n'
    
    renderer.register_handler(r'^>\s+(?P<text>.*?)$', blockquote_handler)


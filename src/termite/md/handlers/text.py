"""Text formatting handlers (bold, italic, etc.)."""

from typing import Dict


def register_text_handlers(renderer):
    """Register text formatting handlers."""
    
    # Bold (**text** or __text__)
    def bold_handler(text: str, groups: Dict) -> str:
        content = groups.get('text', '')
        return f"BOLD[{content}]"
    
    renderer.register_handler(r'\*\*(?P<text>.*?)\*\*', bold_handler)
    renderer.register_handler(r'__(?P<text>.*?)__', bold_handler)
    
    # Italic (*text* or _text_)
    def italic_handler(text: str, groups: Dict) -> str:
        content = groups.get('text', '')
        return f"ITALIC[{content}]"
    
    renderer.register_handler(r'(?<!\*)\*(?P<text>[^*]+?)\*(?!\*)', italic_handler)
    renderer.register_handler(r'(?<!_)_(?P<text>[^_]+?)_(?!_)', italic_handler)




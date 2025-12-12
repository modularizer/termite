"""List handlers (ordered and unordered)."""

from typing import Dict


def register_list_handlers(renderer):
    """Register list handlers."""
    
    # Unordered lists (- item or * item)
    def list_item_handler(text: str, groups: Dict) -> str:
        content = groups.get('text', '').strip()
        return f"  YELLOW[•] {content}"
    
    renderer.register_handler(r'^[\-\*]\s+(?P<text>.*?)$', list_item_handler)
    
    # Ordered lists (1. item)
    def ordered_list_handler(text: str, groups: Dict) -> str:
        num = groups.get('num', '')
        content = groups.get('text', '').strip()
        return f"  CYAN[{num}.] {content}"
    
    renderer.register_handler(r'^(?P<num>\d+)\.\s+(?P<text>.*?)$', ordered_list_handler)




"""Link and image handlers."""

from typing import Dict


def register_link_handlers(renderer):
    """Register link and image handlers."""
    
    # Links ([text](url))
    def link_handler(text: str, groups: Dict) -> str:
        link_text = groups.get('text', '')
        url = groups.get('url', '')
        return f"UNDERLINEBLUE[{link_text}] GRAY[(<{url}>)]"
    
    renderer.register_handler(r'\[(?P<text>.*?)\]\((?P<url>.*?)\)', link_handler)
    
    # Images (![alt](url))
    def image_handler(text: str, groups: Dict) -> str:
        alt = groups.get('alt', '')
        url = groups.get('url', '')
        return f"GRAY[[Image: ]YELLOW[{alt}] GRAY[({url})]]"
    
    renderer.register_handler(r'!\[(?P<alt>.*?)\]\((?P<url>.*?)\)', image_handler)




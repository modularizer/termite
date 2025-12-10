"""Code block and inline code handlers."""

from typing import Dict

from termite import box, sub
from termite.art.box import indent_text


def register_code_handlers(renderer):
    """Register code-related handlers."""
    
    # Inline code (`code`)
    def code_handler(text: str, groups: Dict) -> str:
        content = groups.get('text', '')
        return f"BGGRAYGRAY[{content}]"
    
    renderer.register_handler(r'`(?P<text>[^`]+?)`', code_handler)
    
    # Code blocks are handled separately in the renderer
    # This function sets up the code block handler
    def code_block_handler(text: str, groups: Dict) -> str:
        content = groups.get('text', '').strip()
        lang = groups.get('lang', '').strip().lower()
        lines = content.split('\n')

        # Apply syntax highlighting based on language
        highlighted_lines = renderer._highlight_code(lines, lang)
        content = sub("\n".join(highlighted_lines))
        return indent_text(box(content, bg="#eee"), "    ") + '\n'
    
    renderer._code_block_handler = code_block_handler

if __name__ == "__main__":
    from termite.md import render
    print(render('''
```python
class Example:
    """An example class."""
    
    def __init__(self, name: str):
        self.name = name
    
    def greet(self):
        print(f"Hello, {self.name}!")
```
'''))
"""
Markdown renderer that converts markdown to styled terminal text using termite.

This module provides the main MarkdownRenderer class that processes markdown
and applies termite styling for colors, formatting, and syntax highlighting.
"""

import re
import shutil
from typing import Callable, Dict, Optional

from .handlers import (
    register_header_handlers,
    register_text_handlers,
    register_code_handlers,
    register_link_handlers,
    register_list_handlers,
    register_block_handlers,
)
from .handlers.syntax import highlight_python, highlight_bash, highlight_generic


class MarkdownRenderer:
    """
    A markdown renderer that converts markdown to styled terminal text using termite.
    
    Handlers can be registered to customize rendering of different markdown elements.
    All handlers should return termite formatting strings (e.g., "BOLD[text]").
    """
    
    def __init__(self):
        self.handlers: Dict[str, Callable[[str, Dict], str]] = {}
        self._code_block_handler: Optional[Callable[[str, Dict], str]] = None
        self._syntax_highlighters: Dict[str, Callable[[list[str]], list[str]]] = {}
        # Get terminal width
        try:
            cols, _ = shutil.get_terminal_size()
            self.terminal_width = cols
        except Exception:
            # Fallback to 80 if we can't get terminal size
            self.terminal_width = 80
        self._register_default_handlers()
        self._register_default_syntax_highlighters()
    
    def register_handler(self, pattern: str, handler: Callable[[str, Dict], str]):
        """
        Register a custom handler for a markdown pattern.
        
        Args:
            pattern: A regex pattern to match (should include capturing groups)
            handler: A function that takes (match_text, groups_dict) and returns termite formatting string
                    groups_dict contains named groups from the regex pattern
        
        Example:
            renderer.register_handler(
                r'~~(?P<text>.*?)~~',
                lambda text, groups: f"STRIKETHROUGH[{groups['text']}]"
            )
        """
        self.handlers[pattern] = handler
    
    def register_syntax_highlighter(self, language: str, highlighter: Callable[[list[str]], list[str]]):
        """
        Register a syntax highlighter for a specific language.
        
        Args:
            language: Language name (e.g., 'python', 'bash', 'javascript')
            highlighter: Function that takes a list of code lines and returns a list of styled lines
                        Each line should be a termite formatting string
        
        Example:
            def highlight_python(lines):
                # Custom Python highlighting logic
                return styled_lines
            
            renderer.register_syntax_highlighter('python', highlight_python)
        """
        self._syntax_highlighters[language.lower()] = highlighter
    
    def _register_default_handlers(self):
        """Register default handlers for common markdown elements using termite styling."""
        register_header_handlers(self)
        register_text_handlers(self)
        register_code_handlers(self)
        register_link_handlers(self)
        register_list_handlers(self)
        register_block_handlers(self)
    
    def _register_default_syntax_highlighters(self):
        """Register default syntax highlighters for common languages."""
        self.register_syntax_highlighter('python', highlight_python)
        self.register_syntax_highlighter('py', highlight_python)
        self.register_syntax_highlighter('bash', highlight_bash)
        self.register_syntax_highlighter('sh', highlight_bash)
        self.register_syntax_highlighter('shell', highlight_bash)
        self.register_syntax_highlighter('zsh', highlight_bash)
        # Generic fallback
        self._default_highlighter = highlight_generic
    
    def _highlight_code(self, lines: list[str], language: str) -> list[str]:
        """Apply syntax highlighting to code lines based on language."""
        if language and language in self._syntax_highlighters:
            return self._syntax_highlighters[language](lines)
        elif self._default_highlighter:
            return self._default_highlighter(lines)
        else:
            # No highlighting, just escape brackets
            return [line.replace('[', '%[').replace(']', '%]') for line in lines]
    
    def render(self, markdown: str) -> str:
        """
        Render markdown text to styled terminal output using termite.
        
        Args:
            markdown: The markdown text to render
        
        Returns:
            Rendered styled text (ready to print, already processed through sub())
        """
        lines = markdown.split('\n')
        result_lines = []
        in_code_block = False
        code_block_content = []
        code_block_lang = ''
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Handle code blocks (multiline)
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Start of code block
                    in_code_block = True
                    code_block_lang = line.strip()[3:].strip()
                    code_block_content = []
                else:
                    # End of code block
                    in_code_block = False
                    code_text = '\n'.join(code_block_content)
                    # Manually call code block handler
                    groups = {'text': code_text, 'lang': code_block_lang}
                    rendered = self._code_block_handler(f"```{code_block_lang}\n{code_text}```", groups)
                    result_lines.append(rendered)
                    code_block_content = []
                i += 1
                continue
            
            if in_code_block:
                code_block_content.append(line)
                i += 1
                continue
            
            # Process line with handlers
            # Apply handlers in order: headers first (line-level), then inline elements
            processed_line = line
            
            # Headers should be processed first as they're line-level patterns
            header_pattern = r'^(?P<level>#{1,6})\s+(?P<text>.*)$'
            header_match = re.match(header_pattern, processed_line)
            if header_match:
                header_handler = self.handlers.get(header_pattern)
                if header_handler:
                    groups = header_match.groupdict()
                    processed_line = header_handler(header_match.group(0), groups)
                    result_lines.append(processed_line)
                    i += 1
                    continue
            
            # Order matters: apply more specific patterns first for inline elements
            # Define priority order for built-in handlers
            priority_patterns = [
                r'!\[(?P<alt>.*?)\]\((?P<url>.*?)\)',
                r'\[(?P<text>.*?)\]\((?P<url>.*?)\)',
                r'`(?P<text>[^`]+?)`',
                r'\*\*(?P<text>.*?)\*\*',
                r'__(?P<text>.*?)__',
                r'(?<!\*)\*(?P<text>[^*]+?)\*(?!\*)',
                r'(?<!_)_(?P<text>[^_]+?)_(?!_)',
            ]
            
            # Apply priority handlers first
            for pattern in priority_patterns:
                handler = self.handlers.get(pattern)
                if handler:
                    processed_line = self._apply_handler(processed_line, pattern, handler)
            
            # Apply all other handlers (including custom ones, but skip headers)
            for pattern, handler in self.handlers.items():
                if pattern not in priority_patterns and pattern != header_pattern:
                    processed_line = self._apply_handler(processed_line, pattern, handler)
            
            result_lines.append(processed_line)
            i += 1
        
        # Join all lines
        result_text = '\n'.join(result_lines)
        
        # Handle special header markers before sub() processing
        # This avoids sub() duplication issues with certain text patterns
        from termite.fancy import t
        from termite.raw import RESET, BG_GRAY
        
        # Replace dashes first (before closing markers) - use regex to match the pattern
        # Pattern: __UNDERLINE__<dashes>__END__
        def replace_underline(match):
            dashes = match.group(1)
            return str(t.GRAY) + dashes + str(RESET)
        
        result_text = re.sub(r'__UNDERLINE__([─]+)__END__', replace_underline, result_text)
        
        # Replace header markers (before replacing closing __END__)
        result_text = result_text.replace('__HEADER_H2__', str(t.BOLD + t.BLACK))
        result_text = result_text.replace('__HEADER_H3__', str(t.BOLD + t.GRAY))
        result_text = result_text.replace('__HEADER_H4__', str(t.BOLD + t.LIGHT_GRAY))
        result_text = result_text.replace('__HEADER_H5__', str(t.BOLD + t.BRIGHT_BLACK))
        result_text = result_text.replace('__HEADER_H6__', str(t.BOLD + t.WHITE))
        
        # Replace closing markers
        result_text = result_text.replace('__END__', str(RESET))
        
        # Process through sub() to convert termite formatting strings to actual ANSI codes
        # Lazy import to avoid circular dependency
        from termite.sub import sub
        processed = sub(result_text)
        
        # Fix RESET codes in code blocks - they break the background color
        # We need to reapply background after RESET within code block lines
        # Code block lines have BGGRAYGRAY[│] prefix, so we can detect them
        from termite.raw import BG_GRAY
        
        # Pattern to match code block lines: BGGRAYGRAY[│] followed by content
        # After sub(), this becomes ANSI codes, so we look for the border char │
        # and then replace RESET with RESET+BG_GRAY to maintain background
        lines = processed.split('\n')
        fixed_lines = []
        in_code_block = False
        
        for line in lines:
            # Detect code block lines by looking for the border character
            if '│' in line and BG_GRAY in line[:50]:  # Check if it's a code block line
                in_code_block = True
                # Replace RESET with RESET+BG_GRAY to maintain background
                # But we need to be careful - only replace RESET that's not at the end
                # Actually, we want to replace all RESET except the final one
                if RESET in line:
                    # Split by RESET, then rejoin with RESET+BG_GRAY except for the last segment
                    parts = line.split(RESET)
                    if len(parts) > 1:
                        # Rejoin all but the last with RESET+BG_GRAY
                        fixed = (RESET + BG_GRAY).join(parts[:-1]) + RESET + parts[-1]
                        # But we need to ensure the line ends with RESET to close properly
                        if not fixed.endswith(RESET):
                            fixed = fixed + RESET
                        line = fixed
            else:
                in_code_block = False
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _apply_handler(self, text: str, pattern: str, handler: Optional[Callable] = None) -> str:
        """Apply a handler to matching patterns in text."""
        if handler is None:
            handler = self.handlers.get(pattern)
            if handler is None:
                return text
        
        def replace_func(match):
            groups = match.groupdict() if match.groupdict() else {}
            # Also add numbered groups
            for i, group in enumerate(match.groups(), 1):
                if f'group{i}' not in groups:
                    groups[f'group{i}'] = group
            return handler(match.group(0), groups)
        
        try:
            return re.sub(pattern, replace_func, text, flags=re.MULTILINE | re.DOTALL)
        except Exception:
            # If pattern fails, return original text
            return text


"""
Markdown renderer module for termite.

This module provides markdown rendering capabilities with termite styling,
syntax highlighting, and extensible handler system.
"""

import argparse
import sys
from pathlib import Path
from typing import Callable, Dict

from .renderer import MarkdownRenderer

# Default renderer instance
_default_renderer = MarkdownRenderer()


def render(markdown: str) -> str:
    """
    Render markdown to styled terminal text using the default renderer.
    
    Args:
        markdown: The markdown text to render
    
    Returns:
        Rendered styled text (ready to print)
    """
    return _default_renderer.render(markdown)


def register_handler(pattern: str, handler: Callable[[str, Dict], str]):
    """
    Register a custom handler with the default renderer.
    
    Args:
        pattern: A regex pattern to match (should include capturing groups)
        handler: A function that takes (match_text, groups_dict) and returns termite formatting string
    
    Example:
        from termite.md import register_handler
        
        register_handler(
            r'~~(?P<text>.*?)~~',
            lambda text, groups: f"STRIKETHROUGH[{groups['text']}]"
        )
    """
    _default_renderer.register_handler(pattern, handler)


def register_syntax_highlighter(language: str, highlighter: Callable[[list[str]], list[str]]):
    """
    Register a syntax highlighter for a specific language.
    
    Args:
        language: Language name (e.g., 'python', 'bash', 'javascript')
        highlighter: Function that takes a list of code lines and returns a list of styled lines
    
    Example:
        from termite.md import register_syntax_highlighter
        
        def highlight_rust(lines):
            # Custom Rust highlighting
            return styled_lines
        
        register_syntax_highlighter('rust', highlight_rust)
    """
    _default_renderer.register_syntax_highlighter(language, highlighter)


def create_renderer() -> MarkdownRenderer:
    """
    Create a new renderer instance with default handlers.
    
    Returns:
        A new MarkdownRenderer instance
    """
    return MarkdownRenderer()


def _resolve_file(file_arg: str):
    """Resolve file argument to file object."""
    if file_arg == "stdout":
        return sys.stdout
    elif file_arg == "stderr":
        return sys.stderr
    elif file_arg == "/dev/tty":
        try:
            return open("/dev/tty", "w")
        except Exception:
            return sys.stdout
    else:
        return open(file_arg, "w")


def main():
    """CLI entry point for markdown renderer."""
    parser = argparse.ArgumentParser(
        description="Render markdown files to styled terminal text using termite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m termite.md README.md
  python -m termite.md README.md --output rendered.txt
  python -m termite.md README.md --file stderr
  cat README.md | python -m termite.md -
        """
    )
    
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        help="Markdown file to render (use '-' for stdin, default: stdin)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="stdout",
        help="Output destination: 'stdout', 'stderr', '/dev/tty', or file path (default: stdout)"
    )
    
    parser.add_argument(
        "--flush",
        action="store_true",
        help="Flush the output stream after writing"
    )
    
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output raw ANSI codes instead of processing through termite"
    )
    
    args = parser.parse_args()
    
    # Read input
    if args.file == "-" or args.file is None:
        # Read from stdin
        markdown_text = sys.stdin.read()
    else:
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        markdown_text = file_path.read_text()
    
    # Render markdown
    try:
        rendered = render(markdown_text)
    except Exception as e:
        print(f"Error rendering markdown: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    try:
        output_file = _resolve_file(args.output)
        output_file.write(rendered)
        if not rendered.endswith('\n'):
            output_file.write('\n')
        if args.flush:
            output_file.flush()
        if output_file not in (sys.stdout, sys.stderr):
            output_file.close()
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


__all__ = [
    'MarkdownRenderer',
    'render',
    'register_handler',
    'register_syntax_highlighter',
    'create_renderer',
    'main',
]


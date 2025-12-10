"""Markdown handler modules."""

from .headers import register_header_handlers
from .text import register_text_handlers
from .code import register_code_handlers
from .links import register_link_handlers
from .lists import register_list_handlers
from .blocks import register_block_handlers

__all__ = [
    'register_header_handlers',
    'register_text_handlers',
    'register_code_handlers',
    'register_link_handlers',
    'register_list_handlers',
    'register_block_handlers',
]


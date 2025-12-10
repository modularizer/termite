"""Syntax highlighters for different programming languages."""

from .python import highlight_python
from .bash import highlight_bash
from .generic import highlight_generic

__all__ = [
    'highlight_python',
    'highlight_bash',
    'highlight_generic',
]


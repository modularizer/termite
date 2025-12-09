#!/usr/bin/env python3
"""
Termite CLI - Command-line interface for terminal formatting.
"""

import argparse
from termite.sub import sub, _resolve_file, subprint

def raw():
    return main(raw=True)

def main(raw=False):
    parser = argparse.ArgumentParser(
        description="Apply terminal formatting (colors, styles, cursor control) to text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  termite "RED(Error) GREEN(Success)"
  termite "BOLD(Important)" --name TM
  termite "LEFT(3)GREEN(Hello)" --end ""
  termite "RED(text)" --file /dev/stderr
  termite "GREEN(text)" --esc "{" --esc2 "}"
  termite "GREEN(Hello)" --raw
        """
    )
    
    parser.add_argument(
        "text",
        nargs="+",
        help="Text to format (supports patterns like RED(text), BOLD(text), etc.)"
    )

    
    parser.add_argument(
        "-e", "--esc",
        default="%",
        help="Escape start delimiter (default: %)"
    )

    parser.add_argument(
        "-ee", "--esc-end",
        default="",
        help="Escape end delimiter (default: '')"
    )
    parser.add_argument(
        "-p", "--prefix",
        default="",
        help="Color name start char (default: '')"
    )
    parser.add_argument(
        "-s", "--suffix",
        default="",
        help="Color name end char (default: '')"
    )
    parser.add_argument(
        "-o", "--opener",
        default="(",
        help="Group start char (default: '(')"
    )
    parser.add_argument(
        "-c", "--closer",
        default=")",
        help="Group end char (default: ')')"
    )
    parser.add_argument(
        "-j", "--joiner",
        default="+",
        help="Style join char (default: '+')"
    )
    parser.add_argument(
        "--end",
        default="\n",
        help="String appended after the last value (default: newline)"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        default="stdout",
        help="File to write to: 'stdout', 'stderr', '/dev/tty', or file path (default: stdout)"
    )
    
    parser.add_argument(
        "--flush",
        action="store_true",
        help="Flush the output stream"
    )
    
    parser.add_argument(
        "--raw",
        action="store_true",
        default=raw,
        help="Print raw ANSI escape codes instead of applying formatting"
    )

    parser.add_argument(
        "--pretty",
        action="store_false",
        dest="raw",
        default=not raw,
        help="Apply the formatting"
    )
    
    args = parser.parse_args()
    
    # Prepare kwargs for sub()
    kw = {
        "color_prefix": args.prefix,
        "color_suffix": args.suffix,
        "opener": args.opener,
        "closer": args.closer,
        "joiner": args.joiner,
        "esc": args.esc,
        "esc_end": args.esc_end,

        "end": args.end,
        "file": args.file,
        "flush": args.flush,

        "raw": args.raw
    }
    
    # Process each text argument through sub()
    subprint(" ".join(args.text), **kw)
    


if __name__ == "__main__":
    main()

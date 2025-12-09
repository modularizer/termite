#!/usr/bin/env python3
"""
Termite CLI - Command-line interface for terminal formatting.
"""

import argparse
from termite.sub import sub, _resolve_file

def main():
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
        "--name",
        "-n",
        default="",
        help="Prefix for keys (default: empty string)"
    )
    
    parser.add_argument(
        "--esc",
        default="%",
        help="Escape start delimiter (default: %%)"
    )
    
    parser.add_argument(
        "--esc2",
        default=None,
        help="Escape end delimiter (default: same as --esc)"
    )
    
    # Print function kwargs
    parser.add_argument(
        "--sep",
        default=" ",
        help="Separator between text arguments (default: space)"
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
        help="Print raw ANSI escape codes instead of applying formatting"
    )
    
    args = parser.parse_args()
    
    # Prepare kwargs for sub()
    sub_kwargs = {
        "name": args.name,
        "esc": args.esc,
        "esc2": args.esc2,
    }
    
    # Process each text argument through sub()
    processed_texts = [sub(text, **sub_kwargs) for text in args.text]
    
    # Resolve special file values
    output_file = _resolve_file(args.file)
    
    # Prepare kwargs for print()
    print_kwargs = {
        "sep": args.sep,
        "end": args.end,
        "file": output_file,
        "flush": args.flush,
    }
    
    # Print the processed text
    if args.raw:
        # Print raw escape codes (repr format)
        raw_texts = [repr(text) for text in processed_texts]
        print(*raw_texts, **print_kwargs)
    else:
        print(*processed_texts, **print_kwargs)

if __name__ == "__main__":
    main()

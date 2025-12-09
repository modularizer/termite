#!/usr/bin/env python3
"""
Termite CLI - Command-line interface for terminal formatting.
"""

import argparse
from termite.sub import sub, _resolve_file, subprint, ESC_END, ESC, PREFIX, SUFFIX, OPENER, CLOSER, JOINER


def raw():
    return main(raw=True)

def main(raw=False):
    parser = argparse.ArgumentParser(
        description="Apply terminal formatting (colors, styles, cursor control) to text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  termite "RED{OPENER}Error{CLOSER} GREEN{OPENER}Success{CLOSER}"
  termite "BOLD{OPENER}Important{CLOSER}" --name TM
  termite "LEFT{OPENER}3{CLOSER}GREEN{OPENER}Hello{CLOSER}" --end ""
  termite "RED{OPENER}text{CLOSER}" --file /dev/stderr
  termite "GREEN{{text}}" --esc "{{}}"
  termite "GREEN{OPENER}Hello{CLOSER}" --raw
        """
    )
    
    parser.add_argument(
        "text",
        nargs="+",
        help="Text to format (supports patterns like RED(text), BOLD(text), etc.)"
    )

    
    parser.add_argument(
        "-e", "--esc",
        default=f"{ESC}{ESC_END}",
        help=f"Escape  delimiter (default: '{ESC}{ESC_END}')"
    )

    parser.add_argument(
        "-p", "--prefix",
        default=PREFIX,
        help=f"Color name start char (default: '{PREFIX}')"
    )
    parser.add_argument(
        "-s", "--suffix",
        default=SUFFIX,
        help=f"Color name end char (default: '{SUFFIX}')"
    )
    parser.add_argument(
        "-o", "--opener",
        default=OPENER,
        help=f"Group start char (default: '{OPENER}')"
    )
    parser.add_argument(
        "-c", "--closer",
        default=CLOSER,
        help=f"Group end char (default: '{CLOSER}')"
    )
    parser.add_argument(
        "-j", "--joiner",
        default=JOINER,
        help=f"Style join char (default: '{JOINER}')"
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
        "-r", "--raw",
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

    parser.add_argument(
        "-w",
        default=None,
        help="Wrap the value with this opener and closer, in lieu of using -o and -c"
    )
    parser.add_argument(
        "-ps",
        default=None,
        help="Wrap the key with this prefix/suffix, in lieu of using -p and -s"
    )
    
    args = parser.parse_args()
    if args.w is not None:
        args.opener = args.w[0] if len(args.w) > 0 else ""
        args.closer = args.w[1] if len(args.w) > 1 else ""
    if args.ps is not None:
        args.prefix = args.ps[0] if len(args.ps) > 0 else ""
        args.suffix = args.ps[1] if len(args.ps) > 1 else ""

    # Prepare kwargs for sub()
    kw = {
        "color_prefix": args.prefix,
        "color_suffix": args.suffix,
        "opener": args.opener,
        "closer": args.closer,
        "joiner": args.joiner,
        "esc": args.esc[0] if args.esc else "",
        "esc_end": args.esc[1] if len(args.esc) > 1 else "",

        "end": args.end,
        "file": args.file,
        "flush": args.flush,

        "raw": args.raw
    }
    
    # Process each text argument through sub()
    subprint(" ".join(args.text), **kw)
    


if __name__ == "__main__":
    main()

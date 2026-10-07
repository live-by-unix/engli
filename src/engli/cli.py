"""
Command-line interface for Engli.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from . import __version__
from .lexer import Lexer
from .parser import Parser
from .ast import Program
from .runtime import Interpreter
from .diagnostics import DiagnosticReporter


def load_source(filename: str) -> str:
    """Load source code from a file."""
    path = Path(filename)
    if not path.exists():
        print(f"Error: File not found: {filename}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        print(f"Error: Cannot read file: {e}", file=sys.stderr)
        sys.exit(1)


def run_file(filename: str, check_only: bool = False) -> int:
    """Run an Engli file."""
    source = load_source(filename)

    # Lex
    lexer = Lexer(source, filename)
    tokens = lexer.tokenize()

    lexer_errors = lexer.get_errors()
    if lexer_errors:
        reporter = DiagnosticReporter()
        for error in lexer_errors:
            reporter.add_error(error.message, error.location)
        print(reporter.format_all(), file=sys.stderr)
        return 1

    # Parse
    parser = Parser(tokens)
    program = parser.parse()

    parse_errors = parser.get_errors()
    if parse_errors:
        reporter = DiagnosticReporter()
        for error in parse_errors:
            reporter.add_error(error.message, error.location)
        print(reporter.format_all(), file=sys.stderr)
        return 1

    # If check only, stop here
    if check_only:
        print(f"OK: {filename}")
        return 0

    # Interpret
    interpreter = Interpreter()
    interpreter.interpret(program)

    return 0


def main() -> int:
    """Main entry point."""
    # Check if a file is provided directly (no subcommand)
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-") and sys.argv[1] not in ["run", "check", "format", "test", "repl", "--version", "--help"]:
        # Direct file execution: engli file.engli
        filename = sys.argv[1]
        return run_file(filename, check_only=False)

    parser = argparse.ArgumentParser(
        description="Engli - An English-like interpreted programming language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"Engli {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run an Engli program")
    run_parser.add_argument("file", help="Engli file to run")

    # Check command
    check_parser = subparsers.add_parser("check", help="Check an Engli program without running")
    check_parser.add_argument("file", help="Engli file to check")

    # Format command
    format_parser = subparsers.add_parser("format", help="Format an Engli file")
    format_parser.add_argument("file", help="Engli file to format")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run the test suite")

    # REPL command
    repl_parser = subparsers.add_parser("repl", help="Start the REPL")

    args = parser.parse_args()

    # Handle commands
    if args.command == "run":
        return run_file(args.file, check_only=False)

    if args.command == "check":
        return run_file(args.file, check_only=True)

    if args.command == "format":
        from .formatter import Formatter
        source = load_source(args.file)
        formatter = Formatter(source)
        formatted = formatter.format()
        print(formatted)
        return 0

    if args.command == "test":
        import pytest
        return pytest.main(["-v", "tests/"])

    if args.command == "repl":
        from .repl import REPL
        repl = REPL()
        repl.run()
        return 0

    # Show help if no command
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
REPL (Read-Eval-Print Loop) for Engli.
"""

import sys
from typing import Optional, List

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

from ..lexer import Lexer
from ..parser import Parser
from ..runtime import Interpreter, Value, ValueType
from ..diagnostics import DiagnosticReporter


class REPL:
    """Interactive REPL for Engli."""

    def __init__(self):
        self.interpreter = Interpreter()
        self.multiline_buffer: List[str] = []
        self.in_multiline = False

    def run(self) -> None:
        """Run the REPL."""
        print(f"Engli REPL {self._get_version()}")
        print("Type :help for help, :exit to quit")
        print()

        if PROMPT_TOOLKIT_AVAILABLE:
            self._run_with_prompt_toolkit()
        else:
            self._run_basic()

    def _run_with_prompt_toolkit(self) -> None:
        """Run REPL with prompt_toolkit."""
        session = PromptSession(
            history=FileHistory(".engli_history"),
            auto_suggest=AutoSuggestFromHistory(),
        )

        while True:
            try:
                prompt = "... " if self.in_multiline else "> "
                line = session.prompt(prompt)

                if line.startswith(":"):
                    result = self._handle_command(line)
                    if result == "exit":
                        break
                    continue

                self._process_line(line)

            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                self.multiline_buffer = []
                self.in_multiline = False
            except EOFError:
                print("\nGoodbye!")
                break

    def _run_basic(self) -> None:
        """Run basic REPL without prompt_toolkit."""
        while True:
            try:
                prompt = "... " if self.in_multiline else "> "
                line = input(prompt)

                if line.startswith(":"):
                    result = self._handle_command(line)
                    if result == "exit":
                        break
                    continue

                self._process_line(line)

            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                self.multiline_buffer = []
                self.in_multiline = False
            except EOFError:
                print("\nGoodbye!")
                break

    def _process_line(self, line: str) -> None:
        """Process a line of input."""
        self.multiline_buffer.append(line)

        # Check if we're in a multiline block
        if self._is_block_start(line):
            self.in_multiline = True
            return

        # Check if block ends
        if self.in_multiline and self._is_block_end(line):
            self.in_multiline = False
            self._execute_buffer()
            self.multiline_buffer = []
            return

        # If not in multiline and line ends with period, execute
        if not self.in_multiline and line.endswith("."):
            self._execute_buffer()
            self.multiline_buffer = []

    def _is_block_start(self, line: str) -> bool:
        """Check if a line starts a block."""
        return line.endswith(":")

    def _is_block_end(self, line: str) -> bool:
        """Check if a line ends a block."""
        keywords = ["end the function", "end the loop", "end the repetition", "end the match", "end the type", "end the enumeration"]
        return any(kw in line.lower() for kw in keywords)

    def _execute_buffer(self) -> None:
        """Execute the buffered code."""
        source = "\n".join(self.multiline_buffer)

        # Lex
        lexer = Lexer(source, "<repl>")
        tokens = lexer.tokenize()

        lexer_errors = lexer.get_errors()
        if lexer_errors:
            reporter = DiagnosticReporter()
            for error in lexer_errors:
                reporter.add_error(error.message, error.location)
            print(reporter.format_all(), file=sys.stderr)
            return

        # Parse
        parser = Parser(tokens)
        program = parser.parse()

        parse_errors = parser.get_errors()
        if parse_errors:
            reporter = DiagnosticReporter()
            for error in parse_errors:
                reporter.add_error(error.message, error.location)
            print(reporter.format_all(), file=sys.stderr)
            return

        # Interpret
        try:
            result = self.interpreter.interpret(program)
            if result is not None:
                print(self._value_to_string(result))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

    def _handle_command(self, line: str) -> Optional[str]:
        """Handle a REPL command."""
        command = line[1:].strip().lower()

        if command in ["exit", "quit"]:
            return "exit"

        if command == "help":
            self._show_help()
        elif command == "clear":
            self.multiline_buffer = []
            self.in_multiline = False
            print("Buffer cleared")
        elif command == "reset":
            self.interpreter = Interpreter()
            self.multiline_buffer = []
            self.in_multiline = False
            print("Environment reset")
        elif command.startswith("load"):
            parts = command.split()
            if len(parts) > 1:
                self._load_file(parts[1])
            else:
                print("Usage: :load <filename>")
        elif command.startswith("save"):
            parts = command.split()
            if len(parts) > 1:
                self._save_file(parts[1])
            else:
                print("Usage: :save <filename>")
        elif command.startswith("type"):
            parts = command.split()
            if len(parts) > 1:
                self._show_type(parts[1])
            else:
                print("Usage: :type <variable>")
        elif command == "ast":
            if self.multiline_buffer:
                self._show_ast()
            else:
                print("No code to show AST for")
        else:
            print(f"Unknown command: {command}")
            print("Type :help for available commands")

        return None

    def _show_help(self) -> None:
        """Show help information."""
        print("Available commands:")
        print("  :help     - Show this help")
        print("  :clear    - Clear the input buffer")
        print("  :reset    - Reset the environment")
        print("  :load     - Load a file into the REPL")
        print("  :save     - Save the current buffer to a file")
        print("  :type     - Show the type of a variable")
        print("  :ast      - Show the AST of the current buffer")
        print("  :exit     - Exit the REPL")
        print("  :quit     - Exit the REPL")

    def _load_file(self, filename: str) -> None:
        """Load a file into the REPL."""
        try:
            with open(filename, "r") as f:
                source = f.read()

            lexer = Lexer(source, filename)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()

            self.interpreter.interpret(program)
            print(f"Loaded: {filename}")
        except IOError as e:
            print(f"Error loading file: {e}", file=sys.stderr)

    def _save_file(self, filename: str) -> None:
        """Save the current buffer to a file."""
        try:
            with open(filename, "w") as f:
                f.write("\n".join(self.multiline_buffer))
            print(f"Saved to: {filename}")
        except IOError as e:
            print(f"Error saving file: {e}", file=sys.stderr)

    def _show_type(self, var_name: str) -> None:
        """Show the type of a variable."""
        value = self.interpreter.environment.get(var_name)
        if value is None:
            print(f"Undefined variable: {var_name}")
        else:
            print(f"{var_name}: {value.type.value}")

    def _show_ast(self) -> None:
        """Show the AST of the current buffer."""
        source = "\n".join(self.multiline_buffer)
        lexer = Lexer(source, "<repl>")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        print(program)

    def _value_to_string(self, value: Value) -> str:
        """Convert a value to string for display."""
        if value is None:
            return ""
        if value.type == ValueType.NOTHING:
            return "nothing"
        if value.type == ValueType.TEXT:
            return value.value
        if value.type == ValueType.BOOLEAN:
            return "true" if value.value else "false"
        if value.type == ValueType.NUMBER:
            return str(value.value)
        if value.type == ValueType.DECIMAL:
            return str(value.value)
        if value.type == ValueType.LIST:
            return f"[{', '.join(self._value_to_string(v) for v in value.value)}]"
        if value.type == ValueType.MAP:
            pairs = [f'"{k}": {self._value_to_string(v)}' for k, v in value.value.items()]
            return f"{{{', '.join(pairs)}}}"
        return str(value.value)

    def _get_version(self) -> str:
        """Get the version string."""
        try:
            from .. import __version__
            return __version__
        except ImportError:
            return "0.1.0"

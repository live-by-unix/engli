"""
Lexer for the Engli programming language.
"""

import re
from typing import List, Optional
from dataclasses import dataclass

from .tokens import Token, TokenType, SourceLocation, KEYWORDS


@dataclass
class LexerError:
    """An error from the lexer."""

    message: str
    location: SourceLocation


class Lexer:
    """Lexes Engli source code into tokens."""

    def __init__(self, source: str, filename: str = "<string>"):
        self.source = source
        self.filename = filename
        self.position = 0
        self.line = 1
        self.column = 1
        self.errors: List[LexerError] = []

        # Track indentation for Python-like blocks
        self.indent_stack = [0]
        self.at_line_start = True
        self.expect_indent = False  # Flag to expect indent on next line

    def current_char(self) -> Optional[str]:
        """Get the current character."""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at a character."""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self) -> Optional[str]:
        """Advance to the next character."""
        char = self.current_char()
        if char is None:
            return None

        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
            self.at_line_start = True
        else:
            self.column += 1
            self.at_line_start = False

        return char

    def skip_whitespace(self, tokens: List[Token]) -> None:
        """Skip whitespace (but track indentation at line start)."""
        if not self.at_line_start:
            # Skip regular whitespace in the middle of a line
            while self.current_char() and self.current_char() in " \t":
                self.advance()
            return

        # At line start, count indentation
        indent = 0
        while self.current_char() and self.current_char() in " \t":
            if self.current_char() == " ":
                indent += 1
            else:  # Tab
                indent += 4  # Treat tab as 4 spaces
            self.advance()

        # Check if this is a blank line (only whitespace, then newline or EOF)
        # Blank lines should not trigger INDENT/DEDENT
        if self.current_char() is None or self.current_char() == "\n":
            return

        # Only generate INDENT/DEDENT if indentation actually changed or we expect an indent
        if self.expect_indent and indent > self.indent_stack[-1]:
            self.indent_stack.append(indent)
            tokens.append(self._emit(TokenType.INDENT, "indent"))
            self.expect_indent = False
        elif indent > self.indent_stack[-1]:
            self.indent_stack.append(indent)
            tokens.append(self._emit(TokenType.INDENT, "indent"))
        elif indent < self.indent_stack[-1]:
            while self.indent_stack and indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                tokens.append(self._emit(TokenType.DEDENT, "dedent"))

    def location(self) -> SourceLocation:
        """Get the current source location."""
        return SourceLocation(self.filename, self.line, self.column, self.source)

    def _emit(self, token_type: TokenType, value: str) -> Token:
        """Emit a token (returns without adding to list)."""
        return Token(token_type, value, self.location())

    def read_number(self) -> Token:
        """Read a number literal."""
        start = self.position
        location = self.location()

        # Read integer part
        while self.current_char() and self.current_char().isdigit():
            self.advance()

        # Check for decimal (only if followed by digit)
        if self.current_char() == "." and self.peek_char() and self.peek_char().isdigit():
            self.advance()
            while self.current_char() and self.current_char().isdigit():
                self.advance()

        value = self.source[start:self.position]
        return Token(TokenType.NUMBER, value, location)

    def read_string(self) -> Token:
        """Read a string literal."""
        quote = self.current_char()
        location = self.location()
        self.advance()  # Skip opening quote

        value_chars = []
        while self.current_char() and self.current_char() != quote:
            # Handle escape sequences
            if self.current_char() == "\\":
                self.advance()
                if self.current_char() is None:
                    self.errors.append(LexerError("Unterminated string", location))
                    return Token(TokenType.ERROR, "", location)

                # Handle standard escape sequences
                escape_char = self.current_char()
                escapes = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "\\": "\\",
                    '"': '"',
                    "'": "'",
                }
                value_chars.append(escapes.get(escape_char, escape_char))
                self.advance()
            else:
                value_chars.append(self.current_char())
                self.advance()

        if self.current_char() != quote:
            self.errors.append(LexerError("Unterminated string", location))
            return Token(TokenType.ERROR, "", location)

        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, "".join(value_chars), location)

    def read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start = self.position
        location = self.location()

        while self.current_char() and (self.current_char().isalnum() or self.current_char() == "_"):
            self.advance()

        value = self.source[start:self.position].lower()

        # Check if it's a boolean literal
        if value in ["true", "false", "yes", "no"]:
            return Token(TokenType.BOOLEAN, value, location)

        # Check if it's a keyword
        if value in KEYWORDS:
            return Token(TokenType.KEYWORD, value, location)

        return Token(TokenType.IDENTIFIER, value, location)

    def read_comment(self) -> None:
        """Read a single-line comment."""
        while self.current_char() and self.current_char() != "\n":
            self.advance()

    def read_multiline_comment(self) -> None:
        """Read a multiline comment."""
        self.advance()  # Skip /
        self.advance()  # Skip *

        while self.current_char():
            if self.current_char() == "*" and self.peek_char() == "/":
                self.advance()  # Skip *
                self.advance()  # Skip /
                return
            self.advance()

        # Unterminated comment
        self.errors.append(LexerError("Unterminated multiline comment", self.location()))

    def tokenize(self) -> List[Token]:
        """Tokenize the entire source."""
        tokens: List[Token] = []

        while self.current_char() is not None:
            # Handle indentation at line start
            if self.at_line_start:
                self.skip_whitespace(tokens)

            char = self.current_char()

            # Skip comments
            if char == "#":
                self.read_comment()
                continue

            if char == "/" and self.peek_char() == "*":
                self.read_multiline_comment()
                continue

            # Newline
            if char == "\n":
                location = self.location()
                self.advance()
                tokens.append(Token(TokenType.NEWLINE, "\\n", location))
                continue

            # Skip whitespace in middle of line
            if char in " \t":
                self.advance()
                continue

            # Numbers
            if char.isdigit():
                tokens.append(self.read_number())
                continue

            # Strings
            if char in '"\'':
                tokens.append(self.read_string())
                continue

            # Identifiers and keywords
            if char.isalpha() or char == "_":
                tokens.append(self.read_identifier())
                continue

            # Punctuation and operators
            location = self.location()

            # Period (statement terminator)
            if char == ".":
                self.advance()
                tokens.append(Token(TokenType.PERIOD, ".", location))
                continue

            # Comma (statement continuation or separator)
            if char == ",":
                self.advance()
                tokens.append(Token(TokenType.COMMA, ",", location))
                continue

            # Colon (block start)
            if char == ":":
                self.advance()
                tokens.append(Token(TokenType.COLON, ":", location))
                # Set flag to expect indent on next line
                self.expect_indent = True
                continue

            # Parentheses
            if char == "(":
                self.advance()
                tokens.append(Token(TokenType.LEFT_PAREN, "(", location))
                continue

            if char == ")":
                self.advance()
                tokens.append(Token(TokenType.RIGHT_PAREN, ")", location))
                continue

            # Brackets
            if char == "[":
                self.advance()
                tokens.append(Token(TokenType.LEFT_BRACKET, "[", location))
                continue

            if char == "]":
                self.advance()
                tokens.append(Token(TokenType.RIGHT_BRACKET, "]", location))
                continue

            # Braces
            if char == "{":
                self.advance()
                tokens.append(Token(TokenType.LEFT_BRACE, "{", location))
                continue

            if char == "}":
                self.advance()
                tokens.append(Token(TokenType.RIGHT_BRACE, "}", location))
                continue

            # Error: unknown character
            self.errors.append(LexerError(f"Unknown character: {char}", location))
            self.advance()
            tokens.append(Token(TokenType.ERROR, char, location))

        # Emit remaining DEDENTs
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, "dedent", self.location()))

        # EOF
        tokens.append(Token(TokenType.EOF, "", self.location()))

        return tokens

    def get_errors(self) -> List[LexerError]:
        """Get all lexer errors."""
        return self.errors

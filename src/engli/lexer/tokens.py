"""
Token definitions for the Engli lexer.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class TokenType(Enum):
    """Token types in Engli."""

    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NOTHING = auto()

    # Identifiers and keywords
    IDENTIFIER = auto()
    KEYWORD = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLIED = auto()
    DIVIDED = auto()
    MODULO = auto()

    # Comparisons
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()

    # Boolean operators
    AND = auto()
    OR = auto()
    NOT = auto()

    # Punctuation
    PERIOD = auto()
    COMMA = auto()
    COLON = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    # Special
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    EOF = auto()
    ERROR = auto()


@dataclass
class SourceLocation:
    """Source location information for error reporting."""

    filename: str
    line: int
    column: int
    source: str

    def __str__(self) -> str:
        return f"{self.filename}:{self.line}:{self.column}"


@dataclass
class Token:
    """A token from the Engli lexer."""

    type: TokenType
    value: str
    location: SourceLocation

    def __str__(self) -> str:
        return f"Token({self.type.name}, {repr(self.value)}, {self.location})"

    def __repr__(self) -> str:
        return self.__str__()


# Reserved keywords
KEYWORDS = {
    "set",
    "to",
    "subtract",
    "multiplied",
    "divided",
    "modulo",
    "define",
    "the",
    "constant",
    "as",
    "is",
    "if",
    "otherwise",
    "while",
    "for",
    "each",
    "in",
    "from",
    "through",
    "repeat",
    "times",
    "forever",
    "end",
    "break",
    "continue",
    "function",
    "called",
    "takes",
    "return",
    "a",
    "an",
    "which",
    "has",
    "type",
    "enumeration",
    "containing",
    "create",
    "object",
    "map",
    "list",
    "set",
    "with",
    "mapped",
    "at",
    "index",
    "say",
    "ask",
    "store",
    "answer",
    "read",
    "write",
    "append",
    "file",
    "exists",
    "directory",
    "delete",
    "environment",
    "variable",
    "run",
    "command",
    "arguments",
    "shell",
    "send",
    "get",
    "post",
    "put",
    "patch",
    "request",
    "json",
    "parse",
    "convert",
    "try",
    "error",
    "occurs",
    "throw",
    "nothing",
    "true",
    "false",
    "or",
    "match",
    "when",
    "export",
    "import",
    "task",
    "start",
    "wait",
    "finish",
    "channel",
    "receive",
    "through",
    "current",
    "date",
    "time",
    "unix",
    "timestamp",
    "random",
    "between",
    "and",
    "server",
    "on",
    "port",
    "respond",
    "length",
    "of",
    "into",
    "plus",
    "minus",
    "by",
    "equal",
    "is",
    "not",
    "greater",
    "less",
    "than",
    "exit",
    "quit",
    "help",
    "clear",
    "reset",
    "load",
    "save",
    "type",
    "ast",
}

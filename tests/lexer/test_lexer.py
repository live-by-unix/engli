"""
Tests for the Engli lexer.
"""

import pytest

from engli.lexer import Lexer, TokenType, KEYWORDS


class TestLexer:
    """Test lexer functionality."""

    def test_numbers(self):
        """Test number tokenization."""
        lexer = Lexer("123 45.67")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == "123"
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == "45.67"

    def test_strings(self):
        """Test string tokenization."""
        lexer = Lexer('"hello" \'world\'')
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "world"

    def test_identifiers(self):
        """Test identifier tokenization."""
        lexer = Lexer("x variable_name function123")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "variable_name"
        assert tokens[2].type == TokenType.IDENTIFIER
        assert tokens[2].value == "function123"

    def test_keywords(self):
        """Test keyword tokenization."""
        lexer = Lexer("set if while for")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.KEYWORD
        assert tokens[0].value == "set"
        assert tokens[1].type == TokenType.KEYWORD
        assert tokens[1].value == "if"
        assert tokens[2].type == TokenType.KEYWORD
        assert tokens[2].value == "while"
        assert tokens[3].type == TokenType.KEYWORD
        assert tokens[3].value == "for"

    def test_punctuation(self):
        """Test punctuation tokenization."""
        lexer = Lexer(". , : ( ) [ ] { }")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.PERIOD
        assert tokens[1].type == TokenType.COMMA
        assert tokens[2].type == TokenType.COLON
        assert tokens[3].type == TokenType.LEFT_PAREN
        assert tokens[4].type == TokenType.RIGHT_PAREN
        assert tokens[5].type == TokenType.LEFT_BRACKET
        assert tokens[6].type == TokenType.RIGHT_BRACKET
        assert tokens[7].type == TokenType.LEFT_BRACE
        assert tokens[8].type == TokenType.RIGHT_BRACE

    def test_comments(self):
        """Test comment handling."""
        lexer = Lexer("x # comment\ny")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"
        assert tokens[1].type == TokenType.NEWLINE
        assert tokens[2].type == TokenType.IDENTIFIER
        assert tokens[2].value == "y"

    def test_multiline_comment(self):
        """Test multiline comment handling."""
        lexer = Lexer("x /* comment */ y")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "y"

    def test_indentation(self):
        """Test indentation handling."""
        lexer = Lexer("if x:\n    y\nz")
        tokens = lexer.tokenize()

        assert tokens[4].type == TokenType.INDENT
        assert tokens[7].type == TokenType.DEDENT

    def test_string_escapes(self):
        """Test string escape sequences."""
        lexer = Lexer('"hello\\nworld"')
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello\nworld"

    def test_eof(self):
        """Test EOF token."""
        lexer = Lexer("x")
        tokens = lexer.tokenize()

        assert tokens[-1].type == TokenType.EOF

    def test_all_keywords_in_set(self):
        """Test that all common keywords are in the KEYWORDS set."""
        common_keywords = ["set", "to", "if", "otherwise", "while", "for", "in", "from", "through", "function", "called", "takes", "return", "say", "ask", "read", "write", "create", "delete", "import", "export", "try", "error", "match", "when", "end", "break", "continue", "repeat", "times", "forever", "true", "false", "nothing", "and", "or", "not", "plus", "minus", "multiplied", "divided", "modulo", "is", "equal", "greater", "less", "than"]

        for keyword in common_keywords:
            assert keyword in KEYWORDS, f"Keyword '{keyword}' not in KEYWORDS set"

"""
Tests for the Engli semantic analyzer.
"""

import pytest

from engli.lexer import Lexer
from engli.parser import Parser
from engli.semantics import SemanticAnalyzer


class TestSemanticAnalyzer:
    """Test semantic analyzer functionality."""

    def test_undefined_variable(self):
        """Test detection of undefined variables."""
        source = 'Set x to y.'
        lexer = Lexer(source, "<test>")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        analyzer = SemanticAnalyzer()
        analyzer.analyze(program)

        errors = analyzer.get_errors()
        assert len(errors) > 0
        assert "undefined variable" in errors[0].message.lower()

    def test_break_outside_loop(self):
        """Test detection of break outside loop."""
        source = 'Break out of the loop.'
        lexer = Lexer(source, "<test>")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        analyzer = SemanticAnalyzer()
        analyzer.analyze(program)

        errors = analyzer.get_errors()
        assert len(errors) > 0
        assert "break" in errors[0].message.lower()

    def test_return_outside_function(self):
        """Test detection of return outside function."""
        source = 'Return 10.'
        lexer = Lexer(source, "<test>")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        analyzer = SemanticAnalyzer()
        analyzer.analyze(program)

        errors = analyzer.get_errors()
        assert len(errors) > 0
        assert "return" in errors[0].message.lower()

    def test_valid_program(self):
        """Test that a valid program passes analysis."""
        source = 'Set x to 10.\nSet y to 20.\nSet z to x plus y.'
        lexer = Lexer(source, "<test>")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(program)

        assert result is True
        assert len(analyzer.get_errors()) == 0
